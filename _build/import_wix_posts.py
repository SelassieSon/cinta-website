# -*- coding: utf-8 -*-
"""Parse saved (possibly truncated) ExecuteWixAPI result files and write each
complete blog post to content/blog/<slug>.md with YAML front matter.

Usage: python3 import_wix_posts.py <result_file> [<result_file> ...]
Robust to truncation: extracts as many COMPLETE post objects as parse, ignores
the trailing partial object and any tool header/footer text."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "content", "blog")
os.makedirs(OUT, exist_ok=True)

def extract_posts(raw):
    pi = raw.find('"posts"')
    if pi < 0:
        return []
    start = raw.find('[', pi)
    if start < 0:
        return []
    dec = json.JSONDecoder()
    idx = start + 1
    posts = []
    while idx < len(raw):
        while idx < len(raw) and raw[idx] in ' \n\r\t,':
            idx += 1
        if idx >= len(raw) or raw[idx] != '{':
            break
        try:
            obj, end = dec.raw_decode(raw, idx)
        except Exception:
            break
        posts.append(obj)
        idx = end
    return posts

def excerpt_from(md):
    for line in md.split("\n\n"):
        s = line.strip()
        if not s or s.startswith("!") or s.startswith("#") or s.startswith(">"):
            continue
        s = re.sub(r"\*\*|__|\*|_|`", "", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        return (s[:197] + "...") if len(s) > 200 else s
    return ""

def yaml_scalar(v):
    return json.dumps(v if v is not None else "", ensure_ascii=False)

def write_post(p):
    slug = p.get("slug")
    if not slug:
        return None
    md = p.get("markdown", "") or ""
    fm = []
    fm.append("---")
    fm.append("title: " + yaml_scalar(p.get("title", "")))
    fm.append("slug: " + yaml_scalar(slug))
    fm.append("date: " + yaml_scalar(p.get("date", "")))
    fm.append("author: " + yaml_scalar(p.get("author", "CINTA & Co.")))
    fm.append("tags: " + json.dumps(p.get("tags", []) or [], ensure_ascii=False))
    fm.append("categories: " + json.dumps(p.get("categories", []) or [], ensure_ascii=False))
    fm.append("minutes: " + str(p.get("minutes") or 0))
    fm.append("cover: " + yaml_scalar(p.get("cover", "")))
    fm.append("wix_path: " + yaml_scalar(p.get("wixPath", "")))
    fm.append("excerpt: " + yaml_scalar(excerpt_from(md)))
    fm.append("---")
    with open(os.path.join(OUT, slug + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(fm) + "\n\n" + md.strip() + "\n")
    return slug

def main(files):
    seen = set()
    for existing in os.listdir(OUT):
        if existing.endswith(".md"):
            seen.add(existing[:-3])
    new = []
    for path in files:
        raw = open(path, encoding="utf-8", errors="replace").read()
        for p in extract_posts(raw):
            slug = p.get("slug")
            if slug and slug not in seen:
                if write_post(p):
                    seen.add(slug); new.append(slug)
    print("newly written:", len(new))
    for s in new:
        print("  +", s)
    print("total on disk:", len([x for x in os.listdir(OUT) if x.endswith('.md')]))

if __name__ == "__main__":
    main(sys.argv[1:])
