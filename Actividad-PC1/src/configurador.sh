#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:?}"; MESSAGE="${MESSAGE:?}"; RELEASE="${RELEASE:?}"
DNS_SERVER="${DNS_SERVER:-}"; TARGETS="${TARGETS:-}"
OUT="out"; LOG="$OUT/logs"; CACHE="$OUT/cache"
mkdir -p "$OUT" "$LOG" "$CACHE"
trap 'echo "[configurador] cleanup" >>"$LOG/configurador.log"' EXIT INT TERM
printf "PORT=%s\nMESSAGE=%s\nRELEASE=%s\n" "$PORT" "$MESSAGE" "$RELEASE" > "$OUT/config.env"
if [[ -n "$DNS_SERVER" && -n "$TARGETS" ]]; then
  IFS=',' read -ra H <<< "$TARGETS"
  for h in "${H[@]}"; do
    dig "@$DNS_SERVER" "$h" +short | head -1 > "$OUT/dns_${h}.txt" || true
    echo "[dns] $h -> $(cat "$OUT/dns_${h}.txt")" | tee -a "$LOG/configurador.log"
  done
fi
echo "[configurador] done" | tee -a "$LOG/configurador.log"
