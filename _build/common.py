# -*- coding: utf-8 -*-
"""Shared chrome + helpers for the CINTA & Co. static site generator."""
import os
import json as _json
import urllib.parse as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Lucide-style line icons (red via currentColor) -------------------------
_P = ('fill="none" stroke="currentColor" stroke-linecap="round" '
      'stroke-linejoin="round"')
ICONS = {
 "arrow":  f'<svg viewBox="0 0 24 24" {_P}><path d="M5 12h14M13 5l7 7-7 7"/></svg>',
 "check":  f'<svg viewBox="0 0 24 24" {_P}><path d="M20 6 9 17l-5-5"/></svg>',
 "brain":  f'<svg viewBox="0 0 24 24" {_P}><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>',
 "target": f'<svg viewBox="0 0 24 24" {_P}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/></svg>',
 "refresh":f'<svg viewBox="0 0 24 24" {_P}><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></svg>',
 "scale":  f'<svg viewBox="0 0 24 24" {_P}><path d="M12 3v18"/><path d="M6 21h12"/><path d="m3 7 4-1 4 1"/><path d="m13 7 4-1 4 1"/><path d="M3 7 1 13a3 3 0 0 0 6 0L5 7"/><path d="M21 7l-2 6a3 3 0 0 1-6 0l2-6"/></svg>',
 "cap":    f'<svg viewBox="0 0 24 24" {_P}><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1 2.7 2.5 6 2.5s6-1.5 6-2.5v-5"/></svg>',
 "trophy": f'<svg viewBox="0 0 24 24" {_P}><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>',
 "heart":  f'<svg viewBox="0 0 24 24" {_P}><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
 "cross":  f'<svg viewBox="0 0 24 24" {_P}><path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2Z"/></svg>',
 "rocket": f'<svg viewBox="0 0 24 24" {_P}><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09Z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2Z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
 "factory":f'<svg viewBox="0 0 24 24" {_P}><path d="M3 19a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9.5a.5.5 0 0 0-.77-.42l-4.46 2.84A.5.5 0 0 1 15 11.5v-2a.5.5 0 0 0-.77-.42L9.77 11.92A.5.5 0 0 1 9 11.5V5a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1Z"/><path d="M8 16h.01M12 16h.01M16 16h.01"/></svg>',
 "search": f'<svg viewBox="0 0 24 24" {_P}><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
 "shield": f'<svg viewBox="0 0 24 24" {_P}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
 "workflow":f'<svg viewBox="0 0 24 24" {_P}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><path d="M6.5 10v4a2 2 0 0 0 2 2h4"/></svg>',
 "zap":    f'<svg viewBox="0 0 24 24" {_P}><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/></svg>',
 "layers": f'<svg viewBox="0 0 24 24" {_P}><path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/></svg>',
 "users":  f'<svg viewBox="0 0 24 24" {_P}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13A4 4 0 0 1 16 11"/></svg>',
 "building":f'<svg viewBox="0 0 24 24" {_P}><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/></svg>',
 "clipboard":f'<svg viewBox="0 0 24 24" {_P}><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg>',
 "map":    f'<svg viewBox="0 0 24 24" {_P}><path d="M14.5 4 9 6 3.5 4 3 4.2v15l.5-.2L9 21l5.5-2L20.5 21l.5-.2v-15l-.5.2L15 4Z"/><path d="M9 6v15M15 4v15"/></svg>',
 "chart":  f'<svg viewBox="0 0 24 24" {_P}><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-4 4"/></svg>',
 "gauge":  f'<svg viewBox="0 0 24 24" {_P}><path d="M12 14 8.5 9.5"/><path d="M3.5 17a9 9 0 1 1 17 0"/><circle cx="12" cy="14" r="1.5" fill="currentColor" stroke="none"/></svg>',
 "clock":  f'<svg viewBox="0 0 24 24" {_P}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "download":f'<svg viewBox="0 0 24 24" {_P}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
 "handshake":f'<svg viewBox="0 0 24 24" {_P}><path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/></svg>',
 "linkedin":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm6 0h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.4c0-1.3 0-2.95-1.8-2.95s-2.08 1.4-2.08 2.85V21H9V9Z"/></svg>',
 "menu":   f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}
def icon(name): return ICONS[name]

# Booking endpoint — Google Apps Script web app (replaces n8n entirely).
# Deploy apps-script/Code.gs as a web app (see BOOKING-SETUP.md) and paste its
# /exec URL here, e.g. https://script.google.com/macros/s/AKfy.../exec
BOOKING_WEBHOOK = "https://script.google.com/macros/s/AKfycbyg4NZqVPgFFPaC4Nep-5UypZpW2YcH3nv0BmdgXqhAju8LmOgbm57YxAWS49WLAKOI/exec"

WWW   = "https://www.cintaconsulting.com"
RAI   = "https://responsibleai.cintaconsulting.com"
AIURL = "https://cintaai.cintaconsulting.com"
INS   = "https://insights.cintaconsulting.com"
LI    = "https://www.linkedin.com/company/cinta-andco"
FORM  = "https://docs.google.com/forms/d/e/1FAIpQLSeElHfF4-bxUZg1vnZYdgEuhAKRFK3o7_yHH0j3nSjUz1kCfg/viewform?embedded=true"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
 "viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' fill='%23D04747'/"
 "%3E%3Ctext x='16' y='23' font-family='Montserrat,Arial,sans-serif' "
 "font-size='21' font-weight='700' fill='white' text-anchor='middle'%3EC%3C/"
 "text%3E%3C/svg%3E")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,'
 'wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap" rel="stylesheet">')

def head(title, desc, css="site.css"):
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
     f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
     f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
     f'<link rel="icon" href="{FAVICON}">\n{FONTS}\n'
     f'<link rel="stylesheet" href="{css}">\n</head>\n<body>\n')

def _navlink(href, label, active):
    cur = ' aria-current="page"' if active == label else ''
    return f'<a href="{href}"{cur}>{label}</a>'

def header_www(active=""):
    links = "".join([
        _navlink(f"{WWW}/sectors.html","Sectors",active),
        _navlink(f"{WWW}/services.html","Services",active),
        _navlink(INS,"Insights",active),
        _navlink(f"{WWW}/about.html","About",active),
    ])
    cta = (f'<a href="{WWW}/contact.html" class="btn btn-primary">Book a session '
           f'{icon("arrow")}</a>')
    return (f'<header class="hdr"><div class="hdr__in">'
     f'<a href="{WWW}/" class="logo" aria-label="CINTA & Co. — Facilitating Success">'
     f'<span class="logo__name">CINTA &amp; Co.</span>'
     f'<span class="logo__tag">Facilitating Success</span></a>'
     f'<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" '
     f'aria-controls="nav">{icon("menu")}</button>'
     f'<nav class="nav" id="nav" aria-label="Primary">{links}{cta}</nav>'
     f'</div></header>\n')

def header_dark(offers_href, cta_label, cta_href, how="#how-it-works"):
    links = (f'<a href="{offers_href}">Offers</a>'
             f'<a href="{RAI}/readiness.html">Readiness check</a>'
             f'<a href="{how}">How it works</a>'
             f'<a href="{cta_href}" class="btn btn-primary">{cta_label} {icon("arrow")}</a>')
    return (f'<header class="hdr hdr--dark"><div class="hdr__in">'
     f'<a href="{WWW}/" class="logo cobrand" aria-label="CINTA & Co. — home">'
     f'<span class="logo__name">CINTA &amp; Co.</span>'
     f'<span class="cobrand__x">×</span>'
     f'<span class="cobrand__cocr8">CoCr8&nbsp;Labs</span></a>'
     f'<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" '
     f'aria-controls="nav">{icon("menu")}</button>'
     f'<nav class="nav" id="nav" aria-label="Primary">{links}</nav>'
     f'</div></header>\n')

def header_ai(active=""):
    links = (f'<a href="{AIURL}/#how">How it works</a>'
             f'<a href="{AIURL}/#platform">Platform</a>'
             f'<a href="{AIURL}/#plans">Plans</a>'
             f'<a href="{AIURL}/assessment.html">Assessment</a>'
             f'<a href="{AIURL}/#demo" class="btn btn-primary">Book a Demo {icon("arrow")}</a>')
    return (f'<header class="hdr"><div class="hdr__in">'
     f'<a href="{WWW}/" class="logo" aria-label="CINTA & Co. — Facilitating Success">'
     f'<span class="logo__name">CINTA &amp; Co.</span>'
     f'<span class="logo__tag">Facilitating Success</span></a>'
     f'<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" '
     f'aria-controls="nav">{icon("menu")}</button>'
     f'<nav class="nav" id="nav" aria-label="Primary">{links}</nav>'
     f'</div></header>\n')

def footer(cobrand=False):
    sectors = "".join(f'<a href="{WWW}/sectors.html#{s[0]}">{s[1]}</a>' for s in [
        ("education","Education"),("sports","Sports &amp; Recreation"),
        ("social-impact","Social Impact"),("health","Health &amp; Wellness"),
        ("entrepreneurship","Entrepreneurship"),
        ("building-materials","Building Materials &amp; Manufacturing")])
    services = "".join(f'<a href="{WWW}/services.html#{s[0]}">{s[1]}</a>' for s in [
        ("transformation","Leadership &amp; Transformation"),
        ("strategy","Strategic Planning"),
        ("sales-enablement","Sales Enablement"),
        ("innovation","Business Model Innovation"),
        ("digital","Digital Strategy")])
    company = (f'<a href="{WWW}/about.html">About &amp; team</a>'
     f'<a href="{INS}">Insights</a><a href="{AIURL}">CINTA AI Platform</a>'
     f'<a href="{RAI}">Responsible AI</a><a href="{WWW}/contact.html">Contact</a>')
    cob = (f'<p class="ftr__copy">A CoCr8 Labs × CINTA &amp; Co. partnership.</p>'
           if cobrand else '')
    return (f'<footer class="ftr"><div class="wrap"><div class="ftr__grid">'
     f'<div><div class="ftr__name">CINTA &amp; Co.</div>'
     f'<div class="ftr__tag">Facilitating Success</div>'
     f'<p class="ftr__desc">The consulting partner mid-market organizations trust '
     f'when the ground is shifting. Toronto, Ontario, Canada.</p>'
     f'<div class="ftr__social"><a href="{LI}" aria-label="CINTA &amp; Co. on LinkedIn" '
     f'target="_blank" rel="noopener">{icon("linkedin")}</a></div></div>'
     f'<div><p class="ftr__col-t">Sectors</p><div class="ftr__links">{sectors}</div></div>'
     f'<div><p class="ftr__col-t">Services</p><div class="ftr__links">{services}</div></div>'
     f'<div><p class="ftr__col-t">Company</p><div class="ftr__links">{company}</div></div>'
     f'</div><div class="ftr__bottom">'
     f'<p class="ftr__copy">© 2026 CINTA &amp; Co. All rights reserved.</p>{cob}'
     f'<div class="ftr__legal"><a href="{WWW}/privacy.html">Privacy policy</a>'
     f'<a href="{WWW}/terms.html">Terms of use</a></div></div></div></footer>\n')

SCRIPTS = ('<script>'
 '(function(){var e=document.querySelectorAll("[data-r]");'
 'if(!("IntersectionObserver"in window)||!e.length){e.forEach(function(x){x.classList.add("vis")});return;}'
 'var o=new IntersectionObserver(function(es){es.forEach(function(x){'
 'if(x.isIntersecting){x.target.classList.add("vis");o.unobserve(x.target);}})},'
 '{threshold:.12,rootMargin:"0px 0px -40px 0px"});e.forEach(function(x){o.observe(x)});})();'
 '(function(){var b=document.querySelector(".nav-toggle"),'
 'n=b&&document.getElementById(b.getAttribute("aria-controls"));if(!b||!n)return;'
 'b.addEventListener("click",function(){var o=n.classList.toggle("open");'
 'b.setAttribute("aria-expanded",o?"true":"false");'
 'b.setAttribute("aria-label",o?"Close menu":"Open menu");});})();'
 '</script>\n</body>\n</html>')

def write(prop, filename, title, desc, header_html, body, cobrand=False, css="site.css"):
    html = head(title, desc, css) + header_html + body + footer(cobrand) + SCRIPTS
    outdir = os.path.join(ROOT, prop)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.join(prop, filename)

# ---- booking / lead form helpers (shared across properties) ----
FORM_STYLE = ('<style>'
 '.fld{display:block;margin-bottom:16px}'
 '.fld__l{display:block;font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px}'
 '.fld input,.fld select,.fld textarea{width:100%;padding:12px 14px;border:1px solid var(--gray);'
 'border-radius:var(--r-btn);font-family:var(--ff);font-size:15px;color:var(--text);background:#fff}'
 '.fld textarea{resize:vertical}'
 '.fld input:focus,.fld select:focus,.fld textarea:focus{outline:none;border-color:var(--red);'
 'box-shadow:0 0 0 3px var(--red-tint)}'
 '</style>')

def fld(nm, lab, ty="text", ph="", req=False):
    return (f'<label class="fld"><span class="fld__l">{lab}{" *" if req else ""}</span>'
            f'<input type="{ty}" name="{nm}" placeholder="{ph}"{" required" if req else ""}></label>')

def sel(nm, lab, opts, req=False):
    o = "".join(f'<option>{x}</option>' for x in opts)
    return (f'<label class="fld"><span class="fld__l">{lab}{" *" if req else ""}</span>'
            f'<select name="{nm}"{" required" if req else ""}>{o}</select></label>')

def ta(nm, lab, ph="", req=False, rows=4):
    return (f'<label class="fld"><span class="fld__l">{lab}{" *" if req else ""}</span>'
            f'<textarea name="{nm}" rows="{rows}" placeholder="{ph}"{" required" if req else ""}></textarea></label>')

def _form_js(form_id, ok_id, intent):
    return ('<script>(function(){'
     'var WEBHOOK=' + repr(BOOKING_WEBHOOK) + ';'
     'var f=document.getElementById(' + repr(form_id) + ');if(!f)return;'
     'function uuid(){return "web-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,8);}'
     'f.addEventListener("submit",function(e){'
     'e.preventDefault();if(!f.checkValidity()){f.reportValidity();return;}'
     'var btn=f.querySelector("button[type=submit]");if(btn){btn.disabled=true;btn.style.opacity=.6;}'
     'var d=Object.fromEntries(new FormData(f).entries());'
     'd.intent=' + repr(intent) + ';d.persona="";d.submitted_at=new Date().toISOString();d.response_id=uuid();'
     'fetch(WEBHOOK,{method:"POST",mode:"no-cors",body:JSON.stringify(d)})'
     '.catch(function(){}).finally(function(){'
     'f.style.display="none";var ok=document.getElementById(' + repr(ok_id) + ');if(ok)ok.style.display="block";});'
     '});})();</script>')

def embed_form(form_id, head_t, head_s, fields_html, submit_label, ok_title, ok_text,
               intent="", hidden=None, fallback_subject=None, include_style=True):
    """Branded white-body card with a fire-and-forget form that POSTs to the
    Apps Script endpoint with the given intent ('' ecosystem, 'demo', 'lead')."""
    ok_id = form_id + "-ok"
    hid = ""
    if hidden:
        hid = "".join(f'<input type="hidden" name="{k}" value="{v}">' for k, v in hidden.items())
    fb = ""
    if fallback_subject:
        fb = (f'<p style="font-size:12.5px;color:var(--muted);margin-top:16px;text-align:center">'
              f'Prefer email? <a href="mailto:info@cintaconsulting.com?subject={fallback_subject}" '
              f'class="textlink" style="display:inline">info@cintaconsulting.com</a></p>')
    style = FORM_STYLE if include_style else ""
    return (f'<div class="embed"><div class="embed__head">'
     f'<p class="embed__head-t">{head_t}</p><p class="embed__head-s">{head_s}</p></div>'
     f'<div style="padding:32px;background:#fff">'
     f'<form id="{form_id}" novalidate>{hid}{fields_html}'
     f'<button type="submit" class="btn btn-primary btn-lg" style="width:100%;justify-content:center;margin-top:6px">{submit_label} {icon("arrow")}</button>'
     f'{fb}</form>'
     f'<div id="{ok_id}" style="display:none;text-align:center;padding:24px 8px">'
     f'<div class="icon-well" style="width:56px;height:56px;margin:0 auto 20px">{icon("check")}</div>'
     f'<h3 style="font-size:20px;margin-bottom:10px">{ok_title}</h3>'
     f'<p style="font-size:15px;color:var(--muted);line-height:1.6">{ok_text}</p>'
     f'</div></div></div>'
     f'{style}{_form_js(form_id, ok_id, intent)}')

# ---- interactive assessment (quiz + lead capture) ----
def assessment_page(prop, slug, title, desc, header_html, eyebrow, h1_lead, h1_accent,
                    intro, questions, tiers, service_tag, cta_href, cta_label,
                    cap_head="Get your personalized action plan",
                    cap_sub="Your result, plus the moves that matter most for where you landed.",
                    cobrand=False):
    """Generic multi-step assessment. `questions` is a list of (prompt, [options])
    scored by option index (0..n). `tiers` is a list of {max,t,x} ascending by max.
    The result captures a lead (name+email) to the Apps Script endpoint (intent=lead),
    tagged with service_tag and the computed result."""
    qjson = _json.dumps([{"q": q, "a": opts} for q, opts in questions])
    tjson = _json.dumps(tiers)
    maxscore = sum(len(opts) - 1 for q, opts in questions)
    msgid = slug + "-msg"
    resid, scoreid, planid = slug + "-res", slug + "-score", slug + "-plan"
    hero = ('<section class="darkhero" style="padding-bottom:56px"><div class="wrap">'
     '<div class="kicker" data-r><span class="kicker__bar"></span>'
     f'<span class="kicker__txt">{eyebrow}</span></div>'
     f'<h1 data-r data-rd="1">{h1_lead} <span class="accent">{h1_accent}</span></h1>'
     f'<p class="darkhero__sub" data-r data-rd="2">{intro}</p></div></section>')
    capture = embed_form(slug + "-cap", cap_head, cap_sub,
      (fld("contact_name", "Your name", "text", "Jane Doe", True) +
       fld("contact_email", "Work email", "email", "jane@organization.ca", True) +
       fld("org_name", "Organization", "text", "Organization name", False) +
       f'<input type="hidden" name="message" id="{msgid}">'
       f'<input type="hidden" name="assessment_result" id="{resid}">'
       f'<input type="hidden" name="assessment_score" id="{scoreid}">'
       f'<input type="hidden" name="action_plan" id="{planid}">'
       f'<input type="hidden" name="cta_url" value="{cta_href}">'
       f'<input type="hidden" name="cta_label" value="{cta_label}">'),
      "Email me my action plan", "On its way",
      "Thank you. Your full action plan is on its way to your inbox, and we will follow up within one business day.",
      intent="lead", hidden={"service_interest": service_tag},
      fallback_subject=_u.quote(service_tag))
    app = ('<section class="section"><div class="wrap" style="max-width:760px">'
     '<div id="asmt" data-r>'
     '<div id="bar" style="height:6px;background:var(--gray);border-radius:3px;overflow:hidden;margin-bottom:32px">'
     '<div id="fill" style="height:100%;width:12.5%;background:var(--red);transition:width .3s"></div></div>'
     '<div id="qbox"></div>'
     '<div style="display:flex;justify-content:space-between;margin-top:28px">'
     '<button id="prev" class="btn btn-secondary" style="visibility:hidden">Back</button>'
     '<button id="next" class="btn btn-primary" disabled>Next</button></div></div>'
     '<div id="result" style="display:none">'
     '<div style="text-align:center">'
     '<div class="icon-well" style="width:64px;height:64px;margin:0 auto 24px">' + icon("gauge") + '</div>'
     '<p class="eyebrow" style="justify-content:center">Your result</p>'
     '<h2 id="rtier" style="font-size:var(--fs-h1);margin:12px 0 16px"></h2>'
     '<p id="rtext" style="font-size:17px;color:var(--text-body);line-height:1.7;max-width:560px;margin:0 auto 24px"></p>'
     '<p style="font-size:13px;font-weight:600;color:var(--brown);letter-spacing:.05em;text-transform:uppercase;margin:0 0 10px">Your action plan</p>'
     '<ul id="rsteps"></ul>'
     '<style>#rsteps{list-style:none;padding:0;max-width:560px;margin:0 auto 26px;text-align:left}'
     '#rsteps li{position:relative;padding:10px 0 10px 28px;border-bottom:1px solid var(--gray);font-size:15px;color:var(--text-body)}'
     '#rsteps li:before{content:"";position:absolute;left:2px;top:17px;width:8px;height:8px;border-radius:50%;background:var(--red)}</style>'
     '</div>' + capture +
     f'<p style="text-align:center;margin-top:18px"><a href="{cta_href}" class="textlink">{cta_label}</a>'
     '  ·  <button id="restart" class="textlink" style="background:none;border:0;cursor:pointer;font:inherit;color:var(--red)">Start over</button></p>'
     '</div></div></section>')
    script = ('<script>(function(){'
     'var Q=' + qjson + ';var T=' + tjson + ';'
     'var MSGID=' + repr(msgid) + ',RESID=' + repr(resid) + ',SCOREID=' + repr(scoreid) + ',PLANID=' + repr(planid) + ',LABEL=' + repr(service_tag) + ',MAX=' + str(maxscore) + ';'
     'var i=0,ans=Array(Q.length).fill(-1);'
     'var qbox=document.getElementById("qbox"),fill=document.getElementById("fill"),'
     'nextB=document.getElementById("next"),prevB=document.getElementById("prev"),'
     'asmt=document.getElementById("asmt"),res=document.getElementById("result");'
     'function render(){var q=Q[i];'
     'var h=\'<p style="font-size:13px;font-weight:600;color:var(--brown);letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px">Question \'+(i+1)+\' of \'+Q.length+\'</p>\';'
     'h+=\'<h2 style="font-size:24px;margin-bottom:24px">\'+q.q+\'</h2><div style="display:flex;flex-direction:column;gap:12px">\';'
     'q.a.forEach(function(o,k){var sel=ans[i]===k;'
     'h+=\'<button class="opt" data-k="\'+k+\'" style="text-align:left;padding:16px 18px;border:1.5px solid \'+(sel?"var(--red)":"var(--gray)")+\';border-radius:var(--r-btn);background:\'+(sel?"var(--red-tint)":"#fff")+\';font-family:var(--ff);font-size:15px;color:var(--text);cursor:pointer;transition:all .15s">\'+o+\'</button>\';});'
     'h+=\'</div>\';qbox.innerHTML=h;'
     'fill.style.width=((i+1)/Q.length*100)+"%";'
     'prevB.style.visibility=i===0?"hidden":"visible";'
     'nextB.disabled=ans[i]<0;nextB.textContent=i===Q.length-1?"See result":"Next";'
     'Array.prototype.forEach.call(qbox.querySelectorAll(".opt"),function(b){b.onclick=function(){ans[i]=+b.dataset.k;render();};});}'
     'nextB.onclick=function(){if(ans[i]<0)return;if(i<Q.length-1){i++;render();}else{finish();}};'
     'prevB.onclick=function(){if(i>0){i--;render();}};'
     'function finish(){var s=ans.reduce(function(a,b){return a+b;},0);'
     'var r=T.find(function(z){return s<=z.max;})||T[T.length-1];'
     'asmt.style.display="none";res.style.display="block";'
     'document.getElementById("rtier").textContent=r.t;'
     'document.getElementById("rtext").textContent=r.x;'
     'var steps=r.steps||[];'
     'var ul=document.getElementById("rsteps");if(ul){ul.innerHTML=steps.map(function(x){return "<li>"+x+"</li>";}).join("");}'
     'var plan=r.x+(steps.length?("\\n\\n"+steps.map(function(x){return "- "+x;}).join("\\n")):"");'
     'function setv(id,v){var e=document.getElementById(id);if(e)e.value=v;}'
     'setv(MSGID,LABEL+" result: "+r.t+" (score "+s+"/"+MAX+")");'
     'setv(RESID,r.t);setv(SCOREID,s+"/"+MAX);setv(PLANID,plan);}'
     'document.getElementById("restart").onclick=function(){i=0;ans=Array(Q.length).fill(-1);res.style.display="none";asmt.style.display="block";render();};'
     'render();})();</script>')
    return write(prop, slug + ".html", title, desc, header_html, hero + app + script, cobrand=cobrand)

# ---- reusable fragment helpers ----
def cta_red(heading, sub, label, href, on_red=True):
    cls = "btn btn-on-red btn-lg" if on_red else "btn btn-primary btn-lg"
    return (f'<section class="cta-red"><div class="wrap">'
     f'<div class="cta-red__logo">CINTA &amp; Co.</div>'
     f'<div class="cta-red__tag">Facilitating Success</div>'
     f'<h2 data-r>{heading}</h2>'
     f'<p class="cta-red__sub" data-r data-rd="1">{sub}</p>'
     f'<a href="{href}" class="{cls}" data-r data-rd="2">{label} {icon("arrow")}</a>'
     f'</div></section>\n')
