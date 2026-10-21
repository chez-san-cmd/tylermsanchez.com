import re, pathlib
import os; S = pathlib.Path(os.environ.get("SITE_OUT", pathlib.Path(__file__).resolve().parent.parent)); S.mkdir(parents=True, exist_ok=True); (S/"writing").mkdir(exist_ok=True)
CSS = r"""
/* Layout: one 640px column, left-aligned, nav as a single line of text. Quiet enough that the writing is the design. */
:root{--bg:#F6F7F5;--fg:#15201E;--muted:#5F6E6A;--accent:#1F6F5F;--rule:#D9DEDB;--soft:#ECF0EE;--you:#B8336A;
  --f-body:"Newsreader","Iowan Old Style",Georgia,serif;--f-ui:"IBM Plex Sans",system-ui,-apple-system,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121716;--fg:#E6ECE9;--muted:#99A8A3;--accent:#5CC4A8;--rule:#2B3532;--soft:#1B2422;--you:#F07AA6;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121716;--fg:#E6ECE9;--muted:#99A8A3;--accent:#5CC4A8;--rule:#2B3532;--soft:#1B2422;--you:#F07AA6;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:19px;line-height:1.55;padding-block:0 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.col{max-width:640px;margin:0 auto}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
nav.top{font-family:var(--f-ui);font-size:15px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:baseline;padding:22px 0 36px;border-bottom:1px solid var(--rule);margin-bottom:36px}
nav.top .me{font-weight:600;color:var(--fg);margin-right:auto}
nav.top a[aria-current]{color:var(--fg);border-bottom:2px solid var(--accent)}
.preview{font-family:var(--f-ui);font-size:12.5px;color:var(--muted);background:var(--soft);border-radius:6px;padding:6px 10px;margin:0 0 20px;display:inline-block}
.me-photo{display:block;width:112px;height:112px;border-radius:12px;object-fit:cover;margin:0 0 20px}
h1{font-weight:500;font-size:36px;line-height:1.15;letter-spacing:-.01em;margin:0 0 14px;text-wrap:balance}
h2{font-family:var(--f-ui);font-weight:600;font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:44px 0 12px}
h3{font-weight:500;font-size:23px;margin:36px 0 8px;line-height:1.25;text-wrap:balance}
p{margin:0 0 18px;max-width:66ch}
.lede{font-size:22px;line-height:1.45;color:var(--fg)}
.contact{font-family:var(--f-ui);font-size:15px;display:flex;flex-wrap:wrap;gap:6px 16px;margin:0 0 8px}
.contact span{color:var(--muted)}
ul.list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
ul.list li{display:grid;grid-template-columns:72px 1fr;gap:14px;align-items:baseline}
ul.list .d{font-family:var(--f-mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
ul.list small{display:block;color:var(--muted);font-size:16px}
ul.plain{margin:0 0 18px;padding-left:22px}ul.plain li{margin-bottom:6px}
ol{padding-left:22px}ol li{margin-bottom:10px}
.meta{font-family:var(--f-ui);font-size:14px;color:var(--muted);margin:0 0 28px}
article h3{margin-top:40px}
blockquote{margin:0 0 18px;padding:0 0 0 18px;border-left:3px solid var(--rule);color:var(--fg)}
blockquote ul{padding-left:20px}
figure{margin:24px 0 8px;background:var(--soft);border:1px solid var(--rule);border-radius:10px;padding:14px;overflow-x:auto}
figure svg{display:block;width:100%;height:auto;min-width:560px;color:var(--fg);font-family:var(--f-ui)}
figcaption{margin-top:10px;font-family:var(--f-ui);font-size:14px;color:var(--muted)}
svg text{font-size:12px;fill:currentColor}svg .t{font-size:13px;font-weight:600}svg .s,svg .lab{font-size:11px;fill:var(--muted)}
svg .box{fill:var(--bg);stroke:currentColor;stroke-width:1.5}svg .store{fill:var(--bg);stroke:var(--accent);stroke-width:1.5}
svg .agent{fill:var(--bg);stroke:var(--muted);stroke-width:1.5;stroke-dasharray:5 3}svg .you{fill:var(--bg);stroke:var(--you);stroke-width:2}
svg .ext{fill:var(--soft);stroke:var(--rule);stroke-width:1}svg .edge{fill:none;stroke:currentColor;stroke-width:1.3}
svg .edge.a{stroke:var(--muted)}svg .edge.y{stroke:var(--you);stroke-width:1.8}svg .edge.d{stroke-dasharray:4 3}svg .gate{fill:none;stroke:var(--you);stroke-width:1.2;stroke-dasharray:3 3}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-family:var(--f-ui);font-size:13px;color:var(--muted);margin:0 0 8px}
.legend span{display:inline-flex;align-items:center;gap:6px}.legend i{display:inline-block;width:20px;height:11px;border-radius:3px;border:2px solid}
.year{margin:0 0 36px}.year h3{margin-top:0}
.pending{font-family:var(--f-ui);font-size:13px;color:var(--you);margin:0 0 8px}
footer{margin-top:64px;padding-top:18px;border-top:1px solid var(--rule);font-family:var(--f-ui);font-size:13.5px;color:var(--muted)}
hr{border:0;border-top:1px solid var(--rule);margin:36px 0}
@media (max-width:480px){body{font-size:18px}h1{font-size:30px}ul.list li{grid-template-columns:1fr}ul.list .d{order:2}}
"""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap">'
def nav(cur):
    items=[("index.html","Home","home"),("writing/chat-box.html","Writing","writing"),("index.html#projects","Projects","projects"),("how-i-work.html","How I work","how"),("reading.html","Reading","reading"),("years-in-review.html","Years in review","years")]
    out=[]
    for href,label,key in items:
        if key=="home": continue
        if cur.startswith("writing/"): href = "../"+href if not href.startswith("http") else href
        out.append(f'<a href="{href}"{" aria-current=\"page\"" if key==cur.split("/")[0].replace(".html","") or (key=="writing" and cur.startswith("writing/")) or (key=="how" and cur=="how-i-work.html") or (key=="years" and cur=="years-in-review.html") else ""}>{label}</a>')
    home = "../index.html" if cur.startswith("writing/") else "index.html"
    return f'<nav class="top"><a class="me" href="{home}">Tyler Sanchez</a>{"".join(out)}</nav>'
def page(cur, title, body, standalone=True):
    icon = '../' if cur.startswith('writing/') else ''
    head = f'<title>{title}</title><meta name="claude:viewport-fit-sides" content="cover"><link rel="icon" type="image/png" sizes="32x32" href="{icon}favicon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="{icon}icon-512.png"><link rel="apple-touch-icon" href="{icon}apple-touch-icon.png">{FONTS}<style>{CSS}</style>'
    if standalone:
        head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+head+'</head><body>'
        tail = '</body></html>'
    else:
        tail = ''
    return head + f'<div class="col">{nav(cur)}<span class="preview">Private preview · not yet at tylermsanchez.com · draft copy</span>{body}<footer>© 2026 Tyler Sanchez · Denver · tylersanchez@gmail.com</footer></div>' + tail

# ---------- Home ----------
home = """
<img class="me-photo" src="tyler.jpg" alt="Tyler Sanchez" width="112" height="112">
<h1>I'm Tyler Sanchez, a product manager in Denver. I'm building an assistant that runs my life in the background and only interrupts me for decisions.</h1>
<div class="contact"><span>tylersanchez@gmail.com</span><a href="https://www.linkedin.com/in/tylersanchez" target="_blank" rel="noopener">LinkedIn</a><a href="https://github.com/" target="_blank" rel="noopener">GitHub</a></div>

<h2>About</h2>
<p>I spent the last decade as a PM, mostly at Instagram, where my team worked on how new connections turn into conversations. The part of the job I love is learning a space, forming a point of view, and inventing the product that follows from it. Since leaving Meta I've been building that product for a customer of one: me. A set of agents now reads my inbox, watches job boards, tracks concert presales, runs the renovation paperwork, and brings me a short list of decisions each morning. I never let them send anything. I write about what that teaches me about where assistants are going.</p>
<p>Outside of work: 🍽️ cooking, ⚽ soccer, 🤖 ai, 🥾 hiking, 🎸 live music, 👨‍👧 dad things.</p>

<h2>Now <span style="text-transform:none;letter-spacing:0;font-weight:400">· October 2026</span></h2>
<p>Building in public through mid-December. This site, a first essay on the shape of a proactive assistant, and an open-source version of the Job Radar with the rubric and evals that make it work. Also talking to a few teams about short product-strategy engagements.</p>

<h2>Writing</h2>
<ul class="list">
  <li><span class="d">Oct 2026</span><span><a href="writing/chat-box.html">The assistant I wanted doesn't have a chat box</a><small>Three months with an assistant that works while I sleep, and what it taught me about the shape of the thing.</small></span></li>
  <li><span class="d">Soon</span><span>The assistant is already the front door<small>What happens to discovery when the assistant picks the gym.</small></span></li>
  <li><span class="d">Soon</span><span>Fetch, score, bring only the decisions<small>Open-sourcing the Job Radar and the evals behind it.</small></span></li>
</ul>

<h2 id="projects">Projects</h2>
<ul class="list">
  <li><span class="d">live</span><span><b>Command Center</b><small>One page for every open project in my life, with a strict attention hierarchy and a reply box that starts an agent run.</small></span></li>
  <li><span class="d">live</span><span><b>Job Radar</b><small>Daily fetch of PM postings from ~20 companies, scored against a written rubric. Open source in November.</small></span></li>
  <li><span class="d">live</span><span><b>Concert Radar</b><small>Presale alerts for the artists I'd actually buy tickets for, code included.</small></span></li>
  <li><span class="d">live</span><span><b>Purchase advisor</b><small>Pressure-tests whether to buy at all, then finds the best real value. Never buys.</small></span></li>
  <li><span class="d">next</span><span><b>HomeOS, Keep in Touch</b><small>The same loop for the house and for the people I'm bad at keeping up with.</small></span></li>
</ul>

<h2>Other stuff</h2>
<ul class="plain">
  <li><a href="how-i-work.html">How I work</a>: the principles, the system diagrams, and the tools</li>
  <li><a href="reading.html">Reading</a>: a short list of the books that shaped how I think about product, plus the full shelf</li>
  <li><a href="years-in-review.html">Years in review</a>: public excerpts from the annual letter I write to friends and family</li>
</ul>
"""
(S/"index.html").write_text(page("index.html","Tyler Sanchez",home,standalone=(os.environ.get("ARTIFACT_PREVIEW") is None)))

# ---------- Essay ----------
essay = """
<article>
<h1>The assistant I wanted doesn't have a chat box</h1>
<p class="meta">Draft · October 2026 · about 7 minutes</p>
<p class="lede">For the last three months I have had an assistant that works while I'm asleep. It isn't a person and it isn't an app I open. It is a handful of scheduled jobs that read my email, my calendar, a few job boards and a Notion workspace, and every morning it leaves me a short list: here are the three things only you can decide, here is what I already did about everything else. It is a personal assistant that gets a little more access each month, as trust builds.</p>
<p>I built it because I was between jobs and had the time, but the longer I run it the less it feels like a side project and the more it feels like the actual product. So this is the first of a few posts about what it is, how it works, and what I think it says about where AI assistants are going.</p>

<h3>The chat box is the wrong shape</h3>
<p>Every AI assistant I have used asks me to start. I open a window, I remember what I needed, I type it, I read the answer, I close the window. It is like having a very good reference librarian. But a reference librarian is not what I was missing. What I was missing was the colleague who notices that the presale for a band I like opens Thursday at 10, who already read the forty-message thread with the architect, who says "you have two decisions today and I prepped both."</p>
<p>The difference is who holds the initiative. In a chat box the human holds it, which means the assistant can only ever be as useful as my memory of what to ask. As anyone who is married can tell you, there is a world of difference between doing what your spouse asks and noticing that something needs doing and handling it before they have to ask. Just ask my wife which one she'd like more of. The assistant I wanted holds the initiative itself and hands it back to me only at the points where my judgment is required.</p>
<p>I don't think the chat box is wrong, exactly. It is a great starting interface, the way the command line was. But the parts of my life the assistant helps with don't change much from year to year: health, money, the house, work, the people I care about. Fixed categories want a fixed place on the screen, not a scrolling conversation. So the design question changed from "what should it answer?" to "what should it be allowed to do on its own, where exactly does it stop and wait for me, and what does the thing I look at every morning actually look like?"</p>

<h3>What it actually does</h3>
<p>Here is the current set, in the order I built it.</p>
<p><b>The Command Center.</b> A single page that shows every open project in my life as a tile in a fixed place, like a site plan, with one marker per item that needs something. The rule for the visual hierarchy is strict: a hard deadline, like a payment due, inside three days is the loudest thing on the page; things waiting on me glow softly; items the agents are working on recede; soft deadlines never turn red; fun projects, like a purchase advisor I'm building, live in their own quiet corner. If I only look at it for five seconds I should know whether anything is on fire and whether anything is mine.</p>
<p><b>The attention queue behind it.</b> Every item on the page answers two questions: is this on me or on the agent, and if it's on me, what kind of answer does it need. The agent can move an item into my column with a recommendation at the top and whatever it already prepared underneath. I can reply to any item right from the page, so the loop is: it prepares, I decide in one line, it carries on.</p>
<p><b>Project Books.</b> Every project, from a kitchen renovation to the job search to a dinner planner, gets one Notion page with the same four parts: a brief, a decision log, open questions, and a session log. An agent reads the book before it does anything and writes a line in the log when it finishes. This is also how I talk to it. Instead of returning to one ever-growing chat thread that eventually forgets its own beginning, I open a fresh conversation, point it at the book, and it has the latest context in a few seconds. Memory as a page you can read beats memory as a transcript you have to scroll.</p>
<p><b>Job Radar.</b> A script pulls every product management posting from about twenty companies I think are doing interesting work, every morning. A second job reads each posting against a rubric I wrote about what I actually want from the next role (room to originate bets weighs most, then level, then problem space), scores it 1 to 5, and writes anything worth a look into a table with a one-line "why" a recruiter could read. Anything that scores a 4 or 5 lands in my attention queue. I mark each one Interested or Not for me, sometimes with a note, and the rubric gets revised from my calls. It has been running since September and reads about a hundred postings a week so I don't have to. Every so often I review the roles it passed on, looking for false negatives. So far, none.</p>
<p><b>Smaller ones.</b> A morning brief. A weekly sweep of what fell through the cracks. The renovation paperwork: proposals, permit timelines, the vendor email that needs a reply. Concert presales for artists I'd buy tickets for, with the presale code sitting right on the tile. Not everything has to be useful.</p>

<h3>The rules it runs under</h3>
<p>The part I'm proudest of is not any one agent. It is the small set of rules they all obey, which is what makes me increasingly willing to let them run unattended:</p>
<ol>
<li><b>It never sends anything to another person.</b> It drafts the email, in my voice, and leaves it for me. I have had it draft a decline to a recruiter, a note to our architect, a message to our daycare. I read and send every one myself. This is the rule that makes everything else safe, because the blast radius is limited to a bad draft.</li>
<li><b>It never closes my decisions for me.</b> It makes recommendations. It cannot mark a job "Not for me" or tick something off my to-do list.</li>
<li><b>It never spends money.</b> It can pressure-test a purchase or comparison shop for the best price. The card stays in my wallet.</li>
<li><b>It writes down what it learned.</b> Each project has its book. And it watches the delta between the emails it drafts and the ones I actually send, so it sounds more like me over time. This might be the most useful feature of all.</li>
<li><b>It brings me decisions, not updates.</b> A status report is something I have to read. A decision with a recommendation at the top and the prep already done is something I can act on in thirty seconds.</li>
</ol>
<p>Those rules are the actual product. The scripts are replaceable.</p>

<h3>What surprised me</h3>
<p><b>The hard part is not the model. It is the rubric.</b> The scoring job got good the week I stopped describing jobs I'd like and started writing down what I was actually optimizing for, including the uncomfortable parts: pay floor, hours, how AI-native a team is. The model was fine from day one. My own clarity was the bottleneck. I suspect this is true of every "AI agent" anyone is building right now.</p>
<p><b>It is agile the way the manifesto meant it.</b> The Command Center has had something like a hundred changes since I started, and there are a hundred more I want. The pattern is always the same: I use it for a few days, something feels off, I describe the change, it ships in minutes, I use it for a few more days. Filters. Sorting. A checkbox to mark things done. Replying inline instead of switching apps. A rule that every recommendation leads with the answer and puts the evidence underneath, which is Barbara Minto's pyramid principle applied to a to-do list. No single change was the breakthrough. A thousand small tweaks were. For most of my career, getting a product in front of a user and iterating a hundred times in a few weeks was the thing we said we did. This is the first time it has been literally true.</p>
<p><b>Product taste is the scarce input.</b> Because building is cheap now, the time goes to deciding what should exist, where it should live on the screen, and what the agent should be allowed to touch. I have spent far more hours on what the morning page looks like than on any script behind it, and I think that ratio is right. The agent is only as good as the judgment about what to show me and when.</p>

<h3>Where this goes</h3>
<p>The obvious next version is one that runs the same loop for health, money, the house and the people I'm bad at keeping up with. I'm building those next and will write them up as they land. The Job Radar scaffold goes up on GitHub in a couple of weeks with the rubric and the evals I use to check the scoring, because the interesting part is not my code but the shape: fetch, score against a written point of view, bring only the decisions to a human.</p>
<p>There's a second thing I noticed along the way, about what happens to discovery when the assistant is the one choosing the gym, and it deserves its own post. Soon.</p>
<p>If you're building something in this shape, or run a team that should be, I'd like to compare notes. Email is at the top of the page.</p>
</article>
"""
(S/"writing/chat-box.html").write_text(page("writing/chat-box.html","The assistant I wanted doesn't have a chat box",essay))

# ---------- How I work ----------
src = (pathlib.Path(__file__).resolve().parent/"how-i-work-diagrams.html").read_text()
figs = re.findall(r"<h2>\d\. (.*?)</h2>\s*<p>(.*?)</p>\s*(<figure>.*?</figure>)", src, re.S)
how = """
<h1>How I work</h1>
<p class="lede">An assistant that runs in the background is only as trustworthy as the rules it runs under. Here are the rules, then the system that enforces them, then the tools.</p>

<h2 id="principles">Principles</h2>
<ol>
<li><b>It never sends anything to another person.</b> Drafts stay drafts until I send them.</li>
<li><b>It never closes my decisions for me.</b> It recommends; I mark done, decline, approve.</li>
<li><b>It never spends money.</b> It can comparison-shop and pressure-test a purchase. The card stays with me.</li>
<li><b>It writes down what it learned.</b> Every project has a book: brief, decisions, open questions, session log. The delta between what it drafts and what I send is how it learns my voice.</li>
<li><b>It brings me decisions, not updates.</b> Recommendation first, evidence underneath, prep already done.</li>
</ol>

<h2>The system</h2>
<div class="legend">
  <span><i style="border-color:var(--you)"></i> Me (decides, sends, buys)</span>
  <span><i style="border-color:var(--muted);border-style:dashed"></i> Scheduled Claude run</span>
  <span><i style="border-color:var(--accent)"></i> Notion, the system of record</span>
  <span><i style="border-color:var(--rule);background:var(--soft)"></i> Outside service</span>
</div>
"""
for title, para, fig in figs:
    how += f"<h3>{title}</h3><p>{para}</p>{fig}"
how += """
<h2>Tools</h2>
<ul class="plain">
<li><b>Claude</b> (Claude Code and its scheduled tasks) does the reading, drafting, scoring and filing. Every run starts from a written brief and ends with a log line.</li>
<li><b>Notion</b> is the system of record: the attention queue, one Project Book per project, and the radar tables. If it isn't in Notion, the agent doesn't know it.</li>
<li><b>GitHub Actions</b> runs the deterministic parts on a schedule, like the daily job fetch, and keeps the data as plain JSON in a repo.</li>
<li><b>Gmail, Google Calendar and Drive</b> are read through connectors. Drafts are written to Gmail; nothing is sent from there by an agent.</li>
<li><b>Spotify</b> supplies taste for the concert radar; venue newsletters supply the presale windows.</li>
<li><b>A single HTML page</b> is the Command Center: no framework, reads Notion live, and has been changed about a hundred times.</li>
</ul>
"""
(S/"how-i-work.html").write_text(page("how-i-work.html","How I work",how))

# ---------- Reading ----------
reading = """
<h1>Reading</h1>
<p class="lede">A short list of the books that shaped how I think about product, people and time, one line each. The full shelf, with ratings, is on <a href="https://www.goodreads.com/user/show/16104684-tyler" target="_blank" rel="noopener">Goodreads</a>.</p>
<p class="pending">Pending: Tyler picks 10 to 15 titles. The layout below shows the format.</p>
<ul class="list">
  <li><span class="d">2026</span><span><b>AGI Chronicles</b>, Kevin Roose<small>Most recently finished. One line on why it stuck.</small></span></li>
  <li><span class="d">—</span><span><b>Title</b>, Author<small>One line on what it changed.</small></span></li>
  <li><span class="d">—</span><span><b>Title</b>, Author<small>One line on what it changed.</small></span></li>
</ul>
"""
(S/"reading.html").write_text(page("reading.html","Reading",reading))

# ---------- Years in review ----------
years = """
<h1>Years in review</h1>
<p class="lede">Every December I write a long letter to friends and family with the same three sections: what went well, what could have gone better, and what I'm focusing on next year. The full letters stay with the people they're written for. These are short public excerpts.</p>
<p class="pending">Pending your approval: these are Claude's default picks (2023-B, 2024-A, 2025-A). Swap any of them from the candidates page in Notion.</p>

<div class="year">
<h3>2025 · Presence over productivity</h3>
<p class="meta">From "Focus for 2026: Work, held lightly"</p>
<blockquote><p>My job requires me to mentally live in the future — anticipating risks, planning what we'll build next, preparing for when my engineers free up, and constantly tracking whether we're on pace to hit our goals. I'm good at that kind of thinking, but it doesn't turn off easily, and it's started bleeding into the rest of my life making it harder to be present for the ordinary, fleeting moments of raising a child who only lives in the now.</p>
<p>In 2026, I want to <b>hold work more lightly</b> — not by disengaging, but by limiting how much I engage. Showing up fully during the day, then letting it recede instead of mentally carrying it with me at all times. As my good friend David likes to say, I need to treat work a little more like <i>Severance</i>: be "on" while I'm there, then mentally clock out when the day ends. Practically, this means clearer boundaries, fewer self-imposed commitments, and a more tempered relationship with ambition — stay engaged, do good work, but don't grind for promotion at the expense of energy, presence, and family life.</p></blockquote>
</div>

<div class="year">
<h3>2024 · Four family trips, a solo hike, and a new inflection point</h3>
<p class="meta">From "Sanchez family trips"</p>
<blockquote><p>In October, Claire and I traveled with my parents to visit the Grand Canyon and Las Vegas. It was the first time any of us (except Claire) had seen the Grand Canyon and the first time in Vegas for my parents. What made this trip particularly special for me, aside from the fact that it was the first time Claire and I had taken a trip with my parents, was that Claire and I largely planned the entire trip and were able to give my parents an experience they might not have found otherwise. From choosing to stay inside the park in the Grand Canyon and enjoy spectacular sunsets and the Milky Way at night, to a "best of the best" experience in Vegas that included a close up magic show, front and center tickets to "O" Cirque du Soleil's famed water show, to the Bacchanal Brunch at Caesar's which features over 250 dishes (and unlimited crab legs). It was truly a trip that I'll never forget.</p></blockquote>
</div>

<div class="year">
<h3>2023 · Balance, restlessness, and the case for spontaneous friends</h3>
<p class="meta">From "Focus for 2024: Activities are better with friends"</p>
<blockquote><p>I have a former teammate who moved back to Spain last year after spending a few years in the US with his family. He always lamented the culture around making plans weeks in advance. Compared to Spain, where he might run into a few friends on his way to a wine bar and convince them to join, social hangs in the US are never spontaneous. There's a lot to unpack there, but the idea that there are probably more unplanned things we can do together deeply resonated.</p>
<p>Given that almost all activities are better with friends, I want to try to make a concerted effort this year to invite friends to more casual hangs:</p>
<ul><li>Going for a run? Want to run together?</li><li>Drink coffee? Let's meet at a coffee shop.</li><li>Hungry? Come on over and we'll cook for a low-key dinner.</li><li>I'm going to walk Sully in Wash Park, want to walk with me?</li></ul>
<p>This is going to be a <b>bit of an experiment</b> and it may not work for certain activities (<i>"want to come over and read in silence together?!"</i>), but I am excited to try and spend more time together with friends. [Note to Denver friends: you will not hurt my feelings if you decline an invitation to run an errand with me at Costco. You will just be hurting yourself by not getting access to the free samples.]</p></blockquote>
<p class="meta">The experiment mostly failed in 2024 (my fault; I didn't extend the invites) and came back in 2025 as "low friction connection."</p>
</div>
"""
(S/"years-in-review.html").write_text(page("years-in-review.html","Years in review",years))
print("ok", [p.name for p in S.rglob("*.html")], "figs:", len(figs))
