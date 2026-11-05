#!/usr/bin/env python3
"""Tiny GitHub OAuth relay for Sveltia/Decap CMS (self-hosted).

Implements the Decap "external OAuth provider" protocol so the CMS can log in
with GitHub without exposing the client secret to the browser. Runs on the
droplet, reverse-proxied by Caddy at https://insights.cintaconsulting.com/oauth/*.

Reads from the environment (see /etc/cinta-oauth.env):
  CINTA_OAUTH_CLIENT_ID      GitHub OAuth App client id
  CINTA_OAUTH_CLIENT_SECRET  GitHub OAuth App client secret
  CINTA_OAUTH_PORT           listen port (default 8787, localhost only)

GitHub OAuth App "Authorization callback URL" must be:
  https://insights.cintaconsulting.com/oauth/callback
"""
import os, json, secrets, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CLIENT_ID = os.environ.get("CINTA_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("CINTA_OAUTH_CLIENT_SECRET", "")
PORT = int(os.environ.get("CINTA_OAUTH_PORT", "8787"))
GH_AUTH = "https://github.com/login/oauth/authorize"
GH_TOKEN = "https://github.com/login/oauth/access_token"

PAGE = """<!doctype html><html><body>
<script>
(function(){
  function receive(e){
    if (window.opener) window.opener.postMessage('authorization:github:success:__PAYLOAD__', e.origin);
    window.removeEventListener('message', receive, false);
    window.close();
  }
  window.addEventListener('message', receive, false);
  if (window.opener) window.opener.postMessage('authorizing:github', '*');
})();
</script>
<p>Authorized. You can close this window.</p>
</body></html>"""


def origin(h):
    host = h.headers.get("X-Forwarded-Host") or h.headers.get("Host") or "insights.cintaconsulting.com"
    proto = h.headers.get("X-Forwarded-Proto") or "https"
    return proto + "://" + host


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8", headers=None):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        path = u.path.rstrip("/")

        if path.endswith("/auth"):
            if not CLIENT_ID:
                return self._send(500, "OAuth relay is not configured (missing client id).")
            state = secrets.token_urlsafe(24)
            scope = (q.get("scope") or ["repo"])[0] or "repo"
            redirect_uri = origin(self) + "/oauth/callback"
            params = urllib.parse.urlencode({
                "client_id": CLIENT_ID, "redirect_uri": redirect_uri,
                "scope": scope, "state": state, "allow_signup": "false"})
            return self._send(302, "", headers={
                "Location": GH_AUTH + "?" + params,
                "Set-Cookie": "cinta_oauth_state=" + state +
                              "; Path=/oauth; HttpOnly; SameSite=Lax; Secure; Max-Age=600"})

        if path.endswith("/callback"):
            code = (q.get("code") or [""])[0]
            state = (q.get("state") or [""])[0]
            want = ""
            for part in (self.headers.get("Cookie", "") or "").split(";"):
                part = part.strip()
                if part.startswith("cinta_oauth_state="):
                    want = part.split("=", 1)[1]
            if not code or not state or state != want:
                return self._send(400, "Invalid OAuth state. Close this window and try again.")
            body = urllib.parse.urlencode({
                "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                "code": code, "state": state}).encode()
            req = urllib.request.Request(GH_TOKEN, data=body,
                headers={"Accept": "application/json", "User-Agent": "cinta-oauth"})
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    tok = json.loads(r.read().decode())
            except Exception as e:
                return self._send(502, "Token exchange failed: " + str(e))
            access = tok.get("access_token")
            if not access:
                return self._send(502, "No access token returned: " + json.dumps(tok))
            payload = json.dumps({"token": access, "provider": "github"})
            html = PAGE.replace("__PAYLOAD__", payload)
            return self._send(200, html, headers={
                "Set-Cookie": "cinta_oauth_state=; Path=/oauth; Max-Age=0"})

        return self._send(200, "CINTA OAuth relay is running.")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
