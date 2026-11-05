#!/usr/bin/env bash
# Auto-rebuild + redeploy the Insights blog when the CMS commits a new/edited
# post to GitHub. Installed as a cron job by `deploy-on-server.sh cms`.
# Only rebuilds insights/ (the CMS only touches content/blog + insights/uploads).
set -euo pipefail
REPO=/opt/cinta-website
cd "$REPO"
git fetch origin main -q
if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]; then
  exit 0
fi
git reset --hard origin/main -q
cd "$REPO/_build" && python3 build_blog.py
cp "$REPO"/_shared/*.css "$REPO"/insights/
rsync -a --delete \
  --exclude '*.md' --exclude '_build' --exclude '_shared' --exclude 'apps-script' \
  --exclude 'deploy*.sh' --exclude 'Caddyfile' --exclude '.git*' \
  "$REPO"/insights/ /var/www/insights/
echo "$(date -u +%FT%TZ) redeployed insights @ $(git rev-parse --short HEAD)"
