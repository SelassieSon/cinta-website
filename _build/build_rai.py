# -*- coding: utf-8 -*-
import common as c
from common import icon, RAI, WWW
A = icon("arrow")
SCOPE = '#scope'   # same-page lead-capture form (see scope_form)
HDR = lambda: c.header_dark(f"{RAI}/#services", "Request a scope", SCOPE)

def scope_form(service):
    form = c.embed_form(
      "scope-form",
      "Request a scope",
      "Tell us your context and we'll come back within one business day.",
      (c.fld("contact_name","Your name","text","Jane Doe",True)+
       c.fld("contact_email","Work email","email","jane@organization.ca",True)+
       c.fld("org_name","Organization","text","Organization name",True)+
       c.fld("website","Website","url","https://organization.ca",False)+
       c.sel("sector","Sector",["Education","School Board","Post-secondary",
         "Health / Hospital","Municipality","Ministry / Government",
         "Non-profit / Social Impact","Sports & Recreation","Other"],False)+
       c.fld("role","Your role","text","Executive Director, CISO, Privacy Lead…",False)+
       c.ta("message","What would you like scoped?",
         "Your AI use cases, obligations, timelines, or the questions you're weighing…",False,4)),
      "Request a scope",
      "Request received",
      "Thank you. A member of the CoCr8 &times; CINTA Responsible AI team will be in touch within one business day to scope next steps.",
      intent="lead", hidden={"service_interest": service},
      fallback_subject="Responsible%20AI%20-%20Scoping%20Request")
    return (f'<section class="section section--alt" id="scope"><div class="wrap"><div class="split">'
     f'<div data-r><p class="eyebrow section-head">Start here</p>'
     f'<h2>Request a scope</h2>'
     f'<p>No cost, no commitment. Share your context and we map your obligations, your exposure, '
     f'and the right first engagement, sized to where you actually are.</p>'
     f'<ul class="checklist">'
     f'<li>{icon("check")} A read on your obligations under EDSTA and IPC-OHRC principles</li>'
     f'<li>{icon("check")} The exposure that matters most, in plain language</li>'
     f'<li>{icon("check")} A recommended first engagement, sized to your capacity</li></ul></div>'
     f'<div data-r data-rd="1">{form}</div></div></div></section>\n')

def lander(folder, nav_title, page_title, desc, eyebrow, h1_lead, h1_accent, sub,
           context_intro, steps, includes, why_intro, why_points):
    alert = (f'<div class="alert"><p><strong>January 2026:</strong> The IPC and OHRC '
     f'released joint Principles for the Responsible Use of AI, the de facto assessment '
     f'standard for Ontario\'s broader public sector. '
     f'<a href="https://www.ipc.on.ca" target="_blank" rel="noopener">Read the principles {A}</a></p></div>\n')
    hero = f'''<section class="darkhero"><div class="wrap">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">{eyebrow}</span></div>
<h1 data-r data-rd="1">{h1_lead} <span class="accent">{h1_accent}</span></h1>
<p class="darkhero__sub" data-r data-rd="2">{sub}</p>
<div class="darkhero__actions" data-r data-rd="3">
<a href="{SCOPE}" class="btn btn-primary btn-lg">Request a scope {A}</a>
<a href="#how-it-works" class="btn" style="background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)">How it works</a></div>
<div class="darkhero__quote" data-r><p>"Governance is not a constraint. It is the enabler of sustainable innovation."</p>
<span>CoCr8 Labs × CINTA &amp; Co.</span></div></div></section>
'''
    ctx = f'''<section class="section"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">Why this, why now</p>
<h2>{nav_title}</h2><p class="section__intro">{context_intro}</p></div></div></section>
'''
    stepcards = "".join(
        f'<div class="step" data-r data-rd="{i}"><div class="step__n">{i+1}</div>'
        f'<h3>{t}</h3><p>{x}</p></div>' for i,(t,x) in enumerate(steps))
    how = f'''<section class="section section--dark" id="how-it-works"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head" style="color:var(--red)">Our approach</p>
<h2>How it works</h2></div><div class="steps steps--4">{stepcards}</div></div></section>
'''
    inc = "".join(f'<li>{icon("check")} {x}</li>' for x in includes)
    whatsin = f'''<section class="section"><div class="wrap"><div class="split split--center">
<div data-r><p class="eyebrow section-head">What you get</p>
<h2>Built in, not bolted on</h2>
<p>Responsible practice is designed into the work from the first day, not reviewed at the end. Here is what a typical engagement includes.</p>
<ul class="checklist">{inc}</ul></div>
<div class="panel-dark" data-r data-rd="1"><p class="card__eyebrow">CoCr8 Labs × CINTA &amp; Co.</p>
<h3>Governance expertise meets sector knowledge</h3>
<p>Pure-play AI governance firms know the technical side. They may not know how a faculty senate works, why a health organization\'s exposure differs from a ministry\'s, or how a non-profit board weighs risk. We bring both.</p>
<div class="panel-dark__meta">
<div><div class="panel-dark__meta-n">EDSTA</div><div class="panel-dark__meta-l">Aligned</div></div>
<div><div class="panel-dark__meta-n">IPC<span class="u">-OHRC</span></div><div class="panel-dark__meta-l">Principles</div></div>
<div><div class="panel-dark__meta-n">PHIPA</div><div class="panel-dark__meta-l">Where it applies</div></div>
</div></div></div></div></section>
'''
    wp = "".join(f'<div class="diff"><span class="red-bullet"></span><div><h3>{t}</h3><p>{x}</p></div></div>' for t,x in why_points)
    why = f'''<section class="section section--alt"><div class="wrap"><div class="split">
<div data-r><p class="eyebrow section-head">Why CoCr8 × CINTA</p>
<h2>We do not just know the regulations. We know your sector.</h2>
<p>{why_intro}</p></div>
<div class="diffs" data-r data-rd="1">{wp}</div></div></div></section>
'''
    cta = (f'<section class="cta-red"><div class="wrap">'
     f'<div class="cta-red__logo">CoCr8 Labs × CINTA &amp; Co.</div>'
     f'<div class="cta-red__tag">Responsible AI</div>'
     f'<h2 data-r>Ready to move from exposure to governance?</h2>'
     f'<p class="cta-red__sub" data-r data-rd="1">Request a scope and we will map your context, your obligations, and the right first engagement.</p>'
     f'<a href="{SCOPE}" class="btn btn-on-red btn-lg" data-r data-rd="2">Request a scope {A}</a>'
     f'</div></section>\n')
    body = alert+hero+ctx+how+whatsin+why+cta+scope_form(nav_title)
    c.write(folder,"index.html",page_title,desc,HDR(),body,cobrand=True)

# ---------------- HUB ----------------
def hub():
    alert = (f'<div class="alert"><p><strong>January 2026:</strong> The IPC and OHRC '
     f'released joint Principles for the Responsible Use of AI. '
     f'<a href="https://www.ipc.on.ca" target="_blank" rel="noopener">Read the principles {A}</a></p></div>\n')
    hero = f'''<section class="darkhero"><div class="wrap">
<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">From policy to practice</span></div>
<h1 data-r data-rd="1">Operationalizing <span class="accent">Responsible AI</span></h1>
<p class="darkhero__sub" data-r data-rd="2">Your people are already using AI. The question is not whether to govern it. It is whether you govern it before or after something goes wrong.</p>
<div class="darkhero__actions" data-r data-rd="3">
<a href="#services" class="btn btn-primary btn-lg">See the offers {A}</a>
<a href="{RAI}/readiness.html" class="btn" style="background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)">Take the 2-minute readiness check</a></div>
<div class="darkhero__quote" data-r><p>"Governance is not a constraint. It is the enabler of sustainable innovation."</p>
<span>CoCr8 Labs × CINTA &amp; Co.</span></div></div></section>
'''
    ctxcards = "".join(
        f'<div class="card" data-r data-rd="{i}"><div class="card__icon icon-well">{icon(ic)}</div>'
        f'<h3>{t}</h3><p class="card__txt">{x}</p></div>'
        for i,(ic,t,x) in enumerate([
         ("search","Shadow AI is everywhere","Employees adopt tools faster than policy can keep up. The exposure is already in your organization, whether or not you can see it."),
         ("scale","Regulation is accelerating","EDSTA in force since January 2025. IPC-OHRC principles published January 2026. Ontario\'s Responsible Use of AI Directive is live."),
         ("building","Boards are asking","Leadership now owns AI decisions personally. Silence at the board table is no longer a defensible position."),
         ("chart","A competitive opening","Organizations that govern well move faster, not slower. A clear framework enables confident adoption instead of paralysis.")]))
    ctx = f'''<section class="section"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">Why this, why now</p>
<h2>The pressure is real, and it is intensifying</h2>
<p class="section__intro">Four compounding forces are pushing mid-market organizations to act on AI governance.</p></div>
<div class="cards cards--4">{ctxcards}</div></div></section>
'''
    svcs = [
     ("ecosystem","map","Ecosystem Mapping Session","A 90-minute diagnostic that maps your AI exposure, your obligations, and your highest-priority governance gaps. The entry point to everything below.","https://ecosystem.cintaconsulting.com"),
     ("aia","clipboard","Responsible AI Prototyping + Algorithm Impact Assessment","A formal assessment aligned to EDSTA and IPC-OHRC principles, paired with responsible prototyping of the systems you intend to use.","https://aia.cintaconsulting.com"),
     ("workflow","workflow","Copilot Workflow Redesign","Redesign workflows with AI integrated responsibly. Copilot or equivalent deployment, with governance and training built in from the start.","https://workflow.cintaconsulting.com"),
     ("execution","shield","Responsible AI Execution System","Ongoing governance as AI evolves. Quarterly reviews, policy updates, incident response, and strategic advisory, on retainer.","https://execution.cintaconsulting.com"),
    ]
    scards = "".join(
     f'<div class="card" data-r data-rd="{i}"><div class="card__icon icon-well">{icon(ic)}</div>'
     f'<h3>{t}</h3><p class="card__txt">{x}</p>'
     f'<a href="{h}" class="textlink">Learn more {A}</a></div>'
     for i,(sid,ic,t,x,h) in enumerate(svcs))
    services = f'''<section class="section section--alt" id="services"><div class="wrap">
<div class="section__head" data-r><p class="eyebrow section-head">The offers</p>
<h2>Four engagements, one continuum</h2>
<p class="section__intro">From a rapid diagnostic to an ongoing partnership. Each stands alone or sequences into the next.</p></div>
<div class="cards cards--2">{scards}</div></div></section>
'''
    regs = [("EDSTA","Enhancing Digital Security and Trust Act","In force since January 2025. Covers FIPPA and MFIPPA institutions, school boards, and children\'s aid societies."),
            ("IPC-OHRC","Principles for Responsible Use of AI","Published January 2026. Soft law, but the de facto assessment standard for the broader public sector."),
            ("FIPPA / MFIPPA","Freedom of Information and Protection of Privacy","In force. Increasingly relevant as AI systems process and decide using personal information."),
            ("PHIPA","Personal Health Information Protection Act","In force. Triggered by AI for intake, matching, and clinical decision support.")]
    regcards = "".join(
     f'<div class="card" data-r data-rd="{i}" style="border-left:4px solid var(--red)">'
     f'<h3 style="font-size:16px;color:var(--red)">{a}</h3>'
     f'<p style="font-size:13px;font-weight:500;color:var(--text);margin:6px 0 10px">{n}</p>'
     f'<p class="card__txt">{x}</p></div>' for i,(a,n,x) in enumerate(regs))
    regsec = f'''<section class="section"><div class="wrap">
<div class="section__head section__head--center" data-r><p class="eyebrow section-head">Regulatory landscape</p>
<h2>The compliance environment is not waiting for you</h2>
<p class="section__intro">These frameworks govern Ontario organizations. Each has AI implications, and most are already in force.</p></div>
<div class="cards cards--4">{regcards}</div></div></section>
'''
    cta = (f'<section class="cta-red"><div class="wrap">'
     f'<div class="cta-red__logo">CoCr8 Labs × CINTA &amp; Co.</div>'
     f'<div class="cta-red__tag">Responsible AI</div>'
     f'<h2 data-r>From panic to governance</h2>'
     f'<p class="cta-red__sub" data-r data-rd="1">Request a scope and we will map your context, your obligations, and the right first engagement.</p>'
     f'<a href="{SCOPE}" class="btn btn-on-red btn-lg" data-r data-rd="2">Request a scope {A}</a>'
     f'</div></section>\n')
    body = alert+hero+ctx+services+regsec+cta+scope_form("Responsible AI (general enquiry)")
    c.write("responsibleai","index.html","Responsible AI | CoCr8 Labs × CINTA & Co.",
     "Operationalizing Responsible AI for Ontario organizations. Shadow AI audits, Algorithm Impact Assessments, workflow redesign, and ongoing governance.",
     HDR(), body, cobrand=True)

def readiness():
    QS = [
     ("Do you know where AI is being used across your organization?",
      ["No idea","A rough sense","Mostly mapped","Fully inventoried"]),
     ("Do you have an approved AI use policy?",
      ["None","In draft","Approved, not enforced","Approved and enforced"]),
     ("Who owns AI decisions and accountability?",
      ["No one clearly","Scattered across teams","A working group","A named owner with a board mandate"]),
     ("How do you handle shadow AI (unsanctioned tools)?",
      ["Unaddressed","Aware, no action","Guidance issued","Monitored and governed"]),
     ("Have you assessed AI systems for bias and privacy impact?",
      ["Never","Informally","Some systems","Formal assessments where needed"]),
     ("How current are you on EDSTA and the IPC-OHRC principles?",
      ["Unfamiliar","Heard of them","Reviewing them","Actively aligned"]),
     ("Is there staff training on responsible AI use?",
      ["None","Ad hoc","Some teams","Organization-wide"]),
     ("How do you respond when an AI issue arises?",
      ["No process","Case by case","An informal playbook","Defined incident response"]),
    ]
    TIERS = [
     {"max":7,"t":"Exposed — start with a map","x":"AI is already in your organization, but it is ungoverned. The first move is a 90-minute Ecosystem Mapping Session to see your exposure and obligations before something goes wrong."},
     {"max":13,"t":"Reactive — formalize the basics","x":"You have awareness but not structure. A formal Algorithm Impact Assessment, plus an approved and enforced policy, closes the gaps that matter most."},
     {"max":19,"t":"Managing — tighten and sustain","x":"Good foundations, uneven in places. A Copilot Workflow Redesign and ongoing governance keep you current as regulation and tools keep moving."},
     {"max":24,"t":"Governed — stay ahead","x":"You run a mature practice. An Execution System retainer keeps it current with quarterly reviews, policy updates, and incident response."},
    ]
    c.assessment_page("responsibleai","readiness",
     "AI Governance Readiness Assessment | CoCr8 Labs × CINTA & Co.",
     "An 8-question check of your AI governance maturity against EDSTA and the IPC-OHRC principles, with a personalized next step.",
     HDR(), "AI governance readiness",
     "Is your organization ready to","govern AI?",
     "Eight questions, about two minutes. See where your AI governance stands against EDSTA and the IPC-OHRC principles, and what to shore up first.",
     QS, TIERS, "AI Governance Readiness Assessment",
     f"{RAI}/#scope", "Or request a full scope", cobrand=True)

if __name__ == "__main__":
    hub(); readiness()
    lander("ecosystem","Ecosystem Mapping Session","90-Minute Ecosystem Mapping Session | CoCr8 Labs × CINTA & Co.",
      "A 90-minute diagnostic that maps your AI exposure, obligations, and highest-priority governance gaps.",
      "Start here · 90-minute diagnostic",
      "See your AI exposure","clearly, in 90 minutes",
      "A focused session that maps where AI is used across your organization, what it exposes you to, and where to act first. The entry point to the Responsible AI practice.",
      "Most organizations are making AI decisions without a map. This session gives you one: a clear read on your exposure, your obligations under EDSTA and related frameworks, and the priority actions that follow.",
      [("Map","We map where AI is used across your organization, sanctioned or not."),
       ("Assess","We weigh the exposure by tool, use case, and the data involved."),
       ("Prioritize","We rank what matters by impact and readiness, not noise."),
       ("Recommend","You leave with a concrete recommendation and a clear next step.")],
      ["A map of your current AI footprint across departments","Exposure flagged by tool, use case, and data type","Your obligations under EDSTA and related frameworks","A prioritized, plain-language recommendation","A clear next engagement, if you want one"],
      "We have worked in education, health, sports, and social impact. We bring the governance expertise and the sector knowledge, and that combination is rare.",
      [("Neuroscience-informed","Governance that people actually adopt, designed for the human side of change."),
       ("Sector depth","We know how your organization operates, not just what the regulation says."),
       ("Mid-market right-sized","Purpose-built for 50 to 2,000 employees, not enterprise frameworks scaled down.")])
    lander("aia","Prototyping + AIA","Responsible AI Prototyping + Algorithm Impact Assessment | CoCr8 Labs × CINTA & Co.",
      "A formal Algorithm Impact Assessment aligned to EDSTA and IPC-OHRC principles, paired with responsible prototyping.",
      "Formal assessment · Responsible prototyping",
      "Prove it is safe","before you scale it",
      "A formal Algorithm Impact Assessment aligned to EDSTA and IPC-OHRC principles, paired with responsible prototyping of the systems you intend to use.",
      "Before an algorithmic system goes live, you need to know what it does to the people it touches. The AIA evaluates for bias, privacy impact, and human-rights implications, and prototyping lets you test responsibly before committing.",
      [("Inventory","We map the system, its use cases, and the data it relies on."),
       ("Assess","We evaluate for bias, privacy impact, and human-rights implications."),
       ("Prototype","We test the intended system responsibly, within the guardrails."),
       ("Report","You get a formal AIA and a mitigation roadmap you can act on.")],
      ["A formal Algorithm Impact Assessment report","Bias and fairness evaluation","Privacy impact analysis under FIPPA, MFIPPA, or PHIPA","Human-rights assessment aligned to OHRC guidance","Responsible prototype and a mitigation roadmap"],
      "An AIA is only useful if it reflects how your organization actually operates. We combine formal assessment rigour with real sector understanding.",
      [("EDSTA and IPC-OHRC aligned","Assessed against the standards your regulators actually use."),
       ("Prototyping, not just paperwork","Test the real system responsibly before you commit to it."),
       ("Mitigation you can run","A roadmap sized to your capacity, not a wish list.")])
    lander("workflow","Copilot Workflow Redesign","Copilot Workflow Redesign | CoCr8 Labs × CINTA & Co.",
      "Redesign workflows with AI integrated responsibly. Copilot or equivalent deployment, with governance and training built in.",
      "Workflow transformation · Governance built in",
      "Redesign the work,","not just the tool",
      "A structured lab that redesigns your workflows with AI integrated responsibly. Copilot or equivalent deployment, with governance, oversight, and training built in from the start.",
      "Dropping an AI tool onto a broken workflow just makes the breakage faster. We redesign the work itself, integrate AI where it genuinely helps, and build the oversight and training that make it stick on the floor.",
      [("Map","We map the current-state process, honestly, including the workarounds."),
       ("Design","We redesign the workflow with AI integrated and governance built in."),
       ("Deploy","Copilot or equivalent, with human oversight and escalation paths."),
       ("Embed","Change management and training so your people actually adopt it.")],
      ["Current-state process mapping","A redesigned workflow with AI integrated responsibly","Human oversight mechanisms and escalation paths","Staff training and change management","Implementation support and a post-launch review"],
      "Workflow change fails on the human side, not the technical one. Our neuroscience-informed approach is built for exactly that.",
      [("Human-side first","We design for adoption, because tools no one trusts get worked around."),
       ("Governance from day one","Oversight and escalation designed in, not patched on later."),
       ("Sector-aware","We know the operating reality your workflows actually run in.")])
    lander("execution","Execution System","Responsible AI Execution System | CoCr8 Labs × CINTA & Co.",
      "Ongoing governance as AI evolves. Quarterly reviews, policy updates, incident response, and strategic advisory, on retainer.",
      "Ongoing partnership · Retainer",
      "Governance that keeps up","as AI keeps moving",
      "A retainer-based system for organizations navigating continuous AI change. Quarterly reviews, policy updates as regulation evolves, incident response, and proactive advisory.",
      "AI governance is not a one-time project. Tools change, regulation moves, and new use cases appear every quarter. The Execution System keeps your governance current without pulling your team off its real work.",
      [("Review","Quarterly governance and policy reviews against what has changed."),
       ("Update","Policy and framework updates as regulation and tools evolve."),
       ("Respond","Incident response and advisory support when something comes up."),
       ("Advise","Proactive guidance on new tools, use cases, and board reporting.")],
      ["Quarterly governance and policy reviews","Regulatory monitoring and compliance updates","Incident response and advisory support","New AI tool evaluation and approval support","Board and leadership reporting templates"],
      "Sustained governance needs a partner who knows your organization over time, not a vendor who re-learns it every engagement.",
      [("Continuity","The same team, quarter over quarter, building institutional memory."),
       ("Always current","Policy that moves as EDSTA, IPC-OHRC, and your tools move."),
       ("Board-ready","Reporting that keeps leadership confident and accountable.")])
    print("responsibleai: hub + 4 landers written")
