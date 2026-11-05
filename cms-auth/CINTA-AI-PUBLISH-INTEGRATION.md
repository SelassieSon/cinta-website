# Task: publish CINTA blog posts to the Insights blog

Add a final "publish to Insights" step to CINTA AI's blog-content pipeline. When a
post for **our own brand** (CINTA / CINTA AI / CoCr8) clears Brand-Guard and the
Evaluator, POST it to the Insights blog endpoint. It lands as a **draft** for human
review at `https://insights.cintaconsulting.com/admin`, then a person publishes it.

This is an outbound HTTP call only. Do not add git, GitHub, or file-writing logic to
CINTA AI. The endpoint handles commit, build, and deploy.

## Scope (important)

- Wire this **only** for our own brand tenant. Do not call it for other clients on
  the platform.
- Every request must include `"brand"` set to one of: `cinta`, `cinta-ai`, `cocr8`.
  The server rejects any other brand with HTTP 403, so client content can never reach
  this blog even if the pipeline is misconfigured.

## Endpoint

```
POST https://insights.cintaconsulting.com/publish
Authorization: Bearer <PUBLISH_SECRET>
Content-Type: application/json
```

`PUBLISH_SECRET` is a shared secret. Store it in CINTA AI's existing secrets/env (e.g.
`INSIGHTS_PUBLISH_SECRET`). It must match the value in `/etc/cinta-publish.env` on the
droplet. Never hardcode it.

### Request body

| Field        | Type       | Required | Notes |
|--------------|------------|----------|-------|
| `brand`      | string     | yes      | `cinta`, `cinta-ai`, or `cocr8`. |
| `title`      | string     | yes      | Post title. |
| `body`       | string     | yes      | Full post in GitHub-flavored **Markdown**. |
| `slug`       | string     | no       | URL id. Derived from the title if omitted. |
| `author`     | string     | no       | Defaults to `CINTA & Co.` |
| `categories` | string[]   | no       | e.g. `["Strategy","AI"]` |
| `tags`       | string[]   | no       | |
| `cover`      | string     | no       | Absolute image URL. Shown atop the post and on the grid. |
| `excerpt`    | string     | no       | 1-2 sentences for the listing. Auto-generated if blank. |
| `minutes`    | int        | no       | Estimated read time. |
| `date`       | string     | no       | ISO 8601. Defaults to now (UTC). |
| `draft`      | bool       | no       | Omit to use the server default (currently draft = true, i.e. hold for review). Send `false` only to publish immediately. |

Notes:
- `body` is Markdown. Use `##`/`###` for headings, `![alt](url)` for inline images
  (absolute URLs), `[text](url)` for links. The `cover` is separate; do not repeat it
  as the first body image.
- `slug` is the identity. POSTing the same slug **overwrites** that post (safe for
  re-runs and edits); a new slug creates a new post. Prefer deriving slug from the
  title and keeping it stable.

### Response

```json
{ "ok": true, "slug": "your-post-slug", "draft": true, "url": null }
```

- `url` is `null` while a post is a draft, and the live URL once published.
- Errors return `{ "ok": false, "error": "..." }` with a status code:
  - `401` wrong/missing secret
  - `403` brand not in the allowlist
  - `400` bad JSON or missing `title`
  - `500` server/build error (`detail` has the tail of the failure)

## Drop-in client

```python
# cinta_blog.py
import os
import requests

INSIGHTS_PUBLISH_URL = "https://insights.cintaconsulting.com/publish"
PUBLISH_SECRET = os.environ["INSIGHTS_PUBLISH_SECRET"]

def publish_to_insights(
    *, title: str, body_markdown: str, brand: str = "cinta",
    categories=None, tags=None, cover: str = "", excerpt: str = "",
    minutes: int = 0, slug: str = "", draft: bool | None = None,
    author: str = "CINTA & Co.", timeout: int = 30,
) -> dict:
    """Publish a post to the CINTA Insights blog. Returns the endpoint's JSON.
    Raises requests.HTTPError on a non-2xx response so callers can handle it."""
    payload = {
        "brand": brand,
        "title": title,
        "body": body_markdown,
        "author": author,
        "categories": categories or [],
        "tags": tags or [],
        "cover": cover,
        "excerpt": excerpt,
        "minutes": int(minutes or 0),
    }
    if slug:
        payload["slug"] = slug
    if draft is not None:
        payload["draft"] = draft
    r = requests.post(
        INSIGHTS_PUBLISH_URL,
        headers={"Authorization": f"Bearer {PUBLISH_SECRET}"},
        json=payload,
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()
```

### Where to call it

In the blog/Insights content path, after Brand-Guard and the Evaluator pass, as the
terminal step, and only for the CINTA brand tenant:

```python
result = publish_to_insights(
    title=post.title,
    body_markdown=post.markdown,
    brand="cinta",
    categories=post.categories,
    tags=post.tags,
    cover=post.cover_url,
    excerpt=post.summary,
    minutes=post.read_minutes,
)
# store result["slug"] on the campaign/record for traceability
```

### Error handling

- Treat any non-2xx as a publish failure. Log `error` (and `detail` on 500).
- Do **not** retry 4xx (fix the payload instead). A single retry on 5xx or a timeout
  is reasonable.
- Re-POSTing the same `slug` is idempotent (it updates the post), so a retry won't
  create duplicates.

## Test

```bash
curl -sS -X POST https://insights.cintaconsulting.com/publish \
  -H "Authorization: Bearer $INSIGHTS_PUBLISH_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"brand":"cinta","title":"Pipeline test post",
       "body":"## It works\n\nThis is a test from CINTA AI.",
       "categories":["AI"],"tags":["test"]}'
```

Expect `{"ok":true,"slug":"pipeline-test-post","draft":true,"url":null}`. It then
appears as a draft at `https://insights.cintaconsulting.com/admin`. Delete the test
draft there when done.

## Checklist

- [ ] `INSIGHTS_PUBLISH_SECRET` added to CINTA AI secrets (matches the droplet).
- [ ] `publish_to_insights(...)` added and called as the final step of the CINTA-brand
      blog path only.
- [ ] `brand` set to `cinta` (or `cinta-ai` / `cocr8`); other tenants never call this.
- [ ] Response `slug` stored on the record; failures logged.
- [ ] One test post verified as a draft in `/admin`, then removed.
