# Skills Night live

One deck for the whole night, Raf's Part 1 and Mash's Part 2, with three views:

| View | URL | Who |
| --- | --- | --- |
| Phone | `/live/` | Everyone, from the QR on screen. Follows the projector, votes on polls, answers quick checks, writes short answers that go up as a wall, asks and upvotes questions. |
| Projector | `/live/screen.html?key=HOST_KEY` | The laptop on the projector. With the key, its arrow keys move every phone too. Without a key it only follows. |
| Host remote | `/live/host.html?key=HOST_KEY` | A phone or tablet: next and back, timer, reveal answers, hide a written answer, mark questions answered or hide them. |

The key is taken out of the address bar and remembered on that device, so you only open the `?key=` link once.

The slides, polls and quick checks are all in `docs/live/deck.js`. Edit that one file.

## Keys on the projector

← → move · T start or pause the slide's timer · R reset it · V reveal a quick check's answer · F full screen

## Deploy (Cloudflare)

It deploys to the Perth AI Cloudflare account at **https://skills.perthai.org**. perthai.org's DNS lives in that account, so Wrangler adds the subdomain and its certificate on the first deploy.

From this folder, signed in to Cloudflare as someone with access to the Perth AI account:

```sh
npm install
npx wrangler login                 # once, opens the browser
npx wrangler whoami                # check the Perth AI account is listed
npx wrangler deploy                # pick the Perth AI account if asked
npx wrangler secret put HOST_KEY   # paste a long random word; this is the host password
```

If your login sees more than one account, set the Perth AI one first: copy its Account ID from `wrangler whoami`, then run `set CLOUDFLARE_ACCOUNT_ID=<id>` (Windows) or `export CLOUDFLARE_ACCOUNT_ID=<id>` before deploying.

Then open `https://skills.perthai.org/live/screen.html?key=<that word>` on the projector.

- `skills.perthai.org` is the setup guide. While the room is live, it shows a "The session is live" banner and a Live link in the menu.
- `skills.perthai.org/join` goes straight to the phone page.
- To use a different subdomain, change `routes` in `wrangler.jsonc`. Remove `routes` to fall back to a `workers.dev` address.

The Worker serves all of `docs/` as static files and runs one Durable Object for the room (free plan is fine).
Votes and questions survive a redeploy. To start clean after a rehearsal, use **Clear all votes and questions** on the host remote.

## Try it locally

```sh
echo HOST_KEY=dev > .dev.vars
npx wrangler dev
```

Open http://localhost:8787/live/screen.html?key=dev and http://localhost:8787/live/ in another window.

## If the backend is down

Open `docs/live/screen.html` straight from disk, or from GitHub Pages. It runs as plain slides: arrows move, polls show their options for a show of hands, and V still reveals quick-check answers.
