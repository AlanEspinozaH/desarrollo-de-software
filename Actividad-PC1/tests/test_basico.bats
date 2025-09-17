#!/usr/bin/env bats

setup() {
  export PORT=8080
  export MESSAGE="Hola PC1"
  export RELEASE="v0.1"
  mkdir -p out
}

teardown() {
  [[ -f out/http.pid ]] && kill "$(cat out/http.pid)" 2>/dev/null || true
  rm -rf out dist
}

@test "build genera config.env" {
  run make build
  [ "$status" -eq 0 ]
  [ -f "out/config.env" ]
}

@test "run levanta servidor y responde MESSAGE/RELEASE" {
  run make run
  [ "$status" -eq 0 ]
  run bash -lc 'curl -s http://127.0.0.1:8080'
  [ "$status" -eq 0 ]
  [[ "$output" == *"Hola PC1"* ]]
  [[ "$output" == *"v0.1"* ]]
}
