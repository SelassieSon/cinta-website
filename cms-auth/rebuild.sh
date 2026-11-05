#!/usr/bin/env bash
# Rebuild the Insights blog from content/blog/*.md and sync to the web root.
# Shared by autodeploy.sh (CMS commits) and publish.py (CINTA AI posts).
set -euo pipefail
REPO=/opt/cinta-website
cd "$REPO/_build" && python3 build_blog.py
cp "$REPO"/_shared/*.css "$REPO"/insights/
rsync -a --delete \
  --exclude '*.md' --exclude '_build' --exclude '_shared' --exclude 'apps-script' \
  --exclude 'deploy*.sh' --exclude 'Caddyfile' --exclude '.git*' \
  "$REPO"/insights/ /var/www/insights/
