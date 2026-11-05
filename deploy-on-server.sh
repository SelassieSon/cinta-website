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
    sync cintaai       /var/www/cintaai
    sync insights      /var/www/insights ;;
  insights)
    sync insights /var/www/insights ;;
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
  insights-caddy)
    mkdir -p /etc/caddy/sites /var/www/insights
    if ! grep -q 'import /etc/caddy/sites' /etc/caddy/Caddyfile; then
      cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.bak.$(date +%s)"
      sed -i '1i import /etc/caddy/sites/*.caddy\n' /etc/caddy/Caddyfile
    fi
    cat > /etc/caddy/sites/insights.caddy <<'CADDY'
insights.cintaconsulting.com {
    encode zstd gzip
    # Preserve SEO: old Wix blog URLs /post/<slug> -> new /<slug>.html
    @oldpost path_regexp op ^/post/(.+?)/?$
    redir @oldpost /{re.op.1}.html 301
    root * /var/www/insights
    try_files {path} {path}.html {path}/
    file_server
}
CADDY
    caddy validate --config /etc/caddy/Caddyfile
    systemctl reload caddy
    echo "  insights vhost ready (TLS issues once DNS points insights -> this server)" ;;
  cms)
    # Browser CMS: GitHub OAuth relay + auto-rebuild cron + OAuth-enabled vhost.
    command -v python3 >/dev/null 2>&1 || { apt-get update -qq; apt-get install -y -qq python3; }
    python3 -m pip install --break-system-packages -q markdown pyyaml 2>/dev/null || \
      apt-get install -y -qq python3-markdown python3-yaml || true

    # 1) OAuth relay service
    mkdir -p /opt/cinta-oauth
    cp "$REPO_DIR/cms-auth/oauth.py" /opt/cinta-oauth/oauth.py
    if [ ! -f /etc/cinta-oauth.env ]; then
      cat > /etc/cinta-oauth.env <<'ENV'
# Fill these from your GitHub OAuth App, then: systemctl restart cinta-oauth
CINTA_OAUTH_CLIENT_ID=
CINTA_OAUTH_CLIENT_SECRET=
CINTA_OAUTH_PORT=8787
ENV
      chmod 600 /etc/cinta-oauth.env
      echo "  >> created /etc/cinta-oauth.env — add your GitHub client id/secret, then: systemctl restart cinta-oauth"
    fi
    cat > /etc/systemd/system/cinta-oauth.service <<'UNIT'
[Unit]
Description=CINTA CMS GitHub OAuth relay
After=network-online.target
Wants=network-online.target
[Service]
EnvironmentFile=/etc/cinta-oauth.env
ExecStart=/usr/bin/python3 /opt/cinta-oauth/oauth.py
Restart=always
User=root
[Install]
WantedBy=multi-user.target
UNIT
    systemctl daemon-reload
    systemctl enable --now cinta-oauth
    systemctl restart cinta-oauth

    # 1b) Publish endpoint for the CINTA AI marketing system
    cp "$REPO_DIR/cms-auth/publish.py" /opt/cinta-oauth/publish.py
    if [ ! -f /etc/cinta-publish.env ]; then
      cat > /etc/cinta-publish.env <<'ENV'
# Shared secret CINTA AI sends as "Authorization: Bearer <PUBLISH_SECRET>"
PUBLISH_SECRET=
# GitHub token with contents:write on SelassieSon/cinta-website (for push)
PUBLISH_GH_TOKEN=
PUBLISH_REPO=SelassieSon/cinta-website
# true = AI posts wait for review in /admin; false = AI posts go live
PUBLISH_DEFAULT_DRAFT=true
PUBLISH_PORT=8788
ENV
      chmod 600 /etc/cinta-publish.env
      echo "  >> created /etc/cinta-publish.env — add PUBLISH_SECRET + PUBLISH_GH_TOKEN, then: systemctl restart cinta-publish"
    fi
    cat > /etc/systemd/system/cinta-publish.service <<'UNIT'
[Unit]
Description=CINTA AI blog publish endpoint
After=network-online.target
Wants=network-online.target
[Service]
EnvironmentFile=/etc/cinta-publish.env
ExecStart=/usr/bin/python3 /opt/cinta-oauth/publish.py
Restart=always
User=root
[Install]
WantedBy=multi-user.target
UNIT
    systemctl daemon-reload
    systemctl enable --now cinta-publish
    systemctl restart cinta-publish

    # 2) Auto-rebuild cron (every 5 min, only redeploys insights when main changes)
    chmod +x "$REPO_DIR/cms-auth/autodeploy.sh" "$REPO_DIR/cms-auth/rebuild.sh"
    cat > /etc/cron.d/cinta-cms <<'CRON'
*/5 * * * * root /opt/cinta-website/cms-auth/autodeploy.sh >> /var/log/cinta-cms.log 2>&1
CRON

    # 3) OAuth-enabled Insights vhost (supersedes the basic insights vhost)
    mkdir -p /etc/caddy/sites
    if ! grep -q 'import /etc/caddy/sites' /etc/caddy/Caddyfile; then
      cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.bak.$(date +%s)"
      sed -i '1i import /etc/caddy/sites/*.caddy\n' /etc/caddy/Caddyfile
    fi
    cat > /etc/caddy/sites/insights.caddy <<'CADDY'
insights.cintaconsulting.com {
    encode zstd gzip
    @oldpost path_regexp op ^/post/(.+?)/?$
    redir @oldpost /{re.op.1}.html 301
    handle /oauth/* {
        reverse_proxy 127.0.0.1:8787
    }
    handle /publish* {
        reverse_proxy 127.0.0.1:8788
    }
    handle {
        root * /var/www/insights
        try_files {path} {path}.html {path}/
        file_server
    }
}
CADDY
    caddy validate --config /etc/caddy/Caddyfile
    systemctl reload caddy
    echo "  CMS ready: /admin served, /oauth proxied, auto-rebuild cron installed."
    echo "  If you just created /etc/cinta-oauth.env, fill it and run: systemctl restart cinta-oauth" ;;
  *) echo "unknown mode: $MODE"; exit 1 ;;
esac
echo "done ($MODE)."
