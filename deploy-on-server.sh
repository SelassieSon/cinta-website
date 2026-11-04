#!/usr/bin/env bash
# CINTA & Co. — server-side deploy. Run on the droplet (as root).
#   bash deploy-on-server.sh www            # sync the main site only (staging/first run)
#   bash deploy-on-server.sh all            # sync www + every subdomain (live refresh)
#   bash deploy-on-server.sh staging-caddy  # add staging.cintaconsulting.com vhost
set -euo pipefail

REPO_URL="https://github.com/SelassieSon/cinta-website"
REPO_DIR="/opt/cinta-website"
MODE="${1:-www}"

command -v rsync >/dev/null 2>&1 || { apt-get update -qq; apt-get install -y -qq rsync; }

# clone or fast-forward
if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" fetch --depth 1 origin main -q
  git -C "$REPO_DIR" reset --hard origin/main -q
else
  git clone --depth 1 "$REPO_URL" "$REPO_DIR" -q
fi

sync() { mkdir -p "$2"; rsync -a --delete \
  --exclude '*.md' --exclude '_build' --exclude '_shared' --exclude 'apps-script' \
  --exclude 'deploy*.sh' --exclude 'Caddyfile' --exclude '.git*' \
  "$REPO_DIR/$1/" "$2/"; echo "  synced $1 -> $2"; }

case "$MODE" in
  www)
    sync www /var/www/www ;;
  all)
    sync www          /var/www/www
    sync responsibleai /var/www/landing/responsibleai
    sync ecosystem     /var/www/landing/ecosystem
    sync aia           /var/www/landing/aia
    sync workflow      /var/www/landing/workflow
    sync execution     /var/www/landing/execution
    sync cintaai       /var/www/cintaai ;;
  staging-caddy)
    mkdir -p /etc/caddy/sites
    if ! grep -q 'import /etc/caddy/sites' /etc/caddy/Caddyfile; then
      cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.bak.$(date +%s)"
      sed -i '1i import /etc/caddy/sites/*.caddy\n' /etc/caddy/Caddyfile
    fi
    cat > /etc/caddy/sites/staging-www.caddy <<'CADDY'
staging.cintaconsulting.com {
    encode zstd gzip
    root * /var/www/www
    try_files {path} {path}.html {path}/
    file_server
}
CADDY
    caddy validate --config /etc/caddy/Caddyfile
    systemctl reload caddy
    echo "  staging vhost ready (TLS issues once DNS points staging -> this server)" ;;
  go-live-caddy)
    mkdir -p /etc/caddy/sites
    if ! grep -q 'import /etc/caddy/sites' /etc/caddy/Caddyfile; then
      cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.bak.$(date +%s)"
      sed -i '1i import /etc/caddy/sites/*.caddy\n' /etc/caddy/Caddyfile
    fi
    cat > /etc/caddy/sites/www.caddy <<'CADDY'
cintaconsulting.com {
    redir https://www.cintaconsulting.com{uri} permanent
}
www.cintaconsulting.com {
    encode zstd gzip
    root * /var/www/www
    try_files {path} {path}.html {path}/
    file_server
}
CADDY
    caddy validate --config /etc/caddy/Caddyfile
    systemctl reload caddy
    echo "  www + apex vhost ready (TLS issues once DNS points them here)" ;;
  *) echo "unknown mode: $MODE"; exit 1 ;;
esac
echo "done ($MODE)."
