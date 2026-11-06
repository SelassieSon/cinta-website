# -*- coding: utf-8 -*-
"""Static blog generator for insights.cintaconsulting.com.
Reads content/blog/*.md (YAML-ish front matter + Markdown body) and writes a
brand-consistent listing page, one page per post, and an RSS feed into insights/."""
import os, re, json, glob, html as _html, datetime
from email.utils import formatdate
import yaml as _yaml
import markdown as _md
import common as c
from common import WWW, INS, AIURL, RAI, icon

A = icon("arrow")
SRC = os.path.join(c.ROOT, "content", "blog")
PROP = "insights"

def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if m:
        try:
            meta = _yaml.safe_load(m.group(1)) or {}
        except Exception:
            meta = {}
        return (meta if isinstance(meta, dict) else {}), m.group(2)
    return {}, raw

def fmt_date(v):
    d = None
    if isinstance(v, datetime.datetime):
        d = v
    elif isinstance(v, datetime.date):
        d = datetime.datetime(v.year, v.month, v.day)
    else:
        try:
            d = datetime.datetime.strptime(str(v or "")[:19], "%Y-%m-%dT%H:%M:%S")
        except Exception:
            d = None
    return (d.strftime("%B %-d, %Y") if d else ""), d

def derive_excerpt(body):
    for para in (body or "").split("\n\n"):
        s = para.strip()
        if not s or s.startswith(("!", "#", ">", "-", "|", "```")):
            continue
        s = re.sub(r"\*\*|__|\*|_|`", "", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        return (s[:197] + "...") if len(s) > 200 else s
    return ""

def render_md(body):
    return _md.markdown(body, extensions=["extra", "sane_lists", "smarty"])

ARTICLE_CSS = """<style>
.post-head,.post-body,.post-tags,.post-wrap,.post-cover{box-sizing:border-box}
.post-hero{background:var(--ink,#1a1a1a);color:#fff;padding:0}
.post-wrap{max-width:760px;margin:0 auto;padding:0 24px}
.post-head{padding:56px 24px 32px;max-width:768px;margin:0 auto}
.post-cat{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--red)}
.post-title{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:12px 0 16px;font-weight:700}
.post-meta{font-size:14px;color:var(--muted)}
.post-cover{width:100%;max-width:980px;margin:0 auto 8px;padding:0 24px;display:block}
.post-cover img{width:100%;height:auto;border-radius:6px;display:block}
.post-body{font-size:18px;line-height:1.75;color:var(--text-body);max-width:768px;margin:0 auto;padding:16px 24px 8px}
.post-body p{margin:0 0 22px}
.post-body h1,.post-body h2,.post-body h3,.post-body h4{line-height:1.25;margin:40px 0 14px;color:var(--text)}
.post-body h1{font-size:30px}.post-body h2{font-size:26px}.post-body h3{font-size:21px}.post-body h4{font-size:18px}
.post-body img{max-width:100%;height:auto;border-radius:6px;margin:10px 0}
.post-body a{color:var(--red);text-decoration:underline;text-underline-offset:2px}
.post-body ul,.post-body ol{margin:0 0 22px;padding-left:24px}
.post-body li{margin:8px 0}
.post-body blockquote{margin:24px 0;padding:6px 20px;border-left:4px solid var(--red);color:var(--text);font-style:italic}
.post-body hr{border:0;border-top:1px solid var(--gray);margin:32px 0}
.post-body code{background:var(--gray);padding:2px 6px;border-radius:4px;font-size:.9em}
.post-tags{max-width:768px;margin:28px auto 0;padding:0 24px;display:flex;flex-wrap:wrap;gap:8px}
.post-tags span{font-size:12px;color:var(--muted);border:1px solid var(--gray);border-radius:999px;padding:5px 12px}
.post-byline{display:flex;align-items:center;gap:10px;margin-top:10px}
</style>"""

INDEX_CSS = """<style>
.blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:28px}
.pcard{display:flex;flex-direction:column;background:#fff;border:1px solid var(--gray);border-radius:8px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}
.pcard:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(0,0,0,.08)}
.pcard__img{aspect-ratio:16/9;background-size:cover;background-position:center;background-color:var(--red)}
.pcard__img--ph{background:linear-gradient(135deg,var(--red),var(--brown))}
.pcard__body{padding:20px 22px 24px;display:flex;flex-direction:column;flex:1}
.pcard__cat{font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--red);margin-bottom:8px}
.pcard h3{font-size:19px;line-height:1.3;margin:0 0 10px}
.pcard__ex{font-size:14px;color:var(--muted);line-height:1.6;flex:1}
.pcard__meta{font-size:12.5px;color:var(--muted);margin-top:16px}
.cat-filter{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 36px}
.cat-chip{font-size:13px;font-weight:600;border:1.5px solid var(--gray);background:#fff;color:var(--text);border-radius:999px;padding:8px 16px;cursor:pointer;font-family:var(--ff);transition:all .15s}
.cat-chip.active,.cat-chip:hover{border-color:var(--red);background:var(--red-tint);color:var(--red)}
</style>"""

def post_page(meta, body_html, prev_next=None):
    date_s, _ = fmt_date(meta.get("date"))
    cats = meta.get("categories") or []
    tags = meta.get("tags") or []
    minutes = meta.get("minutes") or 0
    cover = meta.get("cover") or ""
    cat = cats[0] if cats else "Insights"
    cover_html = (f'<div class="post-cover"><img src="{cover}" alt="{_html.escape(meta.get("title",""))}"></div>'
                  if cover else "")
    tag_html = ""
    if tags:
        tag_html = '<div class="post-tags">' + "".join(f"<span>{_html.escape(t)}</span>" for t in tags[:12]) + "</div>"
    meta_line = " · ".join([x for x in [_html.escape(meta.get("author", "CINTA & Co.")), date_s,
                                        (f"{minutes} min read" if minutes else "")] if x])
    body = (f'<section class="section" style="padding-top:40px">'
            f'<div class="post-head"><p class="post-cat">{_html.escape(cat)}</p>'
            f'<h1 class="post-title">{_html.escape(meta.get("title",""))}</h1>'
            f'<p class="post-meta">{meta_line}</p></div>'
            f'{cover_html}'
            f'<article class="post-body">{body_html}</article>'
            f'{tag_html}'
            f'<div class="post-wrap" style="margin-top:14px"><a href="{INS}/" class="textlink">{A} Back to Insights</a></div>'
            f'</section>')
    cta = c.cta_red("Facing a decision like the ones we write about?",
                    "Start with a 90-minute Ecosystem Mapping Session. We map your situation and give you a clear read on where to act first.",
                    "Book a session", f"{WWW}/contact.html")
    return ARTICLE_CSS + body + cta

def index_page(posts):
    cats = []
    for p in posts:
        for ct in (p["meta"].get("categories") or []):
            if ct not in cats:
                cats.append(ct)
    cats = sorted(cats)
    chips = '<button class="cat-chip active" data-cat="*">All</button>' + "".join(
        f'<button class="cat-chip" data-cat="{_html.escape(ct)}">{_html.escape(ct)}</button>' for ct in cats)
    cards = ""
    for p in posts:
        m = p["meta"]
        date_s, _ = fmt_date(m.get("date"))
        cover = m.get("cover") or ""
        cat = (m.get("categories") or ["Insights"])[0]
        img = (f'<div class="pcard__img" style="background-image:url(\'{cover}\')"></div>'
               if cover else '<div class="pcard__img pcard__img--ph"></div>')
        meta_line = " · ".join([x for x in [_html.escape(m.get("author", "CINTA & Co.")), date_s,
                                            (f'{m.get("minutes")} min' if m.get("minutes") else "")] if x])
        data_cats = _html.escape("|".join(m.get("categories") or []))
        cards += (f'<a class="pcard" href="{INS}/{p["slug"]}.html" data-cats="{data_cats}">'
                  f'{img}<div class="pcard__body"><div class="pcard__cat">{_html.escape(cat)}</div>'
                  f'<h3>{_html.escape(m.get("title",""))}</h3>'
                  f'<p class="pcard__ex">{_html.escape(m.get("excerpt",""))}</p>'
                  f'<div class="pcard__meta">{meta_line}</div></div></a>')
    hero = (f'<section class="pagehero"><div class="pagehero__accent"></div>'
            f'<div class="wrap pagehero__in">'
            f'<div class="kicker" data-r><span class="kicker__bar"></span><span class="kicker__txt">Insights</span></div>'
            f'<h1 data-r data-rd="1">Ideas for leaders navigating <span class="accent">change</span></h1>'
            f'<p class="pagehero__sub" data-r data-rd="2">Strategy, transformation, and responsible AI, from the CINTA & Co. team. '
            f'{len(posts)} articles and counting.</p></div></section>')
    brief_band = ('<section class="section" style="padding-bottom:0"><div class="wrap">'
            '<div class="assessband" data-r>'
            '<div class="assessband__txt"><p class="eyebrow section-head">Featured reading</p>'
            '<h2>The Agentic AI Executive Brief</h2>'
            '<p class="section__intro">The MIT CISR framework for the agentic era, with a stage self-check '
            'and what each transition actually requires. Written for leaders deciding where to move next.</p></div>'
            f'<div class="assessband__act"><a href="{AIURL}/brief.html" class="btn btn-primary btn-lg">Read the brief {icon("arrow")}</a></div>'
            '</div></div></section>')
    body = (hero + INDEX_CSS + brief_band + '<section class="section"><div class="wrap">'
            f'<div class="cat-filter">{chips}</div>'
            f'<div class="blog-grid" id="grid">{cards}</div></div></section>'
            '<script>(function(){var chips=document.querySelectorAll(".cat-chip"),'
            'cards=document.querySelectorAll(".pcard");'
            'chips.forEach(function(ch){ch.onclick=function(){'
            'chips.forEach(function(x){x.classList.remove("active")});ch.classList.add("active");'
            'var c=ch.dataset.cat;cards.forEach(function(card){'
            'var cs=(card.dataset.cats||"").split("|");'
            'card.style.display=(c==="*"||cs.indexOf(c)>=0)?"":"none";});};});})();</script>')
    return body

def rss(posts):
    items = ""
    for p in posts[:40]:
        m = p["meta"]
        _, d = fmt_date(m.get("date"))
        pub = formatdate(d.timestamp()) if d else ""
        items += (f"<item><title>{_html.escape(m.get('title',''))}</title>"
                  f"<link>{INS}/{p['slug']}.html</link>"
                  f"<guid>{INS}/{p['slug']}.html</guid>"
                  f"<pubDate>{pub}</pubDate>"
                  f"<description>{_html.escape(m.get('excerpt',''))}</description></item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            '<title>CINTA &amp; Co. Insights</title>'
            f'<link>{INS}/</link>'
            '<description>Strategy, transformation, and responsible AI from CINTA &amp; Co.</description>'
            f'{items}</channel></rss>')

def build():
    files = glob.glob(os.path.join(SRC, "*.md"))
    posts = []
    for f in files:
        meta, body = parse(f)
        if str(meta.get("draft", "")).lower() == "true" or meta.get("draft") is True:
            continue  # unpublished draft: skip from the live site
        slug = meta.get("slug") or os.path.basename(f)[:-3]
        if not meta.get("excerpt"):
            meta["excerpt"] = derive_excerpt(body)
        _, dt = fmt_date(meta.get("date"))
        posts.append({"slug": slug, "meta": meta, "body": body,
                      "sort": dt.isoformat() if dt else ""})
    posts.sort(key=lambda p: p["sort"], reverse=True)
    # per-post pages
    for p in posts:
        html_body = render_md(p["body"])
        c.write(PROP, p["slug"] + ".html",
                _html.escape(p["meta"].get("title", "")) + " | CINTA & Co. Insights",
                p["meta"].get("excerpt", ""),
                c.header_www(active="Insights"), post_page(p["meta"], html_body))
    # index
    c.write(PROP, "index.html", "Insights | CINTA & Co.",
            "Strategy, transformation, and responsible AI insights from CINTA & Co.",
            c.header_www(active="Insights"), index_page(posts))
    # rss
    with open(os.path.join(c.ROOT, PROP, "feed.xml"), "w", encoding="utf-8") as fh:
        fh.write(rss(posts))
    print(f"insights: {len(posts)} posts + index + feed.xml written")

if __name__ == "__main__":
    build()
