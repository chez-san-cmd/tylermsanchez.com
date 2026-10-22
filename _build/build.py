import re, pathlib
import os; S = pathlib.Path(os.environ.get("SITE_OUT", pathlib.Path(__file__).resolve().parent.parent)); S.mkdir(parents=True, exist_ok=True); (S/"writing").mkdir(exist_ok=True); (S/"projects").mkdir(exist_ok=True)
CSS = r"""
/* Layout: one 640px column, left-aligned, nav as a single line of text. Quiet enough that the writing is the design. */
:root{--bg:#F6F7F5;--fg:#15201E;--muted:#5F6E6A;--accent:#0F6E63;--ul:#8FC9BC;--rule:#D9DEDB;--soft:#ECF0EE;--you:#B8336A;
  --f-body:"Newsreader","Iowan Old Style",Georgia,serif;--f-ui:"IBM Plex Sans",system-ui,-apple-system,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121716;--fg:#E6ECE9;--muted:#99A8A3;--accent:#5CC4A8;--ul:#2F6B5E;--rule:#2B3532;--soft:#1B2422;--you:#F07AA6;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121716;--fg:#E6ECE9;--muted:#99A8A3;--accent:#5CC4A8;--ul:#2F6B5E;--rule:#2B3532;--soft:#1B2422;--you:#F07AA6;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:20px;line-height:1.55;padding-block:0 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.col{max-width:640px;margin:0 auto}
a{color:var(--accent);text-decoration:underline;text-decoration-color:var(--ul);text-decoration-thickness:1.5px;text-underline-offset:3px}a:hover{text-decoration-color:var(--accent)}
nav.top a,.contact a,.toc a,.books a{text-decoration:none}nav.top a:hover,.contact a:hover,.toc a:hover,.books a:hover{text-decoration:underline;text-decoration-color:var(--accent)}
nav.top{font-family:var(--f-ui);font-size:16px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--rule);margin-bottom:36px}
nav.top .me{font-weight:600;color:var(--fg);margin-right:auto}
nav.top a[aria-current]{color:var(--fg);border-bottom:2px solid var(--accent)}
.me-photo{display:block;width:150px;height:150px;border-radius:12px;object-fit:cover;margin:0 0 20px}
h1{font-weight:500;font-size:36px;line-height:1.15;letter-spacing:-.01em;margin:0 0 14px;text-wrap:balance}
h2{font-family:var(--f-ui);font-weight:600;font-size:16px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:44px 0 12px}
h3{font-weight:500;font-size:23px;margin:36px 0 8px;line-height:1.25;text-wrap:balance}
p{margin:0 0 18px;max-width:66ch}
.sub{font-size:28px;line-height:1.3;font-weight:400;letter-spacing:-.005em;margin:0 0 18px;text-wrap:balance}
.lede{font-size:22px;line-height:1.45;color:var(--fg)}
.contact{font-family:var(--f-ui);font-size:15px;display:flex;flex-wrap:wrap;gap:6px 16px;margin:0 0 8px}
.contact a{display:inline-flex;align-items:center;gap:6px}.contact .ic{width:16px;height:16px;flex:none}
ul.list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
ul.list li{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:baseline}
ul.list .d{font-family:var(--f-mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
ul.list small{display:block;color:var(--muted);font-size:19px;line-height:1.45;margin-top:2px}
ul.list li>span:last-child>a,ul.list li>span:last-child>b{font-size:22px;font-weight:400;line-height:1.3;color:var(--fg)}ul.list li>span:last-child>a{text-decoration:underline;text-decoration-color:var(--ul);text-decoration-thickness:1.5px;text-underline-offset:3px}ul.list li>span:last-child>a:hover{text-decoration-color:var(--accent)}
ul.plain{margin:0 0 18px;padding-left:22px}ul.plain li{margin-bottom:6px}
ul.other a{font-weight:600}
ol{padding-left:22px}ol li{margin-bottom:10px}
.toc{font-family:var(--f-ui);font-size:15px;display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 8px}.toc a::before{content:"↓ ";color:var(--muted)}
.books{list-style:none;margin:0 0 28px;padding:0}.books li{margin:0 0 6px;font-size:18px}.books .au{color:var(--muted)}.books .star{font-size:14px;margin-left:4px}.count{font-weight:400;letter-spacing:0;text-transform:none}
.meta{font-family:var(--f-ui);font-size:14px;color:var(--muted);margin:0 0 28px}
article h3{margin-top:40px}
blockquote{margin:0 0 18px;padding:0 0 0 18px;border-left:3px solid var(--rule);color:var(--fg)}
blockquote ul{padding-left:20px}
figure{cursor:zoom-in;margin:24px 0 8px;background:var(--soft);border:1px solid var(--rule);border-radius:10px;padding:14px;overflow-x:auto}
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
dialog.lb{border:0;padding:16px;background:var(--bg);color:var(--fg);border-radius:12px;max-width:min(96vw,1400px);width:auto;cursor:zoom-out}dialog.lb::backdrop{background:rgba(0,0,0,.55)}dialog.lb svg{display:block;width:min(92vw,1360px);height:auto;color:var(--fg);font-family:var(--f-ui)}dialog.lb p{font-family:var(--f-ui);font-size:14px;color:var(--muted);margin:10px 0 0}
hr{border:0;border-top:1px solid var(--rule);margin:36px 0}
@media (max-width:480px){nav.top{flex-wrap:nowrap;white-space:nowrap;gap:0 12px;font-size:15px}nav.top .me{margin-right:auto}body{font-size:19px}h1{font-size:30px}.sub{font-size:23px}ul.list li{grid-template-columns:1fr}ul.list .d{order:2}}
"""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap">'
def nav(cur):
    items=[("index.html","Home","home"),("writing/chat-box.html","Writing","writing"),("projects.html","Projects","projects"),("how-i-work.html","AI System","how")]
    out=[]
    for href,label,key in items:
        if key=="home": continue
        if cur.startswith("writing/") or cur.startswith("projects/"): href = "../"+href if not href.startswith("http") else href
        out.append(f'<a href="{href}"{" aria-current=\"page\"" if key==cur.split("/")[0].replace(".html","") or (key=="writing" and cur.startswith("writing/")) or (key=="projects" and cur.startswith("projects/")) or (key=="how" and cur=="how-i-work.html") or (key=="years" and cur=="years-in-review.html") else ""}>{label}</a>')
    home = "../index.html" if (cur.startswith("writing/") or cur.startswith("projects/")) else "index.html"
    return f'<nav class="top"><a class="me" href="{home}">Tyler Sanchez</a>{"".join(out)}</nav>'
LIGHTBOX = """<dialog class="lb" id="lb"><div id="lb-body"></div><p>Click anywhere or press Esc to close.</p></dialog>
<script>
(function(){var d=document.getElementById('lb'),b=document.getElementById('lb-body');
document.querySelectorAll('figure').forEach(function(f){f.setAttribute('title','Click to enlarge');f.addEventListener('click',function(){var s=f.querySelector('svg');if(!s)return;b.innerHTML='';b.appendChild(s.cloneNode(true));d.showModal();});});
d.addEventListener('click',function(){d.close();});})();
</script>
"""
def page(cur, title, body, standalone=True):
    icon = '../' if (cur.startswith('writing/') or cur.startswith('projects/')) else ''
    head = f'<title>{title}</title><meta name="claude:viewport-fit-sides" content="cover"><link rel="icon" type="image/png" sizes="32x32" href="{icon}favicon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="{icon}icon-512.png"><link rel="apple-touch-icon" href="{icon}apple-touch-icon.png">{FONTS}<style>{CSS}</style>'
    if standalone:
        head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+head+'</head><body>'
        tail = '</body></html>'
    else:
        tail = ''
    lb = LIGHTBOX if '<figure' in body else ''
    return head + f'<div class="col">{nav(cur)}{body}<footer>© 2026 Tyler Sanchez · Denver · tylersanchez@gmail.com</footer></div>{lb}' + tail

# ---------- Projects data ----------
# status: live | building | on deck.  slug=None means no page yet.
PROJECTS = [
  dict(slug="command-center", name="Command Center", status="live",
       blurb="One page for every open project in my life, with a strict attention hierarchy and a reply box that starts an agent run."),
  dict(slug="job-radar", name="Job Radar", status="live",
       blurb="Daily fetch of PM postings from ~20 companies, scored against a written rubric. Open source in November."),
  dict(slug="concert-radar", name="Concert Radar", status="live",
       blurb="Presale alerts for the artists I'd actually buy tickets for, code included."),
  dict(slug="purchase-advisor", name="Purchase advisor", status="live",
       blurb="Pressure-tests whether to buy at all, then finds the best real value. Never buys."),
  dict(slug=None, name="What's for Dinner", status="building",
       blurb="Easy weeknight dinners, planned around what's already in the fridge and what's on sale, with the grocery list done."),
]
def project_list(cur):
    pre = "" if cur in ("index.html","projects.html") else "../"
    out = ['<ul class="list">']
    for p_ in PROJECTS:
        title = f'<a href="{pre}projects/{p_["slug"]}.html">{p_["name"]}</a>' if p_["slug"] else f'<b>{p_["name"]}</b>'
        out.append(f'  <li><span class="d">{p_["status"]}</span><span>{title}<small>{p_["blurb"]}</small></span></li>')
    out.append('</ul>')
    return "\n".join(out)

# ---------- Home ----------
home = """
<img class="me-photo" src="tyler.jpg" alt="Tyler Sanchez" width="150" height="150">
<h1>👋 Hi, I'm Tyler, a Product Manager in Denver.</h1>
<p class="sub">I'm building an AI assistant that runs my life in the background and only interrupts me for decisions.</p>
<div class="contact"><a href="mailto:tylersanchez@gmail.com"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M3.5 5.5h17a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1h-17a1 1 0 0 1-1-1v-11a1 1 0 0 1 1-1z"/><path fill="none" stroke="currentColor" stroke-width="1.8" d="m3 7 9 6.5L21 7"/></svg>Email</a><a href="https://www.linkedin.com/in/tylermsanchez" target="_blank" rel="noopener"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A66C2" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>LinkedIn</a><a href="https://github.com/chez-san-cmd" target="_blank" rel="noopener"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="var(--fg)" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3z"/></svg>GitHub</a></div>

<h2>About</h2>
<p>I spent the last decade as a PM, mostly at Instagram, where my team worked on how new connections turn into conversations. The part of the job I love is learning a space, forming a point of view, and inventing the product that follows from it.</p>
<p>Since leaving Meta I've been building that product for a customer of one: me. A set of agents now reads my inbox, watches job boards, tracks concert presales, runs the renovation paperwork, and brings me a short list of decisions each morning. I never let them send anything. I write about what that teaches me about where assistants are going.</p>
<p>Outside of work: 🍽️ cooking, 📚 <a href="reading.html">reading</a>, ⚽ soccer, 🤖 ai, 🥾 hiking, 🎸 live music, 👨‍👧 dad things.</p>

<h2>Now <span style="text-transform:none;letter-spacing:0;font-weight:400">· October 2026</span></h2>
<p>Building in public through mid-December. This site, a first essay on the shape of a proactive assistant, and an open-source version of the Job Radar with the rubric and evals that make it work. Also talking to a few teams about short product-strategy engagements.</p>

<h2>Writing</h2>
<ul class="list">
  <li><span class="d">Oct 2026</span><span><a href="writing/chat-box.html">The assistant I wanted doesn't have a chat box</a><small>Three months with an assistant that works while I sleep, and what it taught me about the shape of the thing.</small></span></li>
  <li><span class="d">Coming soon</span><span><b>The assistant is already the front door</b><small>What happens to discovery when the assistant picks the gym.</small></span></li>
  <li><span class="d">Coming soon</span><span><b>Fetch, score, bring only the decisions</b><small>Open-sourcing the Job Radar and the evals behind it.</small></span></li>
</ul>

<h2 id="projects">AI Projects</h2>
"""+project_list("index.html")+"""

<h2>Other stuff</h2>
<ul class="plain other">
  <li><a href="how-i-work.html">How I work with AI</a>: the principles, the system diagrams, and the tools</li>
  <li><a href="reading.html">Reading list</a>: everything I've read, by year, with the five-star books marked</li>
</ul>
"""
(S/"index.html").write_text(page("index.html","Tyler Sanchez",home,standalone=(os.environ.get("ARTIFACT_PREVIEW") is None)))

# ---------- Projects index ----------
projects_index = """
<h1>AI Projects</h1>
<p class="lede">The agents that run my life in the background, one page each: what it does, why it exists, how it's built, and what I learned. The rules they all run under are on <a href="how-i-work.html">How I work with AI</a>.</p>
""" + project_list("projects.html")
(S/"projects.html").write_text(page("projects.html","AI Projects",projects_index))

def project_page(slug, name, status, lede, what, why, how_built, learned, status_text, fig=None, repo=None):
    """Shared template: What · Why · How it's built · What I learned · Status."""
    toc = '<nav class="toc" aria-label="On this page"><a href="#what">What it does</a><a href="#why">Why I built it</a><a href="#how">How it\'s built</a><a href="#learned">What I learned</a><a href="#status">Status</a></nav>'
    repo_line = f'<p class="meta">The code, prompts and evals are on GitHub: <a href="{repo}" target="_blank" rel="noopener">{repo.replace("https://","")}</a>. The README has the implementation details this page leaves out.</p>' if repo else ''
    body = f"""
<p class="meta" style="margin-bottom:6px"><a href="../projects.html">AI Projects</a> · {status}</p>
<h1>{name}</h1>
<p class="lede">{lede}</p>
{toc}
<h2 id="what">What it does</h2>
{what}
<h2 id="why">Why I built it</h2>
{why}
<h2 id="how">How it's built</h2>
{fig or ''}
{how_built}
{repo_line}
<h2 id="learned">What I learned</h2>
{learned}
<h2 id="status">Status <span class="count">· October 2026</span></h2>
{status_text}
<p class="meta"><a href="../projects.html">← All projects</a></p>
"""
    (S/"projects"/f"{slug}.html").write_text(page(f"projects/{slug}.html", f"{name} · Tyler Sanchez", body))

src = (pathlib.Path(__file__).resolve().parent/"how-i-work-diagrams.html").read_text()
figs = re.findall(r"<h2>\d\. (.*?)</h2>\s*<p>(.*?)</p>\s*(<figure>.*?</figure>)", src, re.S)

# ---------- Project: Job Radar ----------
JR_REPO = "https://github.com/chez-san-cmd/job-radar"
project_page("job-radar", "Job Radar", "live",
  lede="Every morning a script pulls every product-management posting from 23 companies I'd consider working for, and a Claude run scores each one against a rubric I wrote about what I actually want. I see only the ones worth a look.",
  what="""
<p>Two jobs a day. Around 5am Denver time a GitHub Action fetches the PM postings from each company's own job board and commits the day's new ones to a repo. At 6:52am a scheduled Claude task reads each new posting in full, scores it 1 to 5 against the rubric, and writes anything scoring 3 or above to a Notion table with a one-line "why" a recruiter could read. Anything that scores a 4 or 5 also lands in my attention queue the same day; everything else waits for a Sunday review item that lists the week.</p>
<p>I mark each row <i>Interested</i> or <i>Not for me</i>, sometimes with a note. The notes get folded back into the rubric, so the scoring drifts toward my actual judgment rather than my first description of it. It has been running since October 5 and reads about a hundred postings a week so I don't have to.</p>
""",
  why="""
<p>I'm planning a year away from full-time work, and the plan assumes the main levers for the next job are people and stories, not applications. But a rare ideal role can appear at any time, and I didn't want to spend an hour a week scanning career pages to catch it. The Radar is a passive net: it watches, I decide. It also turned out to be the cleanest small example of the shape I think most useful agents will take: fetch on a schedule, score against a written point of view, bring only the decisions to a human.</p>
""",
  fig=figs[2][2],
  how_built="""
<ul class="plain">
<li><b>Fetch.</b> A private repo with one adapter per job-board platform: Greenhouse, Lever, Ashby, Rippling, Workday (Zillow), Eightfold (Netflix), and a scraper for Shopify, which publishes no feed. A GitHub Action runs the fetch daily and commits new postings as plain JSON, so the history is a git log. Why GitHub Actions: scheduled Claude runs can't open arbitrary websites without a per-URL approval nobody is there to give. Splitting deterministic fetching from judgment-heavy scoring solved that and made each half easier to test.</li>
<li><b>Score.</b> A Claude scheduled task reads the day's file and <code>RUBRIC.md</code>. The rubric scores first on latitude to originate product bets, then level, then problem space. Later rules came straight from my notes on real postings: AI-native teams weigh heavily, "traffic cop" seats on shared surfaces cap at 3, fixed in-office days outside Denver cap at 3 but are still shown, and location is a flag rather than a filter. Director and head-of-product titles are scored on strategy ownership instead of being passed on title.</li>
<li><b>Store and show.</b> One Notion database: role, company, fit, score, why, status, my notes, level signal, location, link. A saved view feeds a tile on my Command Center map and the Sunday review. Everything reads through saved views because Notion's row-query API has a workspace quota and views don't.</li>
<li><b>Learn.</b> Daily runs also read the <i>Maybe</i> rows and my notes, and periodic re-scores check the passes for false negatives. So far, none.</li>
</ul>
""",
  repo=JR_REPO,
  learned="""
<p><b>The hard part is not the model. It is the rubric.</b> The scoring got good the week I stopped describing jobs I'd like and started writing down what I was actually optimizing for, including the uncomfortable parts: pay floor, hours, how AI-native a team is. The model was fine from day one. My own clarity was the bottleneck.</p>
<p><b>Flags beat filters.</b> My first instinct was to filter out roles in other cities. Keeping them visible as a capped score instead leaves room for the conversation I actually want to have, which is whether the role could be rescoped to remote.</p>
<p><b>Some boards don't move.</b> Shopify's careers page is one evergreen posting, so the Radar will almost never show anything new there. For companies like that, a person on the inside matters more than a feed.</p>
<p><b>Scheduling is the flaky part.</b> GitHub's cron has run hours late, so scoring sometimes ran before the day's fetch landed. The fix (start scoring when the fetch finishes, not at a fixed time) is the kind of plumbing that takes more of the week than any prompt.</p>
""",
  status_text=f"""
<p>Live since October 5, 2026. Watching 23 companies. A cleaned-up public version, with the fetch adapters, a <code>RUBRIC.md</code> template and the evals I use to check the scoring, goes up on GitHub in mid-November with a Show HN post. Until then the repo is private; the link above will go live when it does.</p>
""")


# ---------- Project: Command Center ----------
CC_FIG = """<figure>
<svg viewBox="0 0 900 420" role="img" aria-label="Tyler reads one Command Center page laid out like a site plan: one tile per project, one marker per item that needs him, a reply box on each. The page reads the Notion Attention Queue through a saved view every 15 minutes. Twice a day, and whenever Tyler replies from the page, a scheduled Claude run checks Gmail and the to-do list, reads the project's book, works up to four queued items, and writes one queue item per decision with the prep and a recommendation attached.">
<defs>
<marker id="ar6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker>
<marker id="ara6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:var(--muted)"/></marker>
<marker id="ary6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:var(--you)"/></marker>
</defs>
<!-- Tyler -->
<rect class="you" x="20" y="60" width="180" height="64" rx="8"/>
<text class="t" x="110" y="86" text-anchor="middle">Tyler</text>
<text class="s" x="110" y="104" text-anchor="middle">5-second read · one-line reply</text>
<!-- The page -->
<rect class="box" x="230" y="30" width="330" height="190" rx="8"/>
<text class="t" x="395" y="54" text-anchor="middle">Command Center page (one HTML file)</text>
<rect class="box" x="246" y="68" width="84" height="46" rx="5"/><text class="s" x="288" y="88" text-anchor="middle">Albion</text><circle cx="320" cy="76" r="5" style="fill:var(--you)"/>
<rect class="box" x="338" y="68" width="84" height="46" rx="5"/><text class="s" x="380" y="88" text-anchor="middle">Return to Work</text><circle cx="412" cy="76" r="5" style="fill:var(--you)"/>
<rect class="box" x="430" y="68" width="84" height="46" rx="5"/><text class="s" x="472" y="88" text-anchor="middle">Health Plan</text>
<rect class="box" x="246" y="122" width="84" height="46" rx="5"/><text class="s" x="288" y="142" text-anchor="middle">Estate</text>
<rect class="box" x="338" y="122" width="84" height="46" rx="5"/><text class="s" x="380" y="142" text-anchor="middle">Job Radar</text>
<rect class="ext" x="430" y="122" width="84" height="46" rx="5"/><text class="s" x="472" y="142" text-anchor="middle">Fun yard</text>
<text class="s" x="246" y="190">tile per project · marker per item · reply box per card</text>
<text class="s" x="246" y="206">🚨 hard deadline inside 3 days · ⚪ soft dates slip, never red</text>
<!-- Notion -->
<rect class="store" x="230" y="270" width="330" height="120" rx="8"/>
<text class="t" x="395" y="294" text-anchor="middle">Notion · Attention Queue</text>
<text x="246" y="318">Item · Project · Ask (Decide / Approve / Context / Do)</text>
<text x="246" y="338">Status · Deadline (Hard / Soft) · Due · Urgency</text>
<text x="246" y="358">Prepared · Recommendation · Link</text>
<text class="s" x="246" y="378">+ one Project Book per project</text>
<!-- Claude run -->
<rect class="agent" x="620" y="150" width="250" height="110" rx="8"/>
<text class="t" x="745" y="176" text-anchor="middle">Queue run (scheduled Claude)</text>
<text class="s" x="745" y="194" text-anchor="middle">7:53am · 3:53pm · or when a reply arrives</text>
<text class="s" x="745" y="212" text-anchor="middle">1 check inbox  2 read the book</text>
<text class="s" x="745" y="228" text-anchor="middle">3 work ≤4 items to the human-only step</text>
<text class="s" x="745" y="244" text-anchor="middle">4 write one queue item per decision</text>
<!-- outside -->
<rect class="ext" x="620" y="330" width="76" height="34" rx="6"/><text x="658" y="351" text-anchor="middle">Gmail</text>
<rect class="ext" x="704" y="330" width="76" height="34" rx="6"/><text x="742" y="351" text-anchor="middle">Calendar</text>
<rect class="ext" x="788" y="330" width="82" height="34" rx="6"/><text x="829" y="351" text-anchor="middle">To-Do list</text>
<!-- edges -->
<path class="edge y" d="M200 92 L230 92" marker-end="url(#ary6)"/>
<path class="edge" d="M395 220 L395 270" marker-end="url(#ar6)" marker-start="url(#ar6)"/>
<text class="lab" x="405" y="250">saved view, every 15 min</text>
<path class="edge y" d="M560 100 L745 100 L745 150" marker-end="url(#ary6)"/>
<text class="lab" x="572" y="92">reply box → starts a run now</text>
<path class="edge a" d="M620 240 L560 290" marker-end="url(#ara6)"/>
<text class="lab" x="600" y="282">writes items + recommendation</text>
<path class="edge a d" d="M560 350 L620 258" marker-end="url(#ara6)"/>
<text class="lab" x="570" y="372">reads the book first</text>
<path class="edge a d" d="M745 330 L745 260" marker-end="url(#ara6)"/>
<path class="edge a d" d="M658 330 L690 260"/><path class="edge a d" d="M829 330 L800 260"/>
<text class="lab" x="752" y="300">read; drafts only</text>
<!-- gate -->
<rect class="gate" x="12" y="150" width="196" height="60" rx="8"/>
<text class="s" x="110" y="172" text-anchor="middle" style="fill:var(--you)">Human gate</text>
<text class="s" x="110" y="188" text-anchor="middle">nothing sent · nothing bought</text>
<text class="s" x="110" y="202" text-anchor="middle">to-dos never checked off for me</text>
</svg>
<figcaption>A site plan, not a feed: fixed tiles, one marker per open item, and a reply box that starts the next run. The queue is a Notion table; the page is one HTML file that reads it.</figcaption>
</figure>"""
project_page("command-center", "Command Center", "live",
  lede="One page that shows every open project in my life as a tile in a fixed place, with one marker per item that needs me. Agents do the work; I approve, decide, and supply context. If I look at it for five seconds I should know whether anything is on fire and whether anything is mine.",
  what="""
<p>Underneath the page is one Notion table, the Attention Queue: one row per thing waiting on me, across every project. Each row says which project it belongs to, what kind of answer it needs (<i>Decide</i>, <i>Approve</i>, <i>Context</i>, or <i>Do</i>), whether the deadline is hard or soft, what the agent already prepared, and what it recommends. Every agent run in my life ends by writing to this table.</p>
<p>Twice a day, at 7:53am and 3:53pm, a scheduled Claude run works the queue: it checks my inbox for replies before trusting the queue, sweeps my to-do list for anything tagged for it, reads the relevant Project Book, takes up to four items as far as an agent is allowed to, and sends me a short phone summary. The page itself refreshes from Notion every fifteen minutes. Each item card has a reply box; sending a line saves it as a comment on the item and starts a run immediately, so I get an answer in minutes rather than at the next scheduled run. A "Mark done" checkbox writes back to Notion. That's the whole interface.</p>
""",
  why="""
<p>Every AI assistant I'd used asked me to start. I open a window, remember what I needed, type it, read the answer. What I was missing was the colleague who notices the presale opens Thursday at 10, who already read the forty-message thread with the architect, who says "you have two decisions today and I prepped both." That colleague holds the initiative and hands it back only where my judgment is required.</p>
<p>The parts of my life it helps with don't change much from year to year: health, money, the house, work, the people I care about. Fixed categories want a fixed place on the screen, not a scrolling conversation. So the page is laid out like a site plan. I'm a visual person, and I wanted to see progress and what needs me across every project at once.</p>
""",
  fig=CC_FIG,
  how_built="""
<ul class="plain">
<li><b>The record is Notion.</b> An Attention Queue database plus one Project Book page per project (brief, decision log, open questions, session log). Notion is the system of record because it's the one tool both I and the agents can read and edit, and it works on my phone. If it isn't in Notion, the agent doesn't know it.</li>
<li><b>The page is one HTML file.</b> No framework. It reads the queue through the Notion connector and draws projects as plots and items as markers. It reads a saved view rather than querying rows, because Notion's row queries have a workspace quota that the first version exhausted in a day; views don't.</li>
<li><b>The attention hierarchy is a formula.</b> Every item has a Hard or Soft deadline and a due date; a Notion formula turns that into an urgency. Hard items go 🚨 Critical inside three days, 🔴 Urgent at four to seven, 🟠 Coming up at eight to fourteen, 🟢 Calm beyond. Soft items never turn red; past due they show ⚪ Slipped and the next run proposes a new date instead of nagging. When anything is Critical, the phone summary leads with it even if nothing else changed. Fun projects live in their own yard with no dates, no colors, and no alerts.</li>
<li><b>Runs follow a written protocol.</b> Inbox before queue. Read the book before acting. Stop at the human-only step: deciding, signing, sending in my name, moving money, conversations with family. Write one queue item per decision with a recommendation at the top and the prep underneath. Drafts are written in my voice from a saved style profile, and when I edit a draft before sending, the run compares the two and offers to update the profile. Every run ends by logging what it learned to the book; changes to decisions or preferences are gated behind one item I answer with "go."</li>
<li><b>Two rules I'd keep if I threw everything else out.</b> The one-minute rule: if an item takes me longer than a minute to act on, the agent didn't finish its prep, and it goes back. And batching: a few items per project per day, never a stream of pings.</li>
</ul>
<p class="meta">There's no public repo for the Command Center because the page is wired to my own Notion workspace and holds personal data. The pieces that generalize, the loop and the Project Books memory model, are on <a href="../how-i-work.html">How I work with AI</a>, and a longer write-up is coming in late November.</p>
""",
  learned="""
<p><b>It's agile the way the manifesto meant it.</b> The page has had something like a hundred changes since the end of September, and the pattern is always the same: I use it for a few days, something feels off, I describe the change, it ships in minutes. Filters. Sorting. A checkbox. Replying inline. A rule that every recommendation leads with the answer. No single change was the breakthrough; a thousand small tweaks were. For most of my career, iterating a hundred times in a few weeks was something we said we did. This is the first time it has been literally true.</p>
<p><b>Product taste is the scarce input.</b> Building is cheap now, so the hours go to deciding what should exist, where it lives on the screen, and what the agent may touch. I've spent far more time on what the morning page looks like than on any script behind it, and I think that ratio is right.</p>
<p><b>Check the inbox before trusting the queue.</b> The very first run worked a queue that was already behind my email. Every run now starts with Gmail.</p>
<p><b>Gating stops drift.</b> Early on, the agent's recommendations kept getting logged as my decisions. Now anything that changes a decision, a preference or a brief waits behind a single approval item. Memory is a page I can read, not a transcript I have to scroll, and I want to be the one who edits it.</p>
""",
  status_text="""
<p>Running daily since September 30, 2026; the page is on roughly its twelfth version. Open threads: triaging text messages (the SMS backup misses RCS), signed-in browsing for scheduled runs, and simplifying the Status × Ask schema. A full write-up of the layout, the attention hierarchy and the reply loop is planned for late November.</p>
""")

# ---------- Project: Concert Radar ----------
project_page("concert-radar", "Concert Radar", "live",
  lede="Presale alerts for Denver shows by artists I'd actually buy tickets for, early enough that popular shows don't push me to the resale market. Claude finds and flags; I buy every ticket myself.",
  what="""
<p>Two tiers. <b>Tier 1</b> is the artists I know I like: everyone I've bought tickets for, saved on Spotify, or play the most. A match sends a push to my phone right away and, if the presale is still ahead, puts a fifteen-minute hold on my calendar at presale start. <b>Tier 2</b> is discovery: artists Claude thinks I might like, or similar to what I already listen to, collected quietly into a Thursday-morning digest while that day's presales are still open. Each pick comes with one sentence on what the artist sounds like and a Spotify link, because my knowledge of newer artists has lapsed over the past decade.</p>
<p>Two scheduled runs a week, Tuesday and Thursday morning, each searching six days back through the venue and promoter newsletters already landing in my Gmail: AEG's Thursday "New Shows" list, Live Nation venues, the Paramount, the Botanic Gardens, Seated, Spotify's concert emails, and since mid-October Bandsintown. Matches become rows in a Notion table with the presale window, the type (artist, venue, registration, card), the password if there is one, the ticket link, and any calendar conflict on the show date. Tier 1 presales also get a tile on my Command Center.</p>
""",
  why="""
<p>I already got the main feed. The gaps were filtering, timing, and coverage outside AEG. The real lesson was timing: Hans Zimmer at Ball Arena needed a registration a week before the presale, and the code arrived the day before. For the highest-demand shows, the alert that matters is the announcement-day one, not the presale-day one. By the time a show hits the Thursday list, an earlier artist or venue presale may already have run.</p>
""",
  fig=figs[3][2],
  how_built="""
<ul class="plain">
<li><b>Taste List.</b> A Notion table of artists with a tier (Tier 1, Tier 2, or Skip), the evidence for the tier, and notes. 34 artists at launch, 23 in Tier 1, seeded from Spotify's most-played and saved lists, two years of ticket orders in Gmail, and Spotify's own concert recommendations. The runs read it fresh every time, and Tier 2 rows are Claude's guesses: I move one to Tier 1 or Skip to teach it.</li>
<li><b>Two Claude scheduled tasks</b> that share one instruction set and re-read a "Run rules" section of the project's Notion book every run, so changing the behavior means editing a paragraph, not a prompt in code. The rules cover radius (Fort Collins to Colorado Springs plus the mountain venues for Tier 1, metro Denver for Tier 2), the eight-pick weekly cap on Tier 2, support acts counting as Tier 2, and a rule that every time is written as an absolute ("closes Thu Oct 15, 10pm"), never "tonight."</li>
<li><b>Connectors.</b> Gmail for the newsletters (a filter archives them so they skip my inbox, and the Radar push becomes the signal), Spotify for taste and links, Google Calendar for conflict checks and holds, Notion for the record.</li>
<li><b>Boundaries.</b> The runs never buy, register, or join a queue, and they never write to the Attention Queue: this is the one fun project allowed to send phone alerts directly, because presale windows last hours.</li>
</ul>
<p class="meta">The code is the two task prompts plus the Notion schemas. A standalone version isn't on the roadmap yet; if it lands, it'll be on <a href="https://github.com/chez-san-cmd" target="_blank" rel="noopener">GitHub</a>.</p>
""",
  learned="""
<p><b>The weekly email is the last window, not the first.</b> Leon Bridges at Red Rocks showed up in the AEG list as "Now – Thu 10pm," which means an earlier presale had already run, and by the time I read the digest on Monday, general on-sale had started. Announcement-day coverage needs the artist-level feeds (Bandsintown, Spotify), not the venue roundups.</p>
<p><b>Twice a week is a real trade-off.</b> Moving from daily to Tuesday and Thursday cut noise, but a presale announced late Thursday and closed by Tuesday is missed.</p>
<p><b>Say the day.</b> After the Leon Bridges miss, every digest line carries an absolute date and time. "Tonight" in an email I read three days later means nothing.</p>
""",
  status_text="""
<p>Live since October 9, 2026. First digest went out October 15 with six discovery picks; no Tier 1 match yet. On the list: finish the Bandsintown and Seated setups, add artist mailing lists for the Tier 1 acts, and test whether a scheduled run can reach Ticketmaster's Discovery API, which returns named presale windows directly.</p>
""")

# ---------- Project: Purchase advisor ----------
PA_FIG = """<figure>
<svg viewBox="0 0 900 320" role="img" aria-label="Flow: Tyler asks about a purchase. For anything over $250 a premise check asks whether it is needed, why now, and what happens if he waits; it can end in 'wait' or 'don't buy'. Otherwise the skill defines value as lifetime usefulness over total cost of ownership, researches three tiers from independent long-term testing and owner reports, and recommends: verdict first, top pick and runner-up, target price, what would change the call, and rationalization flags. Tyler buys.">
<defs>
<marker id="ar7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker>
<marker id="ary7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:var(--you)"/></marker>
</defs>
<rect class="gate" x="12" y="16" width="250" height="44" rx="8"/>
<text class="s" x="137" y="34" text-anchor="middle" style="fill:var(--you)">Advisory only</text>
<text class="s" x="137" y="50" text-anchor="middle">never adds to cart, pays, or checks out</text>
<rect class="you" x="20" y="110" width="110" height="60" rx="8"/>
<text class="t" x="75" y="136" text-anchor="middle">Tyler</text>
<text class="s" x="75" y="154" text-anchor="middle">"should I buy…"</text>
<rect class="agent" x="160" y="90" width="190" height="100" rx="8"/>
<text class="t" x="255" y="114" text-anchor="middle">1 Premise check</text>
<text class="s" x="255" y="132" text-anchor="middle">anything over $250</text>
<text class="s" x="255" y="150" text-anchor="middle">needed? why now?</text>
<text class="s" x="255" y="166" text-anchor="middle">what if I wait or do nothing?</text>
<rect class="agent" x="380" y="90" width="170" height="100" rx="8"/>
<text class="t" x="465" y="114" text-anchor="middle">2 Define value</text>
<text class="s" x="465" y="134" text-anchor="middle">lifetime usefulness</text>
<text class="s" x="465" y="150" text-anchor="middle">÷ total cost of ownership</text>
<text class="s" x="465" y="168" text-anchor="middle">price · upkeep · time · resale</text>
<rect class="agent" x="580" y="90" width="170" height="100" rx="8"/>
<text class="t" x="665" y="114" text-anchor="middle">3 Research</text>
<text class="s" x="665" y="134" text-anchor="middle">value pick · sweet spot</text>
<text class="s" x="665" y="148" text-anchor="middle">· buy-it-once</text>
<text class="s" x="665" y="166" text-anchor="middle">long-term tests, owner reports,</text>
<text class="s" x="665" y="180" text-anchor="middle">price history, refurb</text>
<rect class="box" x="770" y="70" width="120" height="140" rx="8"/>
<text class="t" x="830" y="94" text-anchor="middle">4 Recommend</text>
<text class="s" x="830" y="114" text-anchor="middle">verdict first</text>
<text class="s" x="830" y="130" text-anchor="middle">pick + runner-up</text>
<text class="s" x="830" y="146" text-anchor="middle">target price</text>
<text class="s" x="830" y="162" text-anchor="middle">what changes the call</text>
<text class="s" x="830" y="178" text-anchor="middle">rationalization flags</text>
<text class="s" x="830" y="198" text-anchor="middle">links only</text>
<path class="edge y" d="M130 140 L160 140" marker-end="url(#ary7)"/>
<path class="edge" d="M350 140 L380 140" marker-end="url(#ar7)"/>
<path class="edge" d="M550 140 L580 140" marker-end="url(#ar7)"/>
<path class="edge" d="M750 140 L770 140" marker-end="url(#ar7)"/>
<path class="edge d" d="M255 190 L255 240 L130 240" marker-end="url(#ar7)"/>
<text class="lab" x="262" y="236">exit early: "wait" or "don't buy"</text>
<path class="edge y" d="M830 210 L830 270 L130 270" marker-end="url(#ary7)"/>
<text class="lab" x="440" y="290">I click buy, or I don't · the skill never touches a cart</text>
</svg>
<figcaption>Four steps, and the first one can end the conversation. The output is a verdict and links; the card stays in my wallet.</figcaption>
</figure>"""
project_page("purchase-advisor", "Purchase advisor", "live",
  lede="A Claude skill that pressure-tests whether to buy at all, then finds the best real value and recommends. Advisory only: it never buys. I make every purchase myself.",
  what="""
<p>It's a skill rather than a scheduled agent, so it applies anywhere in Claude the moment I'm considering a purchase. For anything over $250 it starts with a premise check: is this needed, why now, and what happens if I wait or do nothing. It revisits those questions when the conversation starts building momentum toward a specific option, and says plainly if the path no longer makes sense. Under $250 it's a one-line sanity check.</p>
<p>If the premise holds, it defines value as lifetime usefulness divided by total cost of ownership (price, consumables, maintenance, time, resale), researches three tiers (a value pick, a sweet spot, and a buy-it-once option) from independent long-term testing and owner reports, checks price history, refurbished and used options, model cycles and warranty, and then recommends. The recommendation leads with the verdict: buy, wait, or don't. Then the top pick and runner-up, a target price, what would change the call, and any rationalizations it caught me making. It gives me links. I click buy, or I don't.</p>
""",
  why="""
<p>Purchases come up ad hoc, and most of the work of a good one is deciding whether to make it at all. I wanted the research without the momentum: a second opinion that's allowed to say "wait," built into the tool I was already going to ask. And it had to be structurally incapable of spending money, because the useful version of an assistant is one I can trust with more each month, and that trust starts with the card staying in my wallet.</p>
""",
  fig=PA_FIG,
  how_built="""
<ul class="plain">
<li><b>One skill file.</b> The whole thing is a written procedure Claude loads when a purchase comes up: the four steps above, the $250 threshold, and the output format. There is no code, no schedule, and no database. The decision log for it lives in a Notion Project Book like every other project.</li>
<li><b>A written point of view on value.</b> Worth paying more for: durability and repairability, things used daily, kid safety, and anything that saves future decisions. Not worth paying for: brand premium, features I won't use, newest-model status. These are first guesses; the skill is told to tune them from my calls.</li>
<li><b>The format is the product.</b> Verdict first, evidence underneath, which is the same pyramid-principle rule every recommendation in my system follows. A brief I can act on in thirty seconds beats a comparison table I have to read.</li>
</ul>
<p class="meta">Skill files are plain Markdown. If I publish mine, it'll be on <a href="https://github.com/chez-san-cmd" target="_blank" rel="noopener">GitHub</a>.</p>
""",
  learned="""
<p><b>The premise check does most of the work.</b> Of the briefs it has produced so far, the useful ones were less about which model and more about whether, and when. A rotating car seat before a second child: yes, and here's the one. LinkedIn Premium during a job search: here's exactly what you'd lose by cancelling, and whether that matters this month.</p>
<p><b>Rules you write for an agent are rules for yourself.</b> Writing down where I'll happily overspend and where I refuse to turned out to be the hard part, and it's still open. The skill can't be more honest about value than I am.</p>
""",
  status_text="""
<p>In use since October 6, 2026. Open questions I owe it: where I'm happy to overspend (running, skiing, scuba, kitchen gear?), where I refuse to pay for the top end, and whether used and refurbished should be the default or only for some categories. A related question in the Concert Radar book: whether a pair of tickets over $250 should trigger the same premise check.</p>
""")

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
how = """
<h1>How I work with AI</h1>
<p class="lede">An assistant that runs in the background is only as trustworthy as the rules it runs under. Here are the rules, then the system that enforces them, then the tools.</p>
<nav class="toc" aria-label="On this page"><a href="#principles">Principles</a><a href="#system">The System</a><a href="#tools">Tools</a></nav>

<h2 id="principles">Principles</h2>
<ol>
<li><b>It never sends anything to another person.</b> Drafts stay drafts until I send them.</li>
<li><b>It never closes my decisions for me.</b> It recommends; I mark done, decline, approve.</li>
<li><b>It never spends money.</b> It can comparison-shop and pressure-test a purchase. The card stays with me.</li>
<li><b>It writes down what it learned.</b> Every project has a book: brief, decisions, open questions, session log. The delta between what it drafts and what I send is how it learns my voice.</li>
<li><b>It brings me decisions, not updates.</b> Recommendation first, evidence underneath, prep already done.</li>
</ol>

<h2 id="system">The system</h2>
<div class="legend">
  <span><i style="border-color:var(--you)"></i> Me (decides, sends, buys)</span>
  <span><i style="border-color:var(--muted);border-style:dashed"></i> Scheduled Claude run</span>
  <span><i style="border-color:var(--accent)"></i> Notion, the system of record</span>
  <span><i style="border-color:var(--rule);background:var(--soft)"></i> Outside service</span>
</div>
"""
KEEP = {0, 1, 4}   # the loop, Project Books, the learning loop; 2 (Job Radar) and 3 (Concerts) live on their project pages
for i, (title, para, fig) in enumerate(figs):
    if i in KEEP: how += f"<h3>{title}</h3><p>{para}</p>{fig}"
how += '<p class="meta">The per-project diagrams, for the <a href="projects/job-radar.html">Job Radar</a> and <a href="projects/concert-radar.html">Concert Radar</a>, are on their project pages.</p>'

how += """
<h2 id="tools">Tools</h2>
<ul class="plain">
<li><b>Claude</b> (Claude Code and its scheduled tasks) does the reading, drafting, scoring and filing. Every run starts from a written brief and ends with a log line.</li>
<li><b>Notion</b> is the system of record: the attention queue, one Project Book per project, and the radar tables. If it isn't in Notion, the agent doesn't know it.</li>
<li><b>GitHub Actions</b> runs the deterministic parts on a schedule, like the daily job fetch, and keeps the data as plain JSON in a repo.</li>
<li><b>Gmail, Google Calendar and Drive</b> are read through connectors. Drafts are written to Gmail; nothing is sent from there by an agent.</li>
<li><b>Spotify</b> supplies taste for the concert radar; venue newsletters supply the presale windows.</li>
<li><b>A single HTML page</b> is the Command Center: no framework, reads Notion live, and has been changed about a hundred times.</li>
</ul>
"""
(S/"how-i-work.html").write_text(page("how-i-work.html","How I work with AI",how))

# ---------- Reading ----------
import json, email.utils, datetime
books = json.loads((pathlib.Path(__file__).resolve().parent/"books.json").read_text())
def _year(b):
    for k in ("read_at","date_added"):
        if b.get(k):
            y = email.utils.parsedate_to_datetime(b[k]).year
            if y >= 2016: return y
            if k=="read_at": break
    return "Earlier"
def _norm(t):
    t = t.replace("\u2019","'").lower()
    t = re.sub(r"\s*\(.*?\)\s*$", "", t)          # drop "(Series, #1)"
    return t.split(":")[0].strip()
_seen = {}
for b in books:                                     # prefer the rated edition, then the one with a read date
    k = _norm(b["title"])
    if k not in _seen or (b["rating"]!="0" and _seen[k]["rating"]=="0") or (b["rating"]==_seen[k]["rating"] and b["read_at"] and not _seen[k]["read_at"]):
        _seen[k] = b
books = list(_seen.values())
groups = {}
for b in books: groups.setdefault(_year(b), []).append(b)
def _sortkey(b): return email.utils.parsedate_to_datetime(b["read_at"] or b["date_added"])
reading = """
<h1>Reading list</h1>
<p class="lede">Everything I've read since I started keeping track, newest first, pulled from my <a href="https://www.goodreads.com/user/show/16104684-tyler" target="_blank" rel="noopener">Goodreads</a> shelf. A ⭐ marks a five-star book.</p>
"""
def _h(t): return t.replace("&","&amp;").replace("<","&lt;")
for y in sorted(groups, key=lambda k: (k=="Earlier", -k if k!="Earlier" else 0)):
    bs = sorted(groups[y], key=_sortkey, reverse=True)
    label = f"{y} <span class=\"count\">· {len(bs)} book{'s' if len(bs)!=1 else ''}</span>" if y!="Earlier" else f"Earlier <span class=\"count\">· {len(bs)} books, read before I kept dates</span>"
    reading += f'<h2 id="y{y}">{label}</h2>\n<ul class="books">\n'
    for b in bs:
        star = ' <span class="star" title="Five stars">⭐</span>' if b["rating"]=="5" else ""
        reading += f'<li><a href="https://www.goodreads.com/book/show/{b["id"]}" target="_blank" rel="noopener">{_h(b["title"])}</a> <span class="au">({_h(b["author"])})</span>{star}</li>\n'
    reading += "</ul>\n"
reading += f'<p class="meta">Updated {datetime.date.today():%B %Y} from Goodreads. {len(books)} books.</p>'
(S/"reading.html").write_text(page("reading.html","Reading list",reading))

# ---------- Years in review ----------
years = """
<h1>Year in review</h1>
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
# Parked for v1 (Tyler, 2026-10-22): not linked and not built. Flip PUBLISH_YEARS to bring it back.
PUBLISH_YEARS = False
if PUBLISH_YEARS: (S/"years-in-review.html").write_text(page("years-in-review.html","Year in review",years))
print("ok", [p.name for p in S.rglob("*.html")], "figs:", len(figs))
