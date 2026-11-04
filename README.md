# CINTA & Co. — Website

Static, brand-locked, multi-property site for `cintaconsulting.com`, built to
the CINTA & Co. Brand Guidelines and Writing Style Guide (Feb 2026). Self-hosted
on DigitalOcean behind Caddy. The blog stays on Wix at `insights.cintaconsulting.com`.

## Properties (18 pages)

| Folder | Subdomain | Pages |
|---|---|---|
| `www/` | www.cintaconsulting.com | index, about, sectors, services, contact, privacy, terms |
| `responsibleai/` | responsibleai.cintaconsulting.com | hub (#services) |
| `ecosystem/` | ecosystem.cintaconsulting.com | Ecosystem Mapping Session |
| `aia/` | aia.cintaconsulting.com | Responsible AI Prototyping + AIA |
| `workflow/` | workflow.cintaconsulting.com | Copilot Workflow Redesign |
| `execution/` | execution.cintaconsulting.com | Responsible AI Execution System |
| `cintaai/` | cintaai.cintaconsulting.com | platform, saas, agencies, founders, brief, assessment |

Responsible AI properties carry the CoCr8 Labs × CINTA co-branding.

## The brand lives in one place

`_shared/tokens.css` is the single source of truth: red `#D04747`, brown
`#944026`, the Montserrat scale, 60-30-10 colour, radii, shadow, motion. Every
page imports `site.css` → `base.css` → `tokens.css`. Change a brand value once,
in `tokens.css`, and it updates everywhere. This is what stops drift (the wrong
`#c62828` red that was on the old workflow lander cannot happen here).

A copy of the three CSS files is placed in each property folder so each subdomain
root is self-contained. The generator and `deploy.sh` keep them in sync.

## Local preview

```bash
cd www && python3 -m http.server 8080   # then open http://localhost:8080
```

## Regenerating

Pages are generated from `_build/*.py` (shared chrome in `common.py`). To change
copy or structure, edit the builder and re-run:

```bash
cd _build
python3 build_www.py && python3 build_rai.py && python3 build_cintaai.py
cd .. && for p in www responsibleai ecosystem aia workflow execution cintaai; do \
  cp _shared/*.css "$p/"; done
```

## Deploy

1. Set your droplet in `deploy.sh` (`DROPLET=user@IP`), or export `DROPLET`.
2. Put `Caddyfile` on the droplet and reload Caddy.
3. Deploy everything: `./deploy.sh all` (or one property: `./deploy.sh www`).

Caddy issues HTTPS automatically for every host.

## Go-live sequence (zero downtime)

1. Deploy to a `staging.cintaconsulting.com` root first and verify.
2. In Wix, connect the blog to `insights.cintaconsulting.com` (add the CNAME Wix gives you).
3. Point `@` and `www` A records at the droplet. `www` now serves this site.
4. Remove the root domain from Wix, add 301s for any changed blog URLs, submit the sitemap.

## Wiring (search the code)

- **Booking** on `www/contact.html` posts the Ecosystem Mapping intake to a Google
  Apps Script web app (`apps-script/Code.gs`) that books the Calendar event,
  provisions Drive, logs to Sheets, and emails confirmation. Set `BOOKING_WEBHOOK`
  in `_build/common.py` to your deployed `/exec` URL. Full steps in BOOKING-SETUP.md.
- **Brief intake** on `cintaai/brief.html` posts to `#`. Point `action=` at an
  Apps Script web app or form handler.

## Decisions baked in

- No pricing or duration on any page (per instruction). CINTA AI plans show
  capability and fit, not dollars. Say the word to add product pricing back.
- `aia` serves "Responsible AI Prototyping + Algorithm Impact Assessment", the
  combined offering from the GTM doc, so the slug matches the content.
- Montserrat throughout (Brandon Grotesque is not a free web font; the brand
  guide names Montserrat as the sanctioned fallback).
