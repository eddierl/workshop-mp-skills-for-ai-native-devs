// Skills Night live room: one Durable Object holds the current slide, poll votes and audience questions,
// and pushes a summary to every phone and screen over WebSockets. Static pages come from ../docs.
import { DurableObject } from 'cloudflare:workers';

const MAX_QUESTION = 280;
const MAX_QUESTIONS_EACH = 10;
const MAX_NAME = 40;
const MAX_ANSWER = 200;
const WALL_SIZE = 40;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/ws') {
      if (request.headers.get('Upgrade') !== 'websocket') return new Response('Expected a WebSocket', { status: 426 });
      return env.ROOM.get(env.ROOM.idFromName('skills-night')).fetch(request);
    }
    if (url.pathname === '/join' || url.pathname === '/live') return Response.redirect(new URL('/live/', url), 302);
    if (url.pathname === '/api/health') return Response.json({ ok: true, host: Boolean(env.HOST_KEY) });
    return env.ASSETS.fetch(request);
  }
};

function emptyState() {
  return { slide: 0, reveal: {}, votes: {}, answers: {}, questions: [] };
}

export class Room extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.state = emptyState();
    this.pending = null;
    ctx.blockConcurrencyWhile(async () => {
      this.state = { ...emptyState(), ...(await ctx.storage.get('state')) };
    });
  }

  async fetch(request) {
    const url = new URL(request.url);
    const role = url.searchParams.get('role') || 'phone';
    const id = (url.searchParams.get('id') || '').slice(0, 64);
    const key = url.searchParams.get('key') || '';
    const isHost = Boolean(this.env.HOST_KEY) && key === this.env.HOST_KEY;
    if ((role === 'host' || key) && !isHost) return new Response('Wrong host key', { status: 403 });
    if (role === 'phone' && !id) return new Response('Missing id', { status: 400 });

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    this.ctx.acceptWebSocket(server, [role]);
    server.serializeAttachment({ role, id, host: isHost });
    server.send(JSON.stringify({ type: 'state', state: this.publicState(isHost), host: isHost }));
    if (role === 'phone') server.send(JSON.stringify({ type: 'you', ...this.mine(id) }));
    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws, raw) {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }
    const who = ws.deserializeAttachment() || {};
    const s = this.state;

    if (msg.type === 'ping') { ws.send('{"type":"pong"}'); return; }

    if (msg.type === 'vote' && who.id && typeof msg.poll === 'string' && Array.isArray(msg.choices)) {
      const choices = [...new Set(msg.choices.filter(n => Number.isInteger(n) && n >= 0 && n < 12))].slice(0, 12);
      s.votes[msg.poll] = s.votes[msg.poll] || {};
      if (choices.length) s.votes[msg.poll][who.id] = choices;
      else delete s.votes[msg.poll][who.id];
      ws.send(JSON.stringify({ type: 'you', ...this.mine(who.id) }));
      return this.changed();
    }

    // A short written answer, one per person per prompt; sending again replaces it, sending nothing withdraws it
    if (msg.type === 'answer' && who.id && typeof msg.poll === 'string' && typeof msg.text === 'string') {
      const text = msg.text.trim().slice(0, MAX_ANSWER);
      s.answers[msg.poll] = s.answers[msg.poll] || {};
      if (text) s.answers[msg.poll][who.id] = { id: crypto.randomUUID().slice(0, 8), text, ts: Date.now(), hidden: false };
      else delete s.answers[msg.poll][who.id];
      ws.send(JSON.stringify({ type: 'you', ...this.mine(who.id) }));
      return this.changed();
    }

    if (msg.type === 'ask' && who.id && typeof msg.text === 'string') {
      const text = msg.text.trim().slice(0, MAX_QUESTION);
      if (!text || s.questions.filter(q => q.by === who.id).length >= MAX_QUESTIONS_EACH) return;
      const name = typeof msg.name === 'string' ? msg.name.trim().slice(0, MAX_NAME) : '';
      s.questions.push({ id: crypto.randomUUID().slice(0, 8), text, name, by: who.id, ts: Date.now(), up: [], done: false, hidden: false });
      ws.send(JSON.stringify({ type: 'you', ...this.mine(who.id) }));
      return this.changed();
    }

    if (msg.type === 'upvote' && who.id) {
      const q = s.questions.find(q => q.id === msg.q);
      if (!q || q.by === who.id) return;
      q.up = q.up.includes(who.id) ? q.up.filter(x => x !== who.id) : [...q.up, who.id];
      ws.send(JSON.stringify({ type: 'you', ...this.mine(who.id) }));
      return this.changed();
    }

    if (!who.host) return;

    if (msg.type === 'goto' && Number.isInteger(msg.slide) && msg.slide >= 0 && msg.slide < 200) {
      s.slide = msg.slide;
      return this.changed();
    }
    if (msg.type === 'reveal' && typeof msg.poll === 'string') {
      s.reveal[msg.poll] = !s.reveal[msg.poll];
      return this.changed();
    }
    if (msg.type === 'question' && typeof msg.q === 'string') {
      const q = s.questions.find(q => q.id === msg.q);
      if (!q) return;
      if (msg.action === 'done') q.done = !q.done;
      if (msg.action === 'hide') q.hidden = !q.hidden;
      return this.changed();
    }
    if (msg.type === 'hideAnswer' && typeof msg.poll === 'string' && typeof msg.a === 'string') {
      const a = Object.values(s.answers[msg.poll] || {}).find(a => a.id === msg.a);
      if (!a) return;
      a.hidden = !a.hidden;
      return this.changed();
    }
    if (msg.type === 'clearPoll' && typeof msg.poll === 'string') {
      delete s.votes[msg.poll];
      delete s.answers[msg.poll];
      delete s.reveal[msg.poll];
      return this.changed();
    }
    if (msg.type === 'resetAll') {
      this.state = { ...emptyState(), slide: s.slide };
      this.broadcast({ type: 'you', votes: {}, answers: {}, upped: [], asked: [] }, 'phone');
      return this.changed();
    }
    // Timer and spotlight commands go straight to the screens, which own the countdown
    if (msg.type === 'cmd' && typeof msg.cmd === 'string') {
      this.broadcast({ type: 'cmd', cmd: msg.cmd.slice(0, 20) }, 'screen');
    }
  }

  webSocketClose(ws, code) {
    try { ws.close(code, 'bye'); } catch {}
    this.changed(false);
  }

  webSocketError() { this.changed(false); }

  mine(id) {
    const votes = {};
    for (const [poll, byId] of Object.entries(this.state.votes)) if (byId[id]) votes[poll] = byId[id];
    const answers = {};
    for (const [poll, byId] of Object.entries(this.state.answers)) if (byId[id]) answers[poll] = byId[id].text;
    return {
      votes,
      answers,
      upped: this.state.questions.filter(q => q.up.includes(id)).map(q => q.id),
      asked: this.state.questions.filter(q => q.by === id).map(q => q.id)
    };
  }

  publicState(forHost = false) {
    const s = this.state;
    const tallies = {};
    for (const [poll, byId] of Object.entries(s.votes)) {
      const counts = [];
      let voters = 0;
      for (const choices of Object.values(byId)) {
        voters++;
        for (const c of choices) counts[c] = (counts[c] || 0) + 1;
      }
      tallies[poll] = { counts: Array.from(counts, n => n || 0), voters };
    }
    // Newest answers first; the host also sees the hidden ones so they can be shown again
    const walls = {};
    for (const [poll, byId] of Object.entries(s.answers)) {
      const all = Object.values(byId).sort((a, b) => b.ts - a.ts);
      walls[poll] = {
        count: all.filter(a => !a.hidden).length,
        items: all.filter(a => forHost || !a.hidden).slice(0, WALL_SIZE).map(a => ({ id: a.id, text: a.text, hidden: a.hidden || undefined }))
      };
    }
    const questions = s.questions
      .filter(q => !q.hidden)
      .map(q => ({ id: q.id, text: q.text, name: q.name, ups: q.up.length, done: q.done, ts: q.ts }));
    const hidden = forHost ? s.questions.filter(q => q.hidden).map(q => ({ id: q.id, text: q.text, name: q.name, ups: q.up.length, done: q.done, ts: q.ts, hidden: true })) : [];
    return {
      slide: s.slide,
      reveal: s.reveal,
      tallies,
      walls,
      questions,
      hidden,
      online: this.ctx.getWebSockets('phone').length
    };
  }

  // Coalesce bursts of votes into one save and one broadcast every quarter second
  changed(save = true) {
    if (save) this.dirty = true;
    if (this.pending) return;
    this.pending = setTimeout(async () => {
      this.pending = null;
      if (this.dirty) { this.dirty = false; await this.ctx.storage.put('state', this.state); }
      const state = this.publicState(true);
      const forAll = this.publicState(false);
      for (const ws of this.ctx.getWebSockets()) {
        const who = ws.deserializeAttachment() || {};
        try { ws.send(JSON.stringify({ type: 'state', state: who.host ? state : forAll, host: who.host })); } catch {}
      }
    }, 250);
  }

  broadcast(msg, tag) {
    const text = JSON.stringify(msg);
    for (const ws of this.ctx.getWebSockets(tag)) { try { ws.send(text); } catch {} }
  }
}
