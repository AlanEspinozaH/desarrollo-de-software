#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:?define PORT}"
MESSAGE="${MESSAGE:?define MESSAGE}"
RELEASE="${RELEASE:?define RELEASE}"

cleanup(){ echo "[http_echo] cleanup" >&2; }
trap cleanup EXIT INT TERM

while true; do
  BODY="message=${MESSAGE}, release=${RELEASE}, ts=$(date -Iseconds)"
  CLEN=$(printf "%s" "$BODY" | wc -c)
  {
    IFS= read -r _req
    printf "HTTP/1.1 200 OK\r\n"
    printf "Content-Type: text/plain; charset=utf-8\r\n"
    printf "Content-Length: %s\r\n" "$CLEN"
    printf "Connection: close\r\n\r\n"
    printf "%s" "$BODY"
  } | nc -l -p "$PORT" -q 1 127.0.0.1
done
