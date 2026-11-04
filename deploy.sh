#!/usr/bin/env bash
# Deploy one CINTA property to the droplet.  Usage: ./deploy.sh www
# Requires SSH access to the droplet.  Set DROPLET below.
set -euo pipefail
DROPLET="${DROPLET:-user@YOUR_DROPLET_IP}"
PROP="${1:?usage: ./deploy.sh <www|responsibleai|ecosystem|aia|workflow|execution|cintaai|all>}"
props=( "$PROP" )
[ "$PROP" = "all" ] && props=( www responsibleai ecosystem aia workflow execution cintaai )
for p in "${props[@]}"; do
  echo "→ deploying $p"
  rsync -avz --delete --exclude '*.md' "./$p/" "$DROPLET:/var/www/$p/"
done
echo "done. Caddy serves immediately; HTTPS is automatic."
