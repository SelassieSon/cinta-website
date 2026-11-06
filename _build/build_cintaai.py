# -*- coding: utf-8 -*-
import common as c
from common import icon, AIURL, WWW
A = icon("arrow")
DEMO = f"{AIURL}/#demo"
HDR = c.header_ai

def demo_section():
    feats = "".join(
     f'<li style="display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.08)">'
     f'<span style="width:32px;height:32px;background:rgba(208,71,71,.2);border-radius:4px;display:flex;align-items:center;justify-content:center;color:var(--red);flex-shrink:0">{icon(ic)}</span>'
     f'<span><span style="display:block;font-size:14px;font-weight:600;color:#fff">{t}</span>'
     f'<span style="font-size:13px;color:rgba(255,255,255,.6)">{x}</span></span></li>'
     for ic,t,x in [
      ("clock","30 minutes, live","See the full 16-agent pipeline in action with your content."),
      ("zap","Your brand, your content","We use your blog post and brand guidelines, not generic samples."),
      ("download","Walk away with content","You keep every piece produced during the demo."),
      ("check","No commitment required","See the platform in action, then decide on your terms.")])
    form = c.embed_form(
      "demo-form",
      "Book your CINTA AI demo",
      "A few details and we send you times to choose from.",
      (c.fld("contact_name","Your name","text","Jane Doe",True)+
       c.fld("contact_email","Work email","email","jane@company.com",True)+
       c.fld("org_name","Company","text","Company Inc.",True)+
       c.fld("website","Website","url","https://company.com",False)+
       c.sel("segment","You are a",["B2B SaaS","Agency","Founder-led","Enterprise","Other"],False)+
       c.ta("message","What would you like to see? (optional)","A blog post or topic you'd like us to run live…",False,3)),
      "Book my demo",
      "Request received",
      "Check your inbox, we've sent a few times to choose from. Pick one and your 30-minute demo is confirmed to the calendar automatically.",
      intent="demo", fallback_subject="CINTA%20AI%20demo")
    return f'''<section class="section section--dark" id="demo"><div class="wrap"><div class="split">
<div data-r><p class="eyebrow section-head" style="color:var(--red)">Book a demo</p>
<h2 style="font-size:var(--fs-h1)">See CINTA transform your content live</h2>
<p style="font-size:17px;color:rgba(255,255,255,.7);line-height:1.7;margin:20px 0 28px">In 30 minutes, we take your actual blog post and transform it into 70+ channel-optimized pieces using your brand guidelines. You keep everything we produce.</p>
<ul style="list-style:none">{feats}</ul></div>
<div data-r data-rd="1">{form}</div></div></div></section>
'''

def plans_section():
    PLANS = [
     ("Starter","Founder-led companies and solo marketers",
      ["1 brand","Core 8 agents","4 channels (40× multiplication)","8 campaigns per month","Email support"], False),
     ("Growth","Growth SaaS with a 2 to 8 person marketing team",
      ["Up to 3 brands","All 16 agents","6 channels (70× multiplication)","Unlimited campaigns","5 personas + RAG","Priority support and weekly office hours"], True),
     ("Agency","Digital agencies and content studios",
      ["Up to 10 brands","All 16 agents per client","Multi-tenant dashboard","White-label options","Up to 10 team members","Dedicated account manager + Slack"], False),
     ("Enterprise","Mid-market orgs and large agencies",
      ["Unlimited brands","Custom agent configs","CRM integration (Salesforce, HubSpot)","Custom workflows","Policy-as-code audit trails","99.9% SLA and a success manager"], False),
    ]
    cards = ""
    for name,who,feats,feature in PLANS:
        fc = " card--feature" if feature else ""
        badge = '<p class="card__eyebrow">Most popular</p>' if feature else ''
        items = "".join(f'<li style="display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--text-body);padding:7px 0">{icon("check")}<span>{f}</span></li>' for f in feats)
        cards += (f'<div class="card{fc}" data-r>{badge}<h3>{name}</h3>'
         f'<p class="card__txt" style="margin-bottom:18px">{who}</p>'
         f'<ul style="list-style:none;margin-bottom:22px">{items}</ul>'
         f'<a href="{DEMO}" class="btn btn-secondary" style="width:100%;justify-content:center">Book a demo {A}</a></div>')
    style = '<style>#plans .cards--4 .card ul li svg{width:16px;height:16px;color:var(--red);stroke-width:2;flex-shrink:0;margin-top:2px}</style>'
    return style+f'''<section class="section section--alt" id="plans"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">Plans</p>
<h2>A plan for every stage</h2>
<p class="section__intro">From solo founders to multi-brand agencies. Book a demo and we will help you choose the right fit.</p></div>
<div class="cards cards--4">{cards}</div></div></section>
'''

# ============================================================ PLATFORM HOME
def home():
    hero = f'''<section class="darkhero"><div class="wrap">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">CINTA AI · Marketing operations platform</span></div>
<h1 data-r data-rd="1">One brief in. <span class="accent">Seventy pieces out.</span></h1>
<p class="darkhero__sub" data-r data-rd="2">CINTA AI turns a single piece of content into 70+ channel-optimized pieces, in your brand voice, with governance built in. A multi-agent system that multiplies your marketing team without multiplying your headcount.</p>
<div class="darkhero__actions" data-r data-rd="3">
<a href="#demo" class="btn btn-primary btn-lg">Book a demo {A}</a>
<a href="#how" class="btn" style="background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)">How it works</a></div>
<div class="darkhero__quote" data-r>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:24px;max-width:680px;margin:0 auto;border-top:1px solid rgba(255,255,255,.1);padding-top:40px">
{"".join(f'<div><div style="font-size:34px;font-weight:700;color:#fff;line-height:1">{n}<span style="color:var(--red);font-size:20px">{u}</span></div><div style="font-size:12px;color:rgba(255,255,255,.55);margin-top:6px">{l}</div></div>' for n,u,l in [("70","×","content multiplication"),("16","","specialized agents"),("6","","channels per campaign"),("48","h","typical turnaround")])}
</div></div></div></section>
'''
    problem = f'''<section class="section"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">The problem</p>
<h2>Your team cannot create fast enough</h2>
<p class="section__intro">Content is the constraint on growth. Hiring is slow and expensive, tools are fragmented, and your best people spend their days producing instead of thinking.</p></div>
<div class="cards cards--3">
<div class="card" data-r><div class="card__icon icon-well">{icon("zap")}</div><h3>The content bottleneck</h3><p class="card__txt">Demand for content outruns what a small team can produce, and quality slips under the pressure to ship.</p></div>
<div class="card" data-r data-rd="1"><div class="card__icon icon-well">{icon("layers")}</div><h3>Tool fragmentation</h3><p class="card__txt">A dozen point tools that do not talk to each other, each needing its own prompt, its own cleanup, its own learning curve.</p></div>
<div class="card" data-r data-rd="2"><div class="card__icon icon-well">{icon("users")}</div><h3>Team capacity</h3><p class="card__txt">Your strategists are stuck producing. The work that actually moves the business waits for a free afternoon that never comes.</p></div>
</div></div></section>
'''
    how = f'''<section class="section section--alt" id="how"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">How it works</p>
<h2>A brief becomes a campaign</h2></div>
<div class="steps steps--4">
<div class="step" data-r><div class="step__n">1</div><h3>Submit a brief</h3><p>One blog post or a short brief, plus your brand guidelines.</p></div>
<div class="step" data-r data-rd="1"><div class="step__n">2</div><h3>Agents go to work</h3><p>16 specialized agents produce across 6 channels in parallel.</p></div>
<div class="step" data-r data-rd="2"><div class="step__n">3</div><h3>Review the output</h3><p>70+ pieces in your voice, with governance and brand checks applied.</p></div>
<div class="step" data-r data-rd="3"><div class="step__n">4</div><h3>Publish and scale</h3><p>Approve, schedule, and ship. Then do it again, in 48 hours.</p></div>
</div></div></section>
'''
    platform = f'''<section class="section" id="platform"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">The platform</p>
<h2>Built for operators, governed for leaders</h2>
<p class="section__intro">Not a chatbot. A multi-agent system with orchestration, brand control, and policy built in.</p></div>
<div class="cards cards--3">
{"".join(f'<div class="card" data-r data-rd="{i%4}"><div class="card__icon icon-well">{icon(ic)}</div><h3>{t}</h3><p class="card__txt">{x}</p></div>' for i,(ic,t,x) in enumerate([
 ("zap","The multiplication engine","One input becomes 70+ channel-ready pieces, each shaped for where it will live."),
 ("users","Multi-agent orchestration","16 specialized agents coordinate, so each piece is made by an agent built for it."),
 ("shield","Brand Guard","Every piece is checked against your brand voice and guidelines before it reaches you."),
 ("layers","Multi-tenant","Run multiple brands side by side with strict isolation. Built for agencies and portfolios."),
 ("clipboard","Policy as code","Approval routing, risk tiers, and audit trails. Governance that satisfies a board."),
 ("building","White-label","Make it yours. Deliver the whole system under your own brand.")]))}
</div></div></section>
'''
    segments = f'''<section class="section section--alt"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">Who it is for</p>
<h2>Find your fit</h2></div>
<div class="cards cards--3">
<div class="card" data-r><div class="card__icon icon-well">{icon("chart")}</div><h3>B2B SaaS</h3><p class="card__txt">Growth teams that need enterprise output from a lean team.</p><a href="{AIURL}/saas.html" class="textlink">For SaaS {A}</a></div>
<div class="card" data-r data-rd="1"><div class="card__icon icon-well">{icon("layers")}</div><h3>Agencies</h3><p class="card__txt">Multi-tenant and white-label, built for client-service margins.</p><a href="{AIURL}/agencies.html" class="textlink">For agencies {A}</a></div>
<div class="card" data-r data-rd="2"><div class="card__icon icon-well">{icon("rocket")}</div><h3>Founders</h3><p class="card__txt">Founder-led companies that need to show up consistently.</p><a href="{AIURL}/founders.html" class="textlink">For founders {A}</a></div>
</div></div></section>
'''
    body = hero+problem+how+platform+plans_section()+segments+demo_section()
    c.write("cintaai","index.html","CINTA AI | Marketing operations platform",
     "CINTA AI turns one brief into 70+ channel-optimized pieces in your brand voice, with governance built in. Book a live demo.",
     HDR("Home"), body)

# ============================================================ SEGMENT PAGES
def segment(slug, nav, title, desc, eyebrow, h1_lead, h1_accent, sub, persona_name,
            persona_role, story, grid_title, grid, plan_note):
    hero = f'''<section class="darkhero"><div class="wrap">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">{eyebrow}</span></div>
<h1 data-r data-rd="1">{h1_lead} <span class="accent">{h1_accent}</span></h1>
<p class="darkhero__sub" data-r data-rd="2">{sub}</p>
<div class="darkhero__actions" data-r data-rd="3"><a href="{DEMO}" class="btn btn-primary btn-lg">Book a demo {A}</a></div></div></section>
'''
    persona = f'''<section class="section"><div class="wrap"><div class="split split--center">
<div data-r><p class="eyebrow section-head">Sound familiar?</p>
<h2>Meet {persona_name}</h2>
<p style="font-size:15px;color:var(--brown);font-weight:600;margin:-8px 0 18px">{persona_role}</p>
{"".join(f"<p>{p}</p>" for p in story)}</div>
<div class="panel-dark" data-r data-rd="1"><p class="card__eyebrow">With CINTA AI</p>
<h3>{grid_title}</h3>
<ul style="list-style:none;margin-top:8px">
{"".join(f'<li style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.1);font-size:14px;color:rgba(255,255,255,.85)"><span style="color:var(--red);flex-shrink:0">{icon("check")}</span>{g}</li>' for g in grid)}
</ul></div></div></div></section>
'''
    planrow = f'''<section class="section section--alt"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">Your plan</p>
<h2>{plan_note}</h2>
<p class="section__intro">Book a demo and we will confirm the right fit for your stage.</p></div>
<div style="text-align:center" data-r><a href="{DEMO}" class="btn btn-primary btn-lg">Book a demo {A}</a></div></div></section>
'''
    c.write("cintaai",f"{slug}.html",title,desc,HDR(),hero+persona+planrow)

def segments():
    segment("saas","SaaS","CINTA AI for B2B SaaS | Marketing operations platform",
      "Enterprise content output from a lean SaaS marketing team. Book a live demo.",
      "For B2B SaaS","Enterprise output,","lean team",
      "You have a 2 to 8 person marketing team and the content demands of a company three times your size. CINTA AI closes that gap.",
      "Sarah","VP Marketing at a $15M ARR SaaS company, 4-person team",
      ["Sarah's team ships good work, but never enough of it. Every new channel means another hire she cannot justify, or another late night she cannot sustain.",
       "The backlog is not a people problem. It is a throughput problem. One strong idea should become a campaign across six channels, not a single blog post that took a week.",
       "With CINTA AI, Sarah's team briefs once and ships a full campaign in 48 hours, in brand, reviewed, and ready."],
      "What changes for Sarah's team",
      ["70× multiplication from a single brief","48-hour turnaround on full campaigns","83% less time spent on production","All 16 agents, 6 channels, unlimited campaigns","Her strategists back on strategy"],
      "Growth is built for teams like yours")
    segment("agencies","Agencies","CINTA AI for agencies | Multi-tenant, white-label",
      "Multi-tenant, white-label content operations built for agency margins. Book a demo.",
      "For agencies","Better margins,","more brands",
      "Client content is labour-intensive and the margins show it. CINTA AI's multi-tenant, white-label system changes the economics.",
      "A growing studio","10 to 50 clients, lean delivery team",
      ["Agencies win content retainers, then watch the margin erode in production hours. More clients means more headcount, and the math gets worse, not better.",
       "The multi-tenant model flips it. Run every client brand side by side, with strict isolation, under your own label.",
       "Your team moves from producing to directing, and the margin moves with them."],
      "What changes for your studio",
      ["Up to 10 brands, each fully isolated","White-label delivery under your brand","Multi-tenant dashboard across clients","Dedicated account manager and Slack","Production hours converted to margin"],
      "Agency is built for multi-brand delivery")
    segment("founders","Founders","CINTA AI for founders | Show up consistently",
      "Founder-led content that ships consistently without a marketing team. Book a demo.",
      "For founders","Show up,","consistently",
      "You know content matters. You also have a company to run. CINTA AI makes consistent, on-brand content possible without a marketing hire.",
      "Jen","Founder-CEO at a $3M ARR company, no marketing team",
      ["Jen's content is sporadic. A burst when she has time, then silence for a month when the business needs her elsewhere. The market forgets fast.",
       "Consistency is the whole game, and consistency is exactly what a founder's calendar cannot promise.",
       "With CINTA AI, Jen briefs once and the system keeps her visible, in her voice, while she runs the company."],
      "What changes for Jen",
      ["40× multiplication from one brief","8 campaigns a month without a hire","Her voice, applied consistently","4 channels covered automatically","Visibility that does not depend on free time"],
      "Starter is built for founders")

# ============================================================ BRIEF
def brief():
    hero = f'''<section class="darkhero" style="padding-bottom:48px"><div class="wrap">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">Submit a brief</span></div>
<h1 data-r data-rd="1">Give us one brief. <span class="accent">Get a campaign.</span></h1>
<p class="darkhero__sub" data-r data-rd="2">Share a blog post or a short brief and your brand guidelines. We return 70+ channel-optimized pieces within 48 hours.</p></div></section>
'''
    briefform = c.embed_form(
      "brief-form",
      "Content brief",
      "Takes about three minutes. We reply within one business day.",
      (c.fld("contact_name","Full name","text","Jane Doe",True)+
       c.fld("contact_email","Work email","email","jane@company.com",True)+
       c.fld("org_name","Company","text","Company Inc.",True)+
       c.fld("website","Website","url","https://company.com",False)+
       c.sel("segment","Segment",["B2B SaaS","Agency","Founder-led","Other"],False)+
       c.ta("message","Paste your content or a short brief","A blog post, a brief, or a link…",True,5)+
       c.ta("brand_notes","Brand guidelines (link or notes)","Link to your brand guide, or key voice notes…",False,2)),
      "Submit brief",
      "Brief received",
      "Thank you. Your brief is in, and we'll be in touch within one business day to confirm scope and get started.",
      intent="lead", hidden={"service_interest": "CINTA AI content brief"},
      fallback_subject="CINTA%20AI%20content%20brief")
    form = f'''<section class="section"><div class="wrap"><div class="split">
<div data-r><h2>What happens next</h2>
<div class="steps" style="grid-template-columns:1fr;gap:24px;margin-top:24px">
<div style="display:flex;gap:18px"><div class="step__n" style="margin:0">1</div><div><h3 style="font-size:16px">Submit your brief</h3><p style="color:var(--muted);font-size:14px">Your content and brand guidelines, in one form.</p></div></div>
<div style="display:flex;gap:18px"><div class="step__n" style="margin:0">2</div><div><h3 style="font-size:16px">We produce</h3><p style="color:var(--muted);font-size:14px">16 agents generate across your chosen channels.</p></div></div>
<div style="display:flex;gap:18px"><div class="step__n" style="margin:0">3</div><div><h3 style="font-size:16px">You review in 48 hours</h3><p style="color:var(--muted);font-size:14px">On-brand, governed, and ready to publish.</p></div></div>
</div></div>
<div data-r data-rd="1">{briefform}</div></div></div></section>
'''
    c.write("cintaai","brief.html","Submit a brief | CINTA AI",
     "Submit a content brief to CINTA AI and get 70+ channel-optimized pieces within 48 hours.",
     HDR(), hero+form)

# ============================================================ ASSESSMENT
def assessment():
    QS = [
     ("How large is the gap between the content you need and what you produce?",
      ["We keep up fine","A small gap","A large gap","We are drowning"]),
     ("Is your brand voice and are your guidelines documented?",
      ["Not written down","Loosely","Mostly documented","Fully documented and current"]),
     ("How is your marketing team's time split?",
      ["Mostly strategy","Balanced","Mostly producing","Almost all producing"]),
     ("How many separate tools are in your content workflow?",
      ["1 to 2","3 to 5","6 to 10","More than 10"]),
     ("How far along is your AI adoption for marketing?",
      ["Not started","Experimenting","Some workflows","Embedded across the team"]),
     ("Do you have a content review and approval process?",
      ["None","Ad hoc","A light process","A defined approval workflow"]),
     ("Are your brand assets and past content organized and accessible?",
      ["Scattered","Somewhat","Mostly organized","Centralized and tagged"]),
     ("Does leadership back investing in AI for marketing?",
      ["No appetite","Curious","Supportive","Mandated this year"]),
    ]
    TIERS = [
     {"max":7,"t":"Early — set the foundation","x":"The need is real, but a few basics come first. Document your brand voice and consolidate your tools, and agentic AI will pay off far faster. A demo shows exactly where you would start.",
      "steps":["Document your brand voice and guidelines in one place","Consolidate your scattered content tools","Book a demo to see agentic production run on your own content"]},
     {"max":13,"t":"Ready to pilot","x":"You have the need and enough structure to start. A short pilot on your real content proves the 70x multiplication before you commit to anything.",
      "steps":["Pick one flagship piece to run through the pipeline","Confirm your brand guidelines are current","Book a demo and watch one brief become a full campaign"]},
     {"max":19,"t":"Ready to scale","x":"Strong fit. You have the demand, the governance, and the appetite. Move from a pilot to a standing agentic workflow across your channels.",
      "steps":["Move your team from producing to reviewing and directing","Set an approval workflow so governance scales with volume","Book a demo to map a rollout across your channels"]},
     {"max":24,"t":"Ready to operationalize","x":"You are ready to run marketing as an agentic operation, with governance built in. If you serve multiple brands, the multi-tenant setup changes your margins.",
      "steps":["If you run multiple brands or clients, evaluate the multi-tenant setup","Integrate the pipeline with your CRM and publishing","Book a demo to plan your operating model and governance"]},
    ]
    c.assessment_page("cintaai","assessment","Agentic Readiness Assessment | CINTA AI",
     "An 8-question check of how ready your marketing operation is to put agentic AI to work, with a personalized action plan. About two minutes.",
     HDR(), "Agentic readiness assessment",
     "Is your marketing ready for","agentic AI?",
     "Eight questions, about two minutes. See how ready your marketing operation is to put agentic AI to work, and the fastest path to value for where you are.",
     QS, TIERS, "Agentic Readiness Assessment",
     DEMO, "Or book a live demo")

if __name__ == "__main__":
    home(); segments(); brief(); assessment()
    print("cintaai: platform, saas, agencies, founders, brief, assessment written")
