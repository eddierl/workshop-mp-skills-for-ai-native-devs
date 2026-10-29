// Skills Night: the one script for the night. The projector, the host remote and every phone render from this list.
// A slide may carry one thing for phones to do:
//   poll:  { q, options, multi }                  tap to vote, bars on screen
//          add answer and explain for a quick check, revealed with V
//   write: { q, placeholder }                     a short written answer, shown as a wall on screen
// minutes sets the countdown the host starts with T. qr names a link from DECK.links.
// Part 1 follows the Part 1 handout (workshop/handout.html on raf/feature/workbook), cut to fit an hour.
window.DECK = {
  slides: [
    {
      name: 'welcome', part: 'Setup', scenic: true, qr: 'setup',
      kicker: 'While we get going',
      say: 'Scan in, <em>then get set up.</em>',
      sub: 'Work down the setup guide, and put your hand up if you get stuck. Keep the page open: the live link at the top is tonight’s remote for polls and questions.'
    },
    {
      name: 'tonight', part: 'Setup', scenic: true,
      kicker: 'Perth AI · Skills for AI-native devs',
      say: 'Slow down the thinking. <em>Speed up the building.</em>',
      agenda: [['1', 'Part 1', 'Fix a buggy shop'], ['2', 'Pizza', ''], ['3', 'Part 2', 'Build a feature'], ['4', 'Q&A, then demos', '']]
    },

    // Part 1: about 60 minutes
    {
      name: 'part1', part: 'Part 1', scenic: true,
      kicker: 'Part 1',
      say: 'The shop is buggy. <em>Let’s find out why.</em>'
    },
    {
      name: 'room', part: 'Part 1',
      kicker: 'Who’s in the room',
      say: 'How comfortable are you <em>on the command line?</em>',
      poll: { q: 'How comfortable are you with the command line?', options: ['What’s a command line?', 'Beginner', 'Intermediate', 'Advanced'] }
    },
    {
      name: 'warmup', part: 'Part 1', minutes: 5,
      kicker: 'Warm-up',
      say: 'Which could you <em>explain to a friend?</em>',
      sub: 'Tick every one you could. If you’re not sure, leave it. We’ll explain the ones the room is least sure of.',
      poll: { q: 'Which could you explain to a friend?', multi: true, options: ['AI', 'LLM', 'Token', 'Agent', 'Harness', 'Markdown', 'Shell', 'TUI', 'Skill', 'Context window'] }
    },
    {
      name: 'scenario', part: 'Part 1',
      kicker: 'The scenario',
      say: 'A decade-old C# shop, <em>vibe-coded into Python.</em>',
      sub: 'The owners are commercial people, not engineers. They rewrote it with tools like the ones you’re holding. It mostly works. It’s also pretty buggy.',
      cards: [['Keep', 'The styling, which was real investment, and the shopping flow that works.'], ['Fix', 'The defects. Then set up a better way of working, so they stop arriving.']]
    },
    {
      name: 'run', part: 'Part 1', minutes: 10,
      kicker: 'Your turn',
      say: 'Run the shop. <em>Click around.</em>',
      prompt: 'cd python-eshop/backend\nuv sync\nuv run python run.py\n\ncd python-eshop/frontend\nnpm install\nnpm run dev',
      chips: ['backend running', 'frontend running', 'logged in as the demo user', 'catalog → basket → checkout → orders'],
      write: { q: 'First impressions: what feels solid, and where did something feel off?', placeholder: 'Even before you know it’s officially a bug' }
    },
    {
      name: 'retro', part: 'Part 1', minutes: 5,
      kicker: 'Retro: what went wrong?',
      say: 'Why does vibe-coded software <em>end up like this?</em>',
      poll: { q: 'Tick the failure modes you suspect played a part.', multi: true, options: ['No shared spec', 'No plan before coding', 'No tests', 'Context ran out', 'No code review', 'One-shot prompts', 'Couldn’t read the code', 'Something else'] }
    },
    {
      name: 'differently', part: 'Part 1', minutes: 5,
      kicker: 'Retro: what went wrong?',
      say: 'How would <em>you</em> have done it differently?',
      sub: 'A sentence or two, then we open the floor.',
      write: { q: 'How would you have approached it differently?', placeholder: 'A sentence or two' }
    },
    {
      name: 'gut', part: 'Part 1',
      kicker: 'Gut call',
      say: 'A tooling problem, or <em>a process problem?</em>',
      poll: { q: 'Is this mostly a tooling problem or a process problem?', options: ['Mostly tooling', 'A bit of both', 'Mostly process', 'Not sure yet'] }
    },
    {
      name: 'skills', part: 'Part 1',
      kicker: 'Introducing skills',
      say: 'Reusable workflows that sit <em>on top of the model.</em>',
      sub: 'Matt Pocock’s skills are aimed squarely at the failure modes you just ticked. Claude Code, Codex, Copilot and others all read them.',
      cards: [['Helps', 'Forces understanding before code, gives review a fixed point to check against, and turns vibing into something repeatable.'], ['Gaps', 'Doesn’t replace judgement about scope. A skill is only as good as whoever chooses when to use it.']]
    },
    {
      name: 'check1', part: 'Part 1',
      kicker: 'Quick check 1',
      say: 'Do skills run <em>automatically</em> when relevant?',
      poll: {
        q: 'Do skills run automatically when relevant?', options: ['Always', 'Never', 'It depends'], answer: 2,
        explain: 'It depends on the harness and the skill. Most of Matt’s skills wait for you to call them; some the model can pick by itself. Triage opts out in both:',
        code: '# triage/SKILL.md\ndisable-model-invocation: true\n\n# Codex\npolicy:\n  allow_implicit_invocation: false'
      }
    },
    {
      name: 'check2', part: 'Part 1',
      kicker: 'Quick check 2',
      say: 'A skill loads everything it links to, <em>all at once.</em>',
      poll: {
        q: 'Skills load all the information from their links at once.', options: ['True', 'False'], answer: 1,
        explain: 'False. Skills load progressively: the header first, the instructions when the skill is used, and linked files only as needed. That keeps your context window under control.'
      }
    },
    {
      name: 'frontmatter', part: 'Part 1', minutes: 5,
      kicker: 'Look inside one',
      say: 'The header is <em>the label on the folder.</em>',
      prompt: '---\nname: triage\ndescription: Move an issue from vague to ready for an agent…\ndisable-model-invocation: true\n---\n<b># Everything below loads only when the skill runs</b>',
      sub: 'With your neighbour, open one skill’s SKILL.md. What does the header declare, and where did installing it put the files?'
    },
    {
      name: 'shortlist', part: 'Part 1',
      kicker: 'Tonight’s shortlist',
      say: 'Go deep on a few, <em>not a tour of all of them.</em>',
      cards: [['/ask-matt', 'The router. Describe your situation and it points you at the skill that fits.'], ['/grill-with-docs · must have', 'A relentless interview about your plan. It writes down what you agree, and forces understanding before anyone edits code.']],
      poll: { q: 'Which 2 or 3 would you add?', multi: true, options: ['/triage: vague report to clear brief', '/wayfinder: a map for work too big for one sitting', 'code-review: a fixed point to review against', '/implement: build, check, repeat', 'prototype: a throwaway spike to de-risk'] }
    },
    {
      name: 'setup', part: 'Part 1', minutes: 5,
      kicker: 'Practical 1 · Set up',
      say: 'Install them, then <em>know what that did.</em>',
      prompt: '<b>/setup-matt-pocock-skills</b>',
      sub: 'On Codex, type <b>$</b> instead of <b>/</b>. In an agent without commands, ask for the skill by name.',
      poll: { q: 'Tick each one once it’s true for you.', multi: true, options: ['I can point to where the skill files live', 'I checked which skills I call and which the model can pick', 'Skills add to the model; they don’t replace judgement', 'I get why the header loads before the body'] }
    },
    {
      name: 'loop1', part: 'Part 1',
      kicker: 'Part 1’s loop',
      say: 'Understand it <em>before you touch it.</em>',
      flow: [['/triage', 'decide what a report needs'], ['diagnosing-bugs', 'make it fail on demand'], ['/implement', 'test first, then fix'], ['/retro', 'ask why it got in']]
    },
    {
      name: 'reports', part: 'Part 1', minutes: 5, link: 'issues',
      kicker: 'Practical 2 · Pick a bug',
      say: 'Some are vague, some are wrong, <em>some are real.</em>',
      sub: 'GitHub issues written by “customers”. Pick one, or your own, and describe it in your own words first.',
      layers: [['Frontend', 'frontend/src/', 'UI, state, API calls'], ['Router', 'backend/routers/', 'HTTP, validation, auth headers'], ['Service', 'backend/services/', 'Basket merge, checkout rules'], ['DB client', 'backend/db/client.py', 'All the SQL']],
      poll: { q: 'Before the skill: which layer do you suspect?', options: ['Frontend (React)', 'Router (FastAPI)', 'Service (rules)', 'DB client / SQL', 'Not sure yet'] }
    },
    {
      name: 'triage', part: 'Part 1', minutes: 8,
      kicker: 'Practical 2 · Triage',
      say: 'Decide what it needs, <em>before any code.</em>',
      prompt: '<b>/triage</b> issue #1',
      chips: ['needs-triage', 'needs-info', 'ready-for-agent', 'ready-for-human', 'wontfix'],
      sub: 'An agent will happily “fix” a bug that isn’t one. Triage is where you catch that, cheaply.',
      write: { q: 'What did triage surface that you hadn’t considered?', placeholder: 'One thing it asked or found' }
    },
    {
      name: 'diagnose', part: 'Part 1', minutes: 10,
      kicker: 'Practical 2 · Find the cause',
      say: 'Make it fail <em>on demand.</em>',
      prompt: 'Use the <b>diagnosing-bugs</b> skill on issue #1. Show me a command that fails because of this bug before you change any code.',
      sub: 'If you can make it happen, you can prove it’s gone. Skip this for the obvious ones.',
      poll: { q: 'How confident are you in the root cause now?', options: ['Low', 'Medium', 'High'] }
    },
    {
      name: 'backlog', part: 'Part 1',
      kicker: 'Discussion',
      say: 'Fine for one bug. <em>What about a whole backlog?</em>',
      sub: 'Where does this workflow strain? What would you hand to <b>/wayfinder</b>, and what would you still want a person on?',
      write: { q: 'How does this hold up for a backlog, not one bug?', placeholder: 'Your take' }
    },
    {
      name: 'fix', part: 'Part 1', minutes: 10,
      kicker: 'Practical 3 · Fix it, test first',
      say: 'Prove it, <em>then fix it.</em>',
      prompt: '<b>/implement</b> issue #1',
      sub: 'It writes a test that fails, makes it pass, then reviews its own change. Before you call it done:',
      chips: ['clicked through the flow again', 'backend starts clean', 'frontend builds clean', 'a test added or updated']
    },
    {
      name: 'why', part: 'Part 1', minutes: 5,
      kicker: 'Practical 3 · Ask why it got in',
      say: 'Don’t just fix it. <em>Stop the next one.</em>',
      prompt: '<b>/retro</b>',
      sub: 'Same session, before you clear. It suggests a check or a written rule that would have kept this bug out.'
    },
    {
      name: 'caught', part: 'Part 1', minutes: 5,
      kicker: 'Reflect',
      say: 'What did the skills catch that <em>plain prompting wouldn’t?</em>',
      sub: 'And where did they get in the way? Write yours first, then see how it lands against the room.',
      write: { q: 'What did the skills catch that plain prompting wouldn’t have?', placeholder: 'Or where they slowed you down' }
    },
    {
      name: 'again', part: 'Part 1',
      kicker: 'Reflect',
      say: 'Would you reach for these <em>on a real task?</em>',
      poll: { q: 'Would you reach for this skill set again on a real task?', options: ['Definitely', 'Probably, with changes', 'Not sure', 'Probably not'] }
    },
    {
      name: 'pizza', part: 'Break', scenic: true, minutes: 30, egg: true,
      kicker: 'Break',
      say: 'Pizza <em>break.</em>',
      sub: 'Got a question for later? Ask it on your phone, and vote up the ones you want answered.'
    },

    // Part 2: hands on, so no voting
    {
      name: 'part2', part: 'Part 2', scenic: true,
      kicker: 'Part 2',
      say: 'The codebase is clean. <em>Now they want features.</em>'
    },
    {
      name: 'fixed', part: 'Part 2',
      kicker: 'Where we are',
      say: 'Every bug from Part 1 is fixed, and each fix has a test.',
      sub: 'The client is happy. So they’ve asked for something new.'
    },
    {
      name: 'ask', part: 'Part 2',
      kicker: 'The ask',
      say: '“Let shoppers <em>save favourites</em>.”',
      sub: 'Signed-in shoppers can save products and see them all on one page.'
    },
    {
      name: 'tempting', part: 'Part 2',
      kicker: 'The tempting move',
      promptFirst: true,
      prompt: 'add favourites to the shop',
      say: 'It’ll run. Will it be <em>what they meant?</em>'
    },
    {
      name: 'loop', part: 'Part 2',
      kicker: 'Tonight’s loop',
      say: 'Slow down the thinking. <em>Speed up the building.</em>',
      flow: [['/grill-with-docs', 'agree what to build'], ['/to-spec', 'write it down'], ['/to-tickets', 'split it into tickets'], ['/implement', 'test first, then code review'], ['pr', 'the agent writes the PR'], ['/retro', 'make the next run better']]
    },
    {
      name: 'switch', part: 'Part 2', minutes: 5, qr: 'setup',
      kicker: 'Get the code',
      say: 'Switch to <em>Part 2</em>',
      sub: 'No copy yet? Scan, and tick <b>Include all branches</b>. Then switch, and run the setup skill once.',
      prompt: 'git stash -u\ngit fetch\ngit switch mash/part-2-new-features\n<b>/setup-matt-pocock-skills</b>'
    },
    {
      name: 'grill', part: 'Part 2', minutes: 12,
      kicker: 'Step 1 · Grill',
      say: 'Let it <em>interview you.</em>',
      prompt: '<b>/grill-with-docs</b> I want to add favourites to this shop: signed-in shoppers can save products and see them on a Favourites page. Keep each question short.',
      sub: 'Answer fast. If you don’t know, say what you’d guess. It writes the words you agree into <b>GLOSSARY.md</b>. Codex: <b>$grill-with-docs</b>.'
    },
    {
      name: 'spec', part: 'Part 2', minutes: 5,
      kicker: 'Step 2 · Spec and tickets',
      say: 'Write down what you <em>agreed.</em>',
      prompt: '<b>/to-spec</b>\n<b>/to-tickets</b>',
      sub: 'Same session as the grilling: don’t clear yet. Now there’s a record to build against and review against.'
    },
    {
      name: 'tdd', part: 'Part 2', minutes: 15,
      kicker: 'Step 3 · Test first',
      say: 'Red, <em>then green.</em>',
      prompt: '<b>/clear</b>\n<b>/implement</b> the smallest favourites ticket. Show me the failing test before you write the code.',
      sub: 'Fresh context for each ticket. A failing test proves the test can catch the problem.'
    },
    {
      name: 'review', part: 'Part 2', minutes: 8,
      kicker: 'Step 4 · Review',
      say: 'What could go wrong, and <em>which check catches it?</em>',
      prompt: 'Run the tests and show me the output. Then open a PR in my repo into mash/part-2-new-features using the PR template, and review it against <b>REVIEW.md</b>.',
      sub: 'The <b>pr</b> skill shapes the PR: a picture of the change, proof it works, and how risky it is to merge.'
    },
    {
      name: 'risk', part: 'Part 2',
      kicker: 'How Anthropic reviews agent code',
      say: 'Risk decides <em>who approves.</em>',
      tiers: [['Low', 'Docs, copy, behind a flag', '0 people'], ['Medium', 'Ordinary changes', '1 person'], ['High', 'Auth, checkout, CI', '2 people']]
    },
    {
      name: 'merge', part: 'Part 2', minutes: 5,
      kicker: 'Step 5 · Merge',
      say: 'You land it, <em>you own it.</em>',
      sub: 'Read the evidence, fix what matters, merge. Then <b>/retro</b>, in the same session, to make the next run better.'
    },

    // Wrap-up: "beyond today" from the handout, then questions and demos
    {
      name: 'beyond', part: 'Wrap-up',
      kicker: 'Beyond tonight',
      say: 'We went deep on a few. <em>Try these next.</em>',
      cards: [['/teach', 'Turns a part of the codebase you know into a guided lesson for someone else.'], ['/wayfinder', 'Plans work too big for one session as a shared map of tickets.']],
      poll: { q: 'Pick 1 to 3 things you’ll actually try this week.', multi: true, options: ['/teach on code I know well', '/grill-with-docs on a personal project', '/wayfinder on something too big for one sitting', 'Write a mini-skill of my own', 'Share this workshop with a teammate', 'Something else'] }
    },
    {
      name: 'qa', part: 'Q&A', qa: true, qr: 'live',
      kicker: 'Q&A',
      say: 'Your questions',
      sub: 'Ask on your phone and vote up the ones you want answered. Most votes first.'
    },
    {
      name: 'showtell', part: 'Demos', scenic: true, qr: 'slack',
      kicker: 'Show and tell',
      say: 'What did you build?',
      sub: 'Show us where you got to. Then keep the conversation going in the Perth AI Slack.',
      button: ['slack', 'Join the Perth AI Slack']
    }
  ],

  // Pages in docs/ are served next to live/, so links follow wherever the site is hosted.
  // Opened from disk, they point at the GitHub Pages copy instead.
  links: function () {
    var root = new URL('../', location.protocol === 'file:' ? 'https://perth-ai.github.io/workshop-mp-skills-for-ai-native-devs/live/' : location.href);
    return {
      live: new URL('live/', root).href,
      setup: root.href,
      skills: new URL('skills.html', root).href,
      issues: 'https://github.com/perth-ai/workshop-mp-skills-for-ai-native-devs/issues',
      slack: 'https://join.slack.com/t/perthai/shared_invite/zt-4em6mnqt0-q3FFgygYANQEkfUfNLiJ8g'
    };
  }
};
