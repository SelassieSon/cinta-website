# -*- coding: utf-8 -*-
"""Shared chrome + helpers for the CINTA & Co. static site generator."""
import os

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
             f'<a href="{how}">How it works</a>'
             f'<a href="{cta_href}" class="btn btn-primary">{cta_label} {icon("arrow")}</a>')
    return (f'<header class="hdr hdr--dark"><div class="hdr__in">'
     f'<a href="{RAI}" class="logo cobrand" aria-label="CoCr8 Labs and CINTA & Co.">'
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
             f'<a href="{AIURL}/#demo" class="btn btn-primary">Book a Demo {icon("arrow")}</a>')
    return (f'<header class="hdr"><div class="hdr__in">'
     f'<a href="{AIURL}/" class="logo" aria-label="CINTA & Co. — Facilitating Success">'
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
