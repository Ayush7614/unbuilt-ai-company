#!/usr/bin/env sh
set -eu
URL="${HEALTHCHECK_URL:-http://127.0.0.1:8000/health}"
python - "$URL" <<'PY'
import sys
from urllib.request import urlopen

url = sys.argv[1]
with urlopen(url, timeout=5) as response:
    body = response.read().decode("utf-8")
    if response.status != 200 or '"status":"ok"' not in body.replace(" ", ""):
        raise SystemExit(f"Health check failed: HTTP {response.status}: {body}")
    print(f"Health check passed: {url}")
PY
