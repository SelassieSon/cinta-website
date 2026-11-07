# -*- coding: utf-8 -*-
import urllib.parse as _u
import common as c
from common import icon, WWW, RAI, AIURL, INS, LI

A = icon("arrow")

# ============================================================ HOME
def home():
    hero = f'''<section class="hero"><div class="hero__accent"></div>
<div class="wrap hero__in"><div>
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">Mid-market consulting · Toronto, Ontario</span></div>
<h1 data-r data-rd="1">Transform with confidence when the <span class="accent">ground is shifting</span></h1>
<p class="hero__sub" data-r data-rd="2">CINTA &amp; Co. combines neuroscience-informed leadership development with practical business systems, so you do not just survive what is next. You shape it.</p>
<div class="hero__actions" data-r data-rd="3">
<a href="{WWW}/contact.html" class="btn btn-primary btn-lg">Book your Ecosystem Mapping Session {A}</a>
<a href="{WWW}/services.html" class="textlink">Explore our services {A}</a></div></div>
<div class="hero__panel" data-r data-rd="2"><p class="hero__panel-t">CINTA at a glance</p>
<div class="hero__facts">
<div><div class="hero__fact-n">2020</div><div class="hero__fact-l">Founded in Toronto, Ontario</div></div>
<div><div class="hero__fact-n">6</div><div class="hero__fact-l">Sectors served across the mid-market</div></div>
<div><div class="hero__fact-n">4</div><div class="hero__fact-l">Integrated service domains</div></div>
<div><div class="hero__fact-n">1<span class="u"> network</span></div><div class="hero__fact-l">Curated ecosystem of vetted experts</div></div>
</div></div></div></section>
'''
    strip = ('<div class="strip"><div class="wrap strip__in">'
     '<span class="strip__label">Sectors we serve</span>'
     + '<span class="strip__dot"></span>'.join(
        f'<span class="strip__item">{s}</span>' for s in
        ["Education","Sports &amp; Recreation","Social Impact","Health &amp; Wellness",
         "Entrepreneurship","Building Materials &amp; Manufacturing"])
     + '</div></div>\n')

    position = f'''<section class="section"><div class="wrap"><div class="split">
<div data-r><p class="eyebrow section-head">Why CINTA</p>
<h2>The disruption is compounding. <span class="accent">Your partner should be too.</span></h2>
<p>In 2026, mid-market organizations are not facing one challenge at a time. Technology adoption, regulatory complexity, workforce change, and economic pressure arrive together, and they compound.</p>
<p>Generic consultants offer a single tool. We offer a coherent system, built for organizations that need senior expertise without enterprise overhead.</p>
<a href="{WWW}/about.html" class="textlink">Read our story and approach {A}</a></div>
<div class="diffs" data-r data-rd="2">
<div class="diff"><span class="red-bullet"></span><div><h3>Neuroscience-informed transformation</h3><p>We draw on NeuroLeadership Institute principles to move teams from fear-based resistance to purpose-driven adoption. Technology changes. The science of how people navigate change does not.</p></div></div>
<div class="diff"><span class="red-bullet"></span><div><h3>Sector depth where it is rare</h3><p>Education, sports, social impact, and health are underserved by large firms. You get practitioners who already understand your operating reality, your stakeholders, and your constraints.</p></div></div>
<div class="diff"><span class="red-bullet"></span><div><h3>Right-sized for the mid-market</h3><p>Bespoke programs and senior practitioners, calibrated for organizations that need more than an online course and less than a seven-figure engagement.</p></div></div>
</div></div></div></section>
'''
    def dcard(n,ic,title,txt,href):
        return (f'<div class="card" data-r><span class="card__num">{n}</span>'
         f'<div class="card__icon icon-well">{icon(ic)}</div>'
         f'<h3>{title}</h3><p class="card__txt">{txt}</p>'
         f'<a href="{href}" class="textlink">Learn more {A}</a></div>')
    domains = f'''<section class="section section--alt"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">What we do</p>
<h2>Four domains, one coherent approach</h2>
<p class="section__intro">You get an integrated partner across the full arc of transformation, from the human side of change to the systems, governance, and revenue capability that make strategy real.</p></div>
<div class="cards cards--4">
{dcard("01","brain","Leadership &amp; Transformation","Change fails when it triggers a threat response, not because people are stubborn. You get neuroscience-informed programs that build genuine adoption and lasting capability.",WWW+"/services.html#transformation")}
{dcard("02","target","Strategic Planning &amp; Strategy Implementation","Plans fail in execution, not on paper. We stay through implementation, building the milestones, measurement, and accountability that turn intent into outcomes.",WWW+"/services.html#strategy")}
{dcard("03","refresh","Business Model Innovation &amp; Organizational Design","The model that brought you here may not carry you forward. You get a stress-tested model and an organizational design built for what comes next.",WWW+"/services.html#innovation")}
{dcard("04","scale","Digital Strategy &amp; Responsible Innovation","Technology is one tool among many. You get AI governance, shadow AI audits, and workflow design, with responsible practice built in from the first day.",RAI)}
</div></div></section>
'''
    approach = f'''<section class="section"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">How we work</p>
<h2>We assemble the right experts for your challenge</h2>
<p class="section__intro">As a network-model firm, we are the integrator. We understand your whole situation, then bring the right specialists from our ecosystem, including the NeuroLeadership Institute and our Responsible AI partners at CoCr8 Labs.</p></div>
<div class="steps steps--5">
<div class="step" data-r><div class="step__n">1</div><h3>Diagnose</h3><p>Map your ecosystem, pressures, and the priorities that matter most.</p></div>
<div class="step" data-r data-rd="1"><div class="step__n">2</div><h3>Design</h3><p>Build a bespoke program for your situation. Nothing off the shelf.</p></div>
<div class="step" data-r data-rd="2"><div class="step__n">3</div><h3>Facilitate</h3><p>Lead the learning, coaching, and change work that builds capability.</p></div>
<div class="step" data-r data-rd="3"><div class="step__n">4</div><h3>Build</h3><p>Stand up systems, workflows, and governance with partners as needed.</p></div>
<div class="step" data-r data-rd="4"><div class="step__n">5</div><h3>Sustain</h3><p>Support execution with reviews and retainers as the work matures.</p></div>
</div></div></section>
'''
    def scard(sid,ic,title,txt,entry):
        return (f'<div class="card scard" data-r><div class="card__icon icon-well">{icon(ic)}</div>'
         f'<h3>{title}</h3><p class="card__txt">{txt}</p>'
         f'<p class="scard__entry">{entry}</p></div>')
    sectors = f'''<section class="section section--alt"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">Sectors</p>
<h2>We know your world because we have worked in it</h2>
<p class="section__intro">You get senior practitioners with real history in your sector, not a generic playbook adapted on the fly.</p></div>
<div class="cards cards--3">
{scard("education","cap","Education","AI policy uncertainty, faculty fatigue, enrollment pressure, and EDSTA compliance, arriving together.","Leadership &amp; Transformation")}
{scard("sports","trophy","Sports &amp; Recreation","Youth data governance, volunteer-model strain, and digital expectations from members and sponsors.","Strategic Planning")}
{scard("social","heart","Social Impact","Technology adoption that honours mission, satisfies funders, and fits real capacity limits.","Business Model Innovation")}
{scard("health","cross","Health &amp; Wellness","Privacy duties under PHIPA and EDSTA, balanced against service delivery and workforce wellbeing.","Responsible Innovation")}
{scard("ent","rocket","Entrepreneurship","Scaling with the right technology and building the management systems that growth demands.","Digital Strategy")}
{scard("bm","factory","Building Materials &amp; Manufacturing","Supply chain volatility, trade pressure, an aging skilled workforce, and the pull toward digital operations.","Strategic Planning")}
</div></div></section>
'''
    insights = f'''<section class="section"><div class="wrap">
<div class="section__head" data-r style="display:flex;justify-content:space-between;align-items:flex-end;max-width:none;gap:24px">
<div><p class="eyebrow section-head">Insights</p><h2>Ideas for leaders navigating disruption</h2></div>
<a href="{INS}" class="btn btn-secondary">Read The Mid-Market Compass {A}</a></div>
<div class="cards cards--3">
<div class="card" data-r><p class="card__eyebrow">Responsible innovation</p><h3>Shadow AI is already in your organization. Here is what to do next.</h3><p class="card__txt">Your people are using AI tools today, and most have not told anyone. Move from quiet risk to clear governance without slowing teams down.</p></div>
<div class="card" data-r data-rd="1"><p class="card__eyebrow">Human side of transformation</p><h3>Why your transformation initiative is stalling, and it is not what you think</h3><p class="card__txt">The resistance is neurological, not ideological. What the science says about moving a team forward.</p></div>
<div class="card" data-r data-rd="2"><p class="card__eyebrow">Making strategy work</p><h3>The strategic plan that actually gets implemented</h3><p class="card__txt">The plan is the easy part. Here is the framework that makes execution stick.</p></div>
</div></div></section>
'''
    assess = f'''<section class="section"><div class="wrap">
<div class="assessband" data-r>
<div class="assessband__txt"><p class="eyebrow section-head">Free diagnostic</p>
<h2>Where does your organization stand in the agentic era?</h2>
<p class="section__intro">A short self-assessment built on the MIT CISR framework. It maps you onto the agentic AI stages and scores you across tools, workflow, governance, infrastructure, and strategy. About two minutes, with a tailored next step.</p></div>
<div class="assessband__act"><a href="{AIURL}/assessment.html" class="btn btn-primary btn-lg">Take the Agentic Readiness Assessment {A}</a>
<a href="{AIURL}/brief.html" class="textlink" style="margin-top:14px">Prefer to read first? The Agentic AI Executive Brief {A}</a></div>
</div></div></section>
'''
    cta = c.cta_red("Ready to navigate what is next?",
        "Book an Ecosystem Mapping Session and leave with a clear, honest read on where to focus first.",
        "Book your Ecosystem Mapping Session", f"{WWW}/contact.html")
    body = hero+strip+position+domains+approach+assess+sectors+insights+cta
    c.write("www","index.html","CINTA & Co. | Facilitating Success",
        "CINTA & Co. helps mid-market leaders navigate compounding disruption with neuroscience-informed leadership and practical business systems.",
        c.header_www("Home"), body)

# ============================================================ ABOUT
def about():
    hero = f'''<section class="pagehero"><div class="pagehero__accent"></div>
<div class="wrap pagehero__in">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">About CINTA &amp; Co.</span></div>
<h1 data-r data-rd="1">The consulting partner for when the <span class="accent">ground is shifting</span></h1>
<p class="pagehero__sub" data-r data-rd="2">We help mid-market organizations navigate compounding disruption through neuroscience-informed leadership development and practical business systems.</p></div></section>
'''
    story = f'''<section class="section"><div class="wrap"><div class="split">
<div data-r><p class="eyebrow section-head">Our story</p>
<h2>The thesis has not changed. The urgency has.</h2>
<p>CINTA &amp; Co. was founded in 2020 on a simple premise. Mid-market organizations need a different kind of consulting partner. Not a Big Four firm that assigns junior analysts, and not a generalist freelancer. A firm that understands their scale, their constraints, and their ambition.</p>
<p>In 2020, the challenge was digital transformation broadly. In 2026, it is compounding disruption. AI adoption, regulatory complexity, workforce change, economic pressure, and demographic shifts arrive together, not one at a time.</p>
<p>You do not need an AI company or a training vendor. You need a transformation partner who understands all of these forces and can help you respond coherently. That is what we do.</p></div>
<div class="diffs" data-r data-rd="2">
<div class="diff"><span class="red-bullet"></span><div><h3>Founded 2020</h3><p>Toronto, Ontario. Built for the Ontario mid-market from day one.</p></div></div>
<div class="diff"><span class="red-bullet"></span><div><h3>Six sectors</h3><p>Education, sports, social impact, health, entrepreneurship, and building materials.</p></div></div>
<div class="diff"><span class="red-bullet"></span><div><h3>Network model</h3><p>A curated ecosystem of vetted specialists, assembled per engagement.</p></div></div>
<div class="diff"><span class="red-bullet"></span><div><h3>A living brand promise</h3><p>Comfort the weary and inspire effective action.</p></div></div>
</div></div></div></section>
'''
    founder = f'''<section class="section section--dark"><div class="wrap">
<div style="display:grid;grid-template-columns:280px 1fr;gap:64px;align-items:start" class="founder">
<div data-r><div style="aspect-ratio:1;background:linear-gradient(135deg,var(--brown),#5a2a15);border-radius:var(--r-lg);display:flex;align-items:center;justify-content:center;font-size:92px">👤</div></div>
<div data-r data-rd="1"><p class="eyebrow section-head" style="color:var(--red)">Founder &amp; Managing Director</p>
<h2 style="font-size:32px">Unika Hypolite</h2>
<p style="font-size:15px;color:rgba(255,255,255,.65);margin:6px 0 24px">Strategist · Coach · Marketer · Two decades agency and client-side</p>
<p style="font-size:16px;line-height:1.8;color:rgba(255,255,255,.85);margin-bottom:18px">Unika is an accomplished strategist, coach, and marketer, acknowledged for his problem-solving and facilitation. His experience spans two decades working both agency and client-side, leading organizations through uncertainty while building toward sustainable success.</p>
<p style="font-size:16px;line-height:1.8;color:rgba(255,255,255,.85);margin-bottom:18px">He is undaunted by new challenges, approaching problems with a clear mind and a willingness to experiment, always looking to the future to find new opportunities. That orientation is the engine behind CINTA's approach. Diagnose honestly, design boldly, and facilitate the change that makes strategy real.</p>
<p style="font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--red);margin:28px 0 16px;padding-top:24px;border-top:1px solid rgba(255,255,255,.15)">Areas of proficiency</p>
<div style="display:flex;flex-wrap:wrap;gap:10px">
{"".join(f'<span style="font-size:13px;color:rgba(255,255,255,.7);padding:7px 14px;background:rgba(255,255,255,.08);border-radius:20px">{t}</span>' for t in ["Organizational Strategy","Brand Strategy","Digital Marketing","Change Management","Coach Development","Channel Programs","Project Management","Market Research"])}
</div>
<div style="margin-top:28px"><a href="{LI}" target="_blank" rel="noopener" class="btn" style="background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.3)">View LinkedIn profile {A}</a></div>
</div></div></div></section>
'''
    integrator = f'''<section class="section"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">The system integrator model</p>
<h2>We assemble the right experts for your challenge</h2>
<p class="section__intro">The network model is now table stakes for boutique firms. What makes CINTA different is the specific ecosystem we have built, and the judgment to assemble it well.</p></div>
<div class="cards cards--4">
<div class="card" data-r><div class="card__icon icon-well">{icon("brain")}</div><h3>NeuroLeadership Institute</h3><p class="card__txt">Brain-based transformation and change methodology.</p></div>
<div class="card" data-r data-rd="1"><div class="card__icon icon-well">{icon("shield")}</div><h3>CoCr8 Labs</h3><p class="card__txt">Responsible AI governance and technical implementation.</p></div>
<div class="card" data-r data-rd="2"><div class="card__icon icon-well">{icon("layers")}</div><h3>Sector ecosystem</h3><p class="card__txt">Specialists with deep roots in the markets we serve.</p></div>
<div class="card" data-r data-rd="3"><div class="card__icon icon-well">{icon("handshake")}</div><h3>Specialist network</h3><p class="card__txt">Design, data, and delivery partners, vetted and ready.</p></div>
</div></div></section>
'''
    values = f'''<section class="section section--alt"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">How we show up</p>
<h2>Informed. Candid. Warm.</h2>
<p class="section__intro">Our brand personality is not a marketing exercise. It is how we actually work.</p></div>
<div class="cards cards--3">
<div class="card" data-r><div class="card__icon icon-well">{icon("search")}</div><h3>Informed</h3><p class="card__txt">We do the homework. We know your sector, the research, the regulatory landscape, and the trends. We do not wing it.</p></div>
<div class="card" data-r data-rd="1"><div class="card__icon icon-well">{icon("handshake")}</div><h3>Candid</h3><p class="card__txt">We tell you what you need to hear, not what you want to hear. Respectful honesty is the foundation of trust.</p></div>
<div class="card" data-r data-rd="2"><div class="card__icon icon-well">{icon("heart")}</div><h3>Warm</h3><p class="card__txt">We are approachable and human. Consulting does not have to be sterile. We build genuine relationships.</p></div>
</div></div></section>
'''
    cta = c.cta_red("Ready to talk?",
        "Book an Ecosystem Mapping Session and see how CINTA can help your organization navigate what is next.",
        "Book your Ecosystem Mapping Session", f"{WWW}/contact.html")
    body = hero+story+founder+integrator+values+cta
    c.write("www","about.html","About | CINTA & Co.",
        "CINTA & Co. is the consulting partner mid-market organizations trust when the ground is shifting. Led by Unika Hypolite in Toronto.",
        c.header_www("About"), body)

# ============================================================ SECTORS
def sectors():
    hero = f'''<section class="pagehero"><div class="pagehero__accent"></div>
<div class="wrap pagehero__in">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">Sectors we serve</span></div>
<h1 data-r data-rd="1">We know your world <span class="accent">because we have worked in it</span></h1>
<p class="pagehero__sub" data-r data-rd="2">Mid-market organizations face pressures the Big Four overlooks and generalists do not understand. We do. Every sector we serve shares one reality: compounding disruption.</p></div></section>
'''
    SECT = [
        ("education","cap","Education","Colleges, universities, and school boards",
         ["Your faculty are divided about AI. Students use tools the institution has not sanctioned. The executive team is tired from years of pandemic-era change, and enrollment pressure keeps building.",
          "Most institutions are making AI decisions without a coherent framework. Shadow AI is everywhere, EDSTA requirements are landing, and no one has the bandwidth to sort it out.",
          "We know how academic governance works, why faculty resist, and when that resistance is right. We help you build consensus without watering down the strategy."],
         ["AI policy uncertainty and shadow AI","Faculty fatigue and change readiness","Enrollment pressure and demographic shifts","EDSTA compliance obligations","Student expectations outpacing readiness"],
         "Leadership &amp; Transformation, or Strategic Planning", False),
        ("sports","trophy","Sports &amp; Recreation","National and provincial bodies, clubs, leagues",
         ["Performance analytics, youth data governance, and the digital expectations of members and sponsors. Your board asks technology questions your staff cannot answer, and the volunteer model that built Canadian sport is straining.",
          "You cannot adopt technology the way a corporation does. Parents, athletes, coaches, volunteers, sponsors, and funders each have legitimate concerns about data, privacy, and change.",
          "We understand the governance complexity, the volunteer reality, and the balance between modernization and mission."],
         ["Digital expectations from members and sponsors","Data governance for youth participants","Performance analytics, what to adopt","Volunteer workforce sustainability","Evolving community expectations"],
         "Strategic Planning, with Digital Strategy", True),
        ("social-impact","heart","Social Impact","Non-profits, foundations, social enterprises",
         ["Your funders want innovation. Your board wants efficiency. Your staff want to focus on mission. And everyone has an opinion about AI, from utopian to apocalyptic.",
          "The capacity constraint is real. No CTO, no transformation budget, a small team doing important work with limited resources. Technology has to be right-sized to that reality.",
          "We design transformation that honours mission, fits capacity, and satisfies funders, without chasing every tool."],
         ["Technology adoption with mission alignment","Funder expectations on innovation","Responsible practice at limited capacity","Organizational capacity constraints","Staff sustainability and retention"],
         "Business Model Innovation, with Ecosystem Mapping", False),
        ("health","cross","Health &amp; Wellness","Clinics, wellness organizations, service providers",
         ["PHIPA, EDSTA, and privacy impact assessments. The regulatory burden on health organizations adopting technology is significant, and it should be. You handle sensitive information about real people.",
          "Most technology vendors do not understand this. They want to sell you AI for intake, matching, and efficiency, and would rather not discuss the compliance work that using it responsibly requires.",
          "We start with governance. What PHIPA requires, what EDSTA requires, and what an Algorithm Impact Assessment looks like for your use case. Then we design adoption that fits."],
         ["Privacy and compliance under PHIPA and EDSTA","Technology that protects trust","Workforce adaptation and wellbeing","Efficiency balanced against care quality","Governance for sensitive health data"],
         "Responsible Innovation, or Leadership &amp; Transformation", True),
        ("entrepreneurship","rocket","Entrepreneurship","Growth-stage companies, scale-ups, founder-led firms",
         ["You built something that works. Now you need it to scale. The systems that got you here will not get you there. You know this. You just do not have time to fix it while running the business.",
          "The pressure to adopt AI is everywhere. Investors ask, competitors mention it, vendors pitch it. Few tell you how to judge what is real or integrate it without breaking what works.",
          "We work with founders ready to build the next version of their company. Business model evolution, management systems, technology integration, and regulatory navigation."],
         ["Scaling with the right technology","Business model evolution for the next stage","Building management systems mid-flight","Navigating regulatory requirements","Hiring and team development"],
         "Business Model Innovation, with Digital Strategy", False),
        ("building-materials","factory","Building Materials &amp; Manufacturing","Producers, distributors, industrial manufacturers",
         ["Supply chains are volatile and trade policy shifts under your feet. The skilled workforce that built your operation is aging out, and the people you want to hire expect something different. Every competitor is talking about digital operations, and you are not sure what is real.",
          "Manufacturing transformation is rarely a technology problem. It is a people-and-process problem in a technology costume. New systems fail on the plant floor when the workforce has no reason to trust them.",
          "Our managing director spent years leading marketing for a major building materials manufacturer, so we understand plant-floor realities, channel and distributor dynamics, and the Buy Canadian shift reshaping how Canadian manufacturers compete and win."],
         ["Supply chain volatility and trade pressure","Aging skilled workforce and knowledge transfer","Digital operations and Industry 4.0 adoption","Sustainability and ESG reporting","Buy Canadian procurement and channel realignment"],
         "Strategic Planning, with Business Model Innovation", True),
    ]
    out = hero
    for sid,ic,title,sub,paras,chals,entry,alt in SECT:
        altcls = " section--alt" if alt else ""
        pblock = "".join(f'<p>{p}</p>' for p in paras)
        cblock = "".join(f'<li><span style="color:var(--red);flex-shrink:0">→</span> {ch}</li>' for ch in chals)
        out += f'''<section class="section{altcls}" id="{sid}"><div class="wrap"><div class="split">
<div data-r><div class="card__icon icon-well" style="margin-bottom:22px">{icon(ic)}</div>
<h2>{title}</h2><p style="font-size:15px;font-weight:600;color:var(--brown);margin:-8px 0 20px">{sub}</p>
{pblock}<div style="margin-top:30px"><a href="{WWW}/contact.html?sector={_u.quote(title.replace("&amp;","&"))}" class="btn btn-secondary">Talk to us about this sector {A}</a></div></div>
<div class="card" data-r data-rd="1"><p class="card__eyebrow">The compounding challenges</p>
<ul style="display:flex;flex-direction:column;gap:0;margin-top:8px">{cblock}</ul>
<div style="margin-top:20px;padding-top:20px;border-top:1px solid var(--gray)">
<p style="font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:8px">Natural entry point</p>
<p style="font-size:15px;font-weight:600;color:var(--text)">{entry}</p></div></div>
</div></div></section>
'''
    out = out.replace('<ul style="display:flex;flex-direction:column;gap:0;margin-top:8px">',
                      '<ul style="display:flex;flex-direction:column;gap:0;margin-top:8px" class="chlist">')
    out += c.cta_red("Not sure where to start?",
        "Book an Ecosystem Mapping Session. Ninety minutes with a senior practitioner to map your situation and identify priority actions.",
        "Book your Ecosystem Mapping Session", f"{WWW}/contact.html")
    style = ('<style>.chlist li{display:flex;gap:10px;align-items:flex-start;font-size:14px;'
     'color:var(--text-body);padding:10px 0;border-bottom:1px solid var(--gray)}'
     '.chlist li:last-child{border-bottom:none}</style>')
    c.write("www","sectors.html","Sectors | CINTA & Co.",
        "CINTA & Co. serves mid-market organizations in education, sports and recreation, social impact, health and wellness, entrepreneurship, and building materials and manufacturing.",
        c.header_www("Sectors"), style+out)

# ============================================================ SERVICES
def services():
    hero = f'''<section class="pagehero"><div class="pagehero__accent"></div>
<div class="wrap pagehero__in">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">What we do</span></div>
<h1 data-r data-rd="1">Four domains, <span class="accent">one coherent approach</span></h1>
<p class="pagehero__sub" data-r data-rd="2">We do not sell tools, and we do not deliver a deck and disappear. We facilitate transformation through programs that combine learning, design, and implementation.</p></div></section>
'''
    def svc(title, txt, feature=False):
        fc = " card--feature" if feature else ""
        eb = '<p class="card__eyebrow">New offering</p>' if feature else ''
        q = _u.quote(title.replace('&amp;', '&'))
        cta = f'<a href="{WWW}/contact.html?service={q}" class="textlink" style="margin-top:16px">Book a session {A}</a>'
        return f'<div class="card{fc}" data-r>{eb}<h3>{title}</h3><p class="card__txt">{txt}</p>{cta}</div>'
    DOM = [
        ("transformation","01","Leadership &amp; Transformation",
         "Change fails because it triggers a threat response, not because people are stubborn. We apply NeuroLeadership Institute principles to move teams from fear-based resistance to purpose-driven adoption. This remains CINTA's most distinctive capability.",
         "Unlike off-the-shelf training, every program is designed for your teams and your challenge.", False,
         [("Corporate Learning Lab","A 12-week transformation program for intact teams. Cohort learning applied to real organizational challenges, with completed work products by the end.",False),
          ("Executive Coaching","One-on-one coaching for leaders navigating change. A neuroscience-informed approach to decisions, resilience, and leading through uncertainty.",False),
          ("Team Workshop Series","Focused sessions on a specific challenge, typically three to five over four to eight weeks. Change leadership, technology adoption, organizational resilience.",False),
          ("Technology Change Management","Support for technology adoption through the human side. Why people resist, what would make them adopt, and how to build the muscle for continuous change.",False)]),
        ("strategy","02","Strategic Planning &amp; Strategy Implementation",
         "Plans fail in execution, not on paper. The plan gets approved, then sits in a drawer. We stay through implementation, embedding technology milestones, regulatory requirements, and accountability into the execution framework.",
         "Unlike consultants who deliver a deck and leave, we facilitate the change that makes strategy real.", True,
         [("Strategic Planning Engagement","A facilitated process with environmental analysis, stakeholder engagement, strategy development, and an implementation framework you can actually run.",False),
          ("Strategy Implementation Support","Quarterly support for organizations executing a plan. Performance measurement, course correction, and accountability facilitation.",False),
          ("Sales Enablement","Strategy only creates value when your revenue team can execute it. We build the playbooks, messaging, training, and tools that align sales and marketing and shorten the path from plan to revenue. You build durable capability, not a dependency on us.",True),
          ("Regulatory Strategy Integration","Compliance built into the plan rather than bolted on. EDSTA, PHIPA, sector regulations, and funder expectations, addressed proactively.",False)]),
        ("innovation","03","Business Model Innovation &amp; Organizational Design",
         "The model that got you here will not get you there. At some point optimization is not enough, and you need to stress-test the business model itself and design for the next version of your organization.",
         "Unlike firms that optimize the status quo, we help you design what comes next, with the governance to get there.", False,
         [("Business Model Innovation","Stress-test and evolve your model with ecosystem mapping, scenario analysis, revenue design, and governance recommendations.",False),
          ("Organizational Design","Structures that fit strategy. Roles, reporting, decision rights, and governance mechanisms that let you execute.",False),
          ("Governance Framework Design","Clear, not bureaucratic. Decision rights, accountability, and reporting for boards, committees, and leadership teams.",False),
          ("Ecosystem Analysis","A deep read of your competitive landscape, partner ecosystem, and market dynamics, with the strategic implications drawn out.",False)]),
        ("digital","04","Digital Strategy &amp; Responsible Innovation",
         "Technology is one tool among many. We start with your organizational reality, then design a digital strategy your people can actually execute. AI governance, shadow AI audits, workflow automation, and algorithm impact assessments, with responsible practice built in from day one.",
         "Unlike vendors selling a single tool, we build governance in from the start, not after something goes wrong.", True,
         [("Shadow AI Audit &amp; Migration Sprint","Find every AI tool in use, authorized or not. Assess the exposure and build a governed migration path to sanctioned alternatives.",False),
          ("Responsible AI Prototyping + Algorithm Impact Assessment","A formal assessment aligned to EDSTA and IPC-OHRC principles, paired with responsible prototyping of the systems you intend to use.",False),
          ("Workflow Redesign Lab","Redesign workflows with AI integrated responsibly. Copilot or equivalent deployment, with governance and training built in.",False),
          ("Responsible Innovation Execution System","Ongoing support as AI evolves. Quarterly reviews, policy updates, incident response, and strategic guidance, on retainer.",False)]),
    ]
    out = hero
    for did,num,title,intro,unlike,alt,svcs in DOM:
        altcls = " section--alt" if alt else ""
        cards = "".join(svc(t,x,f) for t,x,f in svcs)
        extra = ""
        if did == "digital":
            extra = (f'<div class="assessband assessband--inline" data-r style="margin-top:36px">'
             f'<div class="assessband__txt"><h3>Not sure where to start?</h3>'
             f'<p>Take the Agentic Readiness Assessment. It maps your organization onto the agentic AI stages and scores you across tools, workflow, governance, infrastructure, and strategy, with a tailored next step in about two minutes.</p></div>'
             f'<div class="assessband__act"><a href="{AIURL}/assessment.html" class="btn btn-primary">Take the assessment {A}</a>'
             f'<a href="{AIURL}/brief.html" class="textlink" style="margin-top:14px">Read the Agentic AI Executive Brief {A}</a></div></div>')
        if did == "innovation":
            extra = (f'<div class="assessband assessband--inline" data-r style="margin-top:36px">'
             f'<div class="assessband__txt"><h3>Rethinking your model for the agentic era?</h3>'
             f'<p>The Agentic AI Executive Brief lays out the MIT CISR framework for the agentic era, with a stage self-check and what each transition actually requires of your model and your organization. Written for leaders.</p></div>'
             f'<div class="assessband__act"><a href="{AIURL}/brief.html" class="btn btn-primary">Read the brief {A}</a></div></div>')
        out += f'''<section class="section{altcls}" id="{did}"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">Domain {num}</p>
<h2>{title}</h2><p class="section__intro">{intro}</p>
<p style="font-size:15px;color:var(--muted);font-style:italic;margin-top:14px;max-width:700px">{unlike}</p></div>
<div class="cards cards--2">{cards}</div>{extra}</div></section>
'''
    process = f'''<section class="section section--dark"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head" style="color:var(--red)">How we work</p>
<h2>Diagnose. Design. Facilitate. Build. Sustain.</h2></div>
<div class="steps steps--5">
<div class="step" data-r><div class="step__n">1</div><h3>Diagnose</h3><p>Understand what is really happening in your organization.</p></div>
<div class="step" data-r data-rd="1"><div class="step__n">2</div><h3>Design</h3><p>Bespoke programs for your specific situation.</p></div>
<div class="step" data-r data-rd="2"><div class="step__n">3</div><h3>Facilitate</h3><p>Learning labs, workshops, coaching, change management.</p></div>
<div class="step" data-r data-rd="3"><div class="step__n">4</div><h3>Build</h3><p>Systems, workflows, and governance, with partners as needed.</p></div>
<div class="step" data-r data-rd="4"><div class="step__n">5</div><h3>Sustain</h3><p>Retainers, quarterly reviews, continuous improvement.</p></div>
</div></div></section>
'''
    cta = c.cta_red("Get clarity on your transformation priorities",
        "Every engagement starts with an Ecosystem Mapping Session. Book one and leave with a clear recommendation on where to focus first.",
        "Book your Ecosystem Mapping Session", f"{WWW}/contact.html")
    c.write("www","services.html","Services | CINTA & Co.",
        "Four integrated domains: Leadership and Transformation, Strategic Planning, Business Model Innovation, and Digital Strategy and Responsible Innovation.",
        c.header_www("Services"), out+process+cta)

# ============================================================ CONTACT
def contact():
    hero = f'''<section class="pagehero"><div class="pagehero__accent"></div>
<div class="wrap pagehero__in">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">Start here</span></div>
<h1 id="book-h1" data-r data-rd="1">Get clarity on your <span class="accent">transformation priorities</span></h1>
<p id="book-sub" class="pagehero__sub" data-r data-rd="2">Every engagement begins with an Ecosystem Mapping Session, a focused diagnostic that maps your organization and gives you a clear recommendation for where to act first.</p></div></section>
'''
    SECTORS = ["Education","Sports &amp; Recreation","Social Impact","Health &amp; Wellness",
      "Entrepreneurship","Building Materials &amp; Manufacturing","Ministry","School Board",
      "Hospital/Health","Municipality","Crown Agency","Other"]
    TIMEFRAMES = ["This week","Within two weeks","This month","Flexible"]
    secopts = "".join(f'<option>{s}</option>' for s in SECTORS)
    tfopts = "".join(f'<option>{t}</option>' for t in TIMEFRAMES)
    def field(nm,lab,ty,ph,req):
        return (f'<label class="fld"><span class="fld__l">{lab}{" *" if req else ""}</span>'
         f'<input type="{ty}" name="{nm}" placeholder="{ph}"{" required" if req else ""}></label>')
    formfields = (
     field("contact_name","Your name","text","Jane Doe",True)+
     field("contact_email","Work email","email","jane@organization.ca",True)+
     field("org_name","Organization","text","Organization name",True)+
     field("website","Website","url","https://organization.ca",False)+
     f'<label class="fld"><span class="fld__l">Sector *</span><select name="sector" required>{secopts}</select></label>'+
     field("role","Your role","text","Executive Director, VP, Director…",False)+
     f'<label class="fld"><span class="fld__l">Ideal timing</span><select name="desired_timeframe">{tfopts}</select></label>')
    body = f'''<section class="section"><div class="wrap"><div class="split">
<div data-r>
<h2 id="book-left-h2">The Ecosystem Mapping Session</h2>
<p>Ninety minutes with a senior practitioner. We map your landscape, surface the pressures that matter most, and give you a clear read on priority actions. Some leaders take that clarity and run with it. Most decide they want a partner for the journey. Either outcome is a good one.</p>
<ul class="checklist">
<li>{icon("check")} A clear map of your current ecosystem and pressure points</li>
<li>{icon("check")} Priorities ranked by impact and readiness, not noise</li>
<li>{icon("check")} A concrete recommendation you can act on, with or without us</li></ul>
<div class="panel-dark" style="margin-top:8px">
<p class="card__eyebrow" id="book-panel-eb">Ecosystem Mapping Session</p>
<h3 id="book-panel-h3">A 90-minute diagnostic with a senior practitioner</h3>
<p>Submit the form and we confirm your session by email, with the calendar invite and your intake folder. Priority-sector bookings are scheduled automatically.</p>
<div class="panel-dark__meta">
<div><div class="panel-dark__meta-n">90<span class="u"> min</span></div><div class="panel-dark__meta-l">Focused session</div></div>
<div><div class="panel-dark__meta-n">1:1</div><div class="panel-dark__meta-l">Senior practitioner</div></div>
<div><div class="panel-dark__meta-n">24<span class="u"> h</span></div><div class="panel-dark__meta-l">Confirmation by email</div></div>
</div></div></div>
<div data-r data-rd="1">
<div class="embed"><div class="embed__head"><p class="embed__head-t">Book your session</p>
<p class="embed__head-s">A few details and we take care of the scheduling.</p>
<p id="book-focus" style="display:none;margin-top:10px;font-weight:700;color:#fff;font-size:14px"></p></div>
<div style="padding:32px;background:#fff">
<form id="book-form" novalidate>{formfields}
<button type="submit" class="btn btn-primary btn-lg" style="width:100%;justify-content:center;margin-top:6px">Book your session {A}</button>
<p id="book-fallback" style="font-size:12.5px;color:var(--muted);margin-top:16px;text-align:center">Prefer email? <a href="mailto:info@cintaconsulting.com?subject=Ecosystem%20Mapping%20Session" class="textlink" style="display:inline">info@cintaconsulting.com</a></p>
</form>
<div id="book-ok" style="display:none;text-align:center;padding:24px 8px">
<div class="icon-well" style="width:56px;height:56px;margin:0 auto 20px">{icon("check")}</div>
<h3 style="font-size:20px;margin-bottom:10px">Request received</h3>
<p style="font-size:15px;color:var(--muted);line-height:1.6">Thank you. We will confirm your session by email, with the calendar invite and your intake folder, within one business day.</p>
</div></div></div></div>
</div></div>
<style>
.fld{{display:block;margin-bottom:16px}}
.fld__l{{display:block;font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px}}
.fld input,.fld select{{width:100%;padding:12px 14px;border:1px solid var(--gray);border-radius:var(--r-btn);font-family:var(--ff);font-size:15px;color:var(--text);background:#fff}}
.fld input:focus,.fld select:focus{{outline:none;border-color:var(--red);box-shadow:0 0 0 3px var(--red-tint)}}
</style>
<script>
(function(){{
  var WEBHOOK = {c.BOOKING_WEBHOOK!r};
  var f=document.getElementById("book-form");if(!f)return;
  function uuid(){{return 'web-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8);}}
  // Carry service/sector context from the CTA link into the booking
  var params=new URLSearchParams(location.search);
  var svc=params.get("service"), sec=params.get("sector");
  function setHero(focus,sub){{
    var h=document.getElementById("book-h1");
    if(h){{h.textContent="Let's talk about ";var s=document.createElement("span");s.className="accent";s.textContent=focus;h.appendChild(s);}}
    var p=document.getElementById("book-sub");if(p)p.textContent=sub;
  }}
  function showFocus(t){{var fo=document.getElementById("book-focus");if(fo){{fo.textContent="Focus: "+t;fo.style.display="block";}}}}
  if(svc){{
    showFocus(svc);
    var hid=document.createElement("input");hid.type="hidden";hid.name="service_interest";hid.value=svc;f.appendChild(hid);
    setHero(svc,"Ninety minutes with a senior practitioner to scope your "+svc+" priorities, surface what is in the way, and leave you with a clear recommendation on where to start.");
    var e;
    if(e=document.getElementById("book-left-h2")) e.textContent="Scoping your "+svc;
    if(e=document.getElementById("book-panel-eb")) e.textContent=svc+" scoping session";
    if(e=document.getElementById("book-panel-h3")) e.textContent="A focused 90-minute session with a senior practitioner";
  }}
  if(sec){{
    var sel=f.querySelector("select[name=sector]");
    if(sel){{for(var i=0;i<sel.options.length;i++){{if(sel.options[i].text.replace(/&amp;/g,"&")===sec){{sel.selectedIndex=i;break;}}}}}}
    showFocus(sec);
    setHero(sec,"Every CINTA engagement starts with a 90-minute Ecosystem Mapping Session, a focused diagnostic tailored to organizations like yours in "+sec+". Tell us about your priorities and we take care of the scheduling.");
  }}
  f.addEventListener("submit",function(e){{
    e.preventDefault();
    if(!f.checkValidity()){{f.reportValidity();return;}}
    var btn=f.querySelector("button[type=submit]");btn.disabled=true;btn.style.opacity=.6;
    var d=Object.fromEntries(new FormData(f).entries());
    d.persona="";                       // workflow derives persona from role when blank
    d.submitted_at=new Date().toISOString();
    d.response_id=uuid();
    // Fire-and-forget to the Apps Script web app, which books the calendar event
    // and emails the confirmation. no-cors keeps the default text/plain body that
    // Apps Script reads as e.postData.contents (no preflight, no CORS setup needed).
    // GA4 key event + Google Ads conversion. Carries the service, never personal fields.
    if(window.gtag){{gtag("event","generate_lead",{{form_name:"contact-booking",lead_intent:"booking",service:(new URLSearchParams(location.search).get("service")||"ecosystem-mapping"),page_host:location.hostname}});}}
    fetch(WEBHOOK,{{method:"POST",mode:"no-cors",body:JSON.stringify(d)}})
      .catch(function(){{}})
      .finally(function(){{
        f.style.display="none";
        document.getElementById("book-ok").style.display="block";
      }});
  }});
}})();
</script>
'''
    c.write("www","contact.html","Contact | CINTA & Co.",
        "Book an Ecosystem Mapping Session with CINTA & Co. Ninety minutes with a senior practitioner to map your situation and identify priority actions.",
        c.header_www(), hero+body)

# ============================================================ PRIVACY + TERMS
def legal(slug, title, intro, sections, desc=None):
    hero = f'''<section class="pagehero"><div class="wrap pagehero__in">
<div class="kicker"><span class="kicker__bar"></span><span class="kicker__txt">{title}</span></div>
<h1>{title}</h1><p class="pagehero__sub">{intro}</p></div></section>
'''
    def _block(h, ps):
        # A paragraph that already starts with a tag (e.g. a <ul>) is emitted
        # as-is; plain text is wrapped in <p>.
        inner = "".join(p if p.lstrip().startswith("<") else f"<p>{p}</p>" for p in ps)
        return f"<h2>{h}</h2>{inner}"
    blocks = "".join(_block(h, ps) for h, ps in sections)
    body = f'<section class="section"><div class="wrap"><div class="prose">{blocks}</div></div></section>'
    c.write("www",f"{slug}.html",f"{title} | CINTA & Co.",
        desc or f"{title} for CINTA & Co.", c.header_www(), hero+body)

def privacy():
    legal("privacy","Privacy policy",
      "How CINTA &amp; Co. collects, uses, and protects your personal information. Last updated November 2026.",
      [
       ("Who this covers",[
         "CINTA &amp; Co. is a consulting firm based in Toronto, Ontario, Canada. This policy explains how we handle personal information across our public websites, including cintaconsulting.com, our Insights blog, the CINTA AI marketing site, and our Responsible AI pages.",
         "If you are a client using the CINTA AI marketing platform itself, the data inside that platform is governed by the separate agreement we sign with you, not by this website policy.",
         "Questions about this policy, or about the information we hold on you, can go to <a href='mailto:info@cintaconsulting.com'>info@cintaconsulting.com</a>."]),
       ("What we collect",[
         "We collect two kinds of information.",
         "The first is what you give us directly. When you book a session, request an assessment result, or contact us, we collect your name, your work email, your organization, and anything else you choose to type into a form, including your answers to an assessment and the result it produces.",
         "The second is basic technical information your browser sends on its own, such as your IP address, device and browser type, and the pages you view. This sits in standard server logs and helps us keep the site secure and working.",
         "Our pages also load fonts from Google Fonts, which means Google receives the IP address of the request when a page loads."]),
       ("Cookies and analytics",[
         "We use Google Analytics to understand how people find and use our site, and Google Ads conversion tracking to see which of our campaigns lead to an inquiry. These Google tools set cookies and collect usage information, such as the pages you view, your approximate location, and the device and browser you use. We set our form tracking to record only the type of request, never the personal details you type into a form.",
         "You can turn this off. Most browsers let you block or clear cookies, and Google offers an opt-out add-on that applies across every site, at <a href='https://tools.google.com/dlpage/gaoptout' target='_blank' rel='noopener'>tools.google.com/dlpage/gaoptout</a>. Essential cookies that make the site work are not affected."]),
       ("How we use it",[
         "We use your information to:",
         "<ul><li>reply to you and answer what you asked;</li><li>send the assessment result or action plan you requested;</li><li>schedule, confirm, and follow up on sessions you book;</li><li>tell you about services and insights where you have agreed to hear from us;</li><li>keep the site secure and make it better over time.</li></ul>",
         "When a business inquiry comes in, we may prepare a short background summary of your organization from publicly available web information, so the person who follows up is prepared. We do not sell your personal information to anyone, for any purpose."]),
       ("Email and your consent",[
         "We send marketing email only where you have given consent or where Canadian anti-spam law otherwise allows it, for example when you asked us for something or we already have a business relationship with you. Every such email identifies us and carries an unsubscribe link. Use it any time and we stop."]),
       ("Service providers we rely on",[
         "We do not sell personal information. To run the site and our follow-up, we use a small set of trusted providers that process information on our behalf:",
         "<ul><li>Google Workspace, which handles our web form submissions, scheduling, email, and related storage;</li><li>Google Analytics and Google Ads, which measure how the site is used and how our campaigns perform;</li><li>Anthropic (the Claude API), which generates the short organization background summary described above.</li></ul>",
         "We also share your information with the specialists we engage to serve you, and only to the extent they need it to do that work."]),
       ("Where your information is processed",[
         "Some of these providers operate in the United States, so your information may be stored or processed outside Canada. When that happens, it can be subject to the laws of the country where it is held, including lawful access by courts and authorities there."]),
       ("Your rights",[
         "Under Canadian privacy law you can:",
         "<ul><li>ask what personal information we hold about you;</li><li>ask us to correct it;</li><li>withdraw your consent to our use of it;</li><li>ask us to delete it.</li></ul>",
         "Email <a href='mailto:info@cintaconsulting.com'>info@cintaconsulting.com</a> and we will respond within a reasonable time, and no later than 30 days. If you are not satisfied with how we handle a concern, you can contact the <a href='https://www.priv.gc.ca/' target='_blank' rel='noopener'>Office of the Privacy Commissioner of Canada</a>."]),
       ("Security and retention",[
         "We take reasonable measures to protect your information, and we keep it only as long as we need it for the purposes in this policy or as the law requires. No system is perfectly secure, so we cannot promise absolute security, but we work to reduce the risk."]),
       ("Children",[
         "Our site and services are meant for organizations and the professionals who run them. They are not directed to children, and we do not knowingly collect personal information from them."]),
       ("Changes to this policy",[
         "We may update this policy as our practices or the law change. The date at the top shows when it last changed, and we will flag anything significant."]),
      ])

def terms():
    legal("terms","Terms of use",
      "The terms that govern your use of the CINTA &amp; Co. website. Last updated November 2026.",
      [
       ("Using this site",[
         "This website gives general information about CINTA &amp; Co. and our services. By using it, you agree to these terms. If you do not agree, please do not use the site."]),
       ("Our content and brand",[
         "The content here, including text, design, and the CINTA &amp; Co. brand marks, belongs to us unless we say otherwise. You are welcome to read and share it. You may not reproduce it as your own or use our brand marks without written permission."]),
       ("Assessments and tools",[
         "Our site offers assessments and tools, and some of them produce AI-generated results. These exist to help you think, not to guarantee an outcome. A result is general information based on the answers you give. It is not a professional opinion tailored to your organization, and you should not treat it as one."]),
       ("No professional advice",[
         "Nothing on this site is a substitute for advice suited to your own situation. For guidance specific to your organization, book a session and speak with us directly."]),
       ("Booking and contact",[
         "When you book a session or send us a form, you agree that we may contact you to arrange it and to follow up. How we handle the information you share is set out in our <a href='/privacy.html'>privacy policy</a>."]),
       ("Other sites and the CINTA AI platform",[
         "Our site links to other properties and partners, including the CINTA AI marketing site, our Responsible AI practice with CoCr8 Labs, and our Insights blog. We are not responsible for the content of sites we do not control. Use of the CINTA AI marketing platform itself is governed by the separate agreement we sign with clients, not by these terms."]),
       ("The site is provided as is",[
         "We work to keep the site accurate and available, but we provide it as is, without warranties of any kind. To the extent the law allows, CINTA &amp; Co. is not liable for indirect or consequential loss arising from your use of the site or from anything you rely on here."]),
       ("Governing law",[
         "These terms are governed by the laws of the Province of Ontario and the laws of Canada that apply there. Any dispute about them belongs to the courts of Ontario."]),
       ("Changes and contact",[
         "We may update these terms from time to time, and the date at the top shows when they last changed. Questions can go to <a href='mailto:info@cintaconsulting.com'>info@cintaconsulting.com</a>."]),
      ])

if __name__ == "__main__":
    home(); about(); sectors(); services(); contact(); privacy(); terms()
    print("www: all 7 pages written")
