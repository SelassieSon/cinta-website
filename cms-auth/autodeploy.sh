#!/usr/bin/env bash
# Auto-rebuild + redeploy the Insights blog when a post is committed to GitHub
# (via the CMS). Installed as a cron job by `deploy-on-server.sh cms`.
set -euo pipefail
REPO=/opt/cinta-website
cd "$REPO"
git fetch origin main -q
if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]; then
  exit 0
fi
git reset --hard origin/main -q
bash "$REPO/cms-auth/rebuild.sh"
echo "$(date -u +%FT%TZ) redeployed insights @ $(git rev-parse --short HEAD)"
