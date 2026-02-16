#!/usr/bin/env sh
set -eu

PORT="${1:-8000}"
echo "Serving on http://localhost:${PORT}"
python3 -m http.server "${PORT}"
