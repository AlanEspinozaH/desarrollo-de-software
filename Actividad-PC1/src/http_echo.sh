#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:?define PORT}"
MESSAGE="${MESSAGE:?define MESSAGE}"
RELEASE="${RELEASE:?define RELEASE}"

while true; do
  NOW="$(date -Iseconds)"
  BODY="message=${MESSAGE}, release=${RELEASE}, ts=${NOW}"
  CLEN=$(printf "%s" "$BODY" | wc -c)
  {
    printf "HTTP/1.1 200 OK\r\n"
    printf "Content-Type: text/plain; charset=utf-8\r\n"
    printf "Content-Length: %s\r\n" "$CLEN"
    printf "Connection: close\r\n"
    printf "\r\n"
    printf "%s" "$BODY"
  } | nc -l -p "$PORT" -q 1
done

