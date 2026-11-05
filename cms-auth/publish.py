#!/usr/bin/env python3
"""Blog publish endpoint for the CINTA AI marketing system.

CINTA AI's final step POSTs a finished post here; this writes a Markdown file
to content/blog/, commits + pushes it to GitHub (the blog's source of truth),
and rebuilds the live site. Posts can be published live or held as drafts for
review in the CMS.

Runs on the droplet, reverse-proxied by Caddy at
  https://insights.cintaconsulting.com/publish

Reads from the environment (see /etc/cinta-publish.env):
  PUBLISH_SECRET          shared bearer token CINTA AI must send
  PUBLISH_GH_TOKEN        GitHub token with contents:write on the repo (push)
  PUBLISH_REPO            owner/repo (default SelassieSon/cinta-website)
  PUBLISH_DEFAULT_DRAFT   "true" (hold for review) or "false" (go live)
  PUBLISH_PORT            listen port (default 8788, localhost only)

Request:  POST /publish
  Headers: Authorization: Bearer <PUBLISH_SECRET>, Content-Type: application/json
  Body:    {"title","body"(markdown),"slug"?,"author"?,"categories"?[],
            "tags"?[],"cover"?,"excerpt"?,"minutes"?,"date"?(ISO),"draft"?(bool)}
Response: {"ok":true,"slug":...,"draft":bool,"url":... | null}
"""
import os, re, json, hmac, subprocess, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO = "/opt/cinta-website"
SECRET = os.environ.get("PUBLISH_SECRET", "")
TOKEN = os.environ.get("PUBLISH_GH_TOKEN", "")
REPO_SLUG = os.environ.get("PUBLISH_REPO", "SelassieSon/cinta-website")
PORT = int(os.environ.get("PUBLISH_PORT", "8788"))
DEFAULT_DRAFT = os.environ.get("PUBLISH_DEFAULT_DRAFT", "true").lower() == "true"
SITE = "https://insights.cintaconsulting.com"


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", (s or "").lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:80].strip("-") or "post"


def run(args):
    return subprocess.run(args, cwd=REPO, check=True, capture_output=True, text=True)


def fm_line(k, v):
    if isinstance(v, bool):
        return f"{k}: {'true' if v else 'false'}"
    if isinstance(v, int):
        return f"{k}: {v}"
    if isinstance(v, list):
        return f"{k}: " + json.dumps(v, ensure_ascii=False)
    return f"{k}: " + json.dumps(v if v is not None else "", ensure_ascii=False)


def publish(d):
    title = (d.get("title") or "").strip()
    if not title:
        raise ValueError("title is required")
    body = d.get("body") or d.get("markdown") or ""
    slug = slugify(d.get("slug") or title)
    draft = bool(d.get("draft", DEFAULT_DRAFT))
    date = d.get("date") or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    fm = [
        fm_line("title", title),
        fm_line("slug", slug),
        fm_line("date", date),
        fm_line("author", d.get("author") or "CINTA & Co."),
        fm_line("categories", d.get("categories") or []),
        fm_line("tags", d.get("tags") or []),
        fm_line("minutes", int(d.get("minutes") or 0)),
        fm_line("cover", d.get("cover") or ""),
        fm_line("excerpt", d.get("excerpt") or ""),
        fm_line("draft", draft),
    ]
    content = "---\n" + "\n".join(fm) + "\n---\n\n" + body.strip() + "\n"
    # Sync to latest, write, commit, push.
    run(["git", "fetch", "origin", "main"])
    run(["git", "reset", "--hard", "origin/main"])
    rel = f"content/blog/{slug}.md"
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as f:
        f.write(content)
    run(["git", "add", rel])
    run(["git", "-c", "user.email=bot@cintaconsulting.com", "-c", "user.name=CINTA AI",
         "commit", "-m", f"{'Draft' if draft else 'Publish'}: {title}"])
    push_url = f"https://x-access-token:{TOKEN}@github.com/{REPO_SLUG}"
    run(["git", "push", push_url, "HEAD:main"])
    subprocess.run(["bash", os.path.join(REPO, "cms-auth", "rebuild.sh")], check=True)
    return {"ok": True, "slug": slug, "draft": draft,
            "url": (None if draft else f"{SITE}/{slug}.html")}


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if not self.path.rstrip("/").endswith("/publish"):
            return self._json(404, {"ok": False, "error": "not found"})
        auth = self.headers.get("Authorization", "")
        token = auth[7:] if auth.startswith("Bearer ") else ""
        if not SECRET or not hmac.compare_digest(token, SECRET):
            return self._json(401, {"ok": False, "error": "unauthorized"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            d = json.loads(self.rfile.read(n).decode() or "{}")
        except Exception as e:
            return self._json(400, {"ok": False, "error": "bad json: " + str(e)})
        try:
            return self._json(200, publish(d))
        except ValueError as e:
            return self._json(400, {"ok": False, "error": str(e)})
        except subprocess.CalledProcessError as e:
            return self._json(500, {"ok": False, "error": "git/build failed",
                                    "detail": (e.stderr or "")[-400:]})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
