#!/usr/bin/env bash
set -u
run_posix() {
  cd /tmp && rm -rf l00_lab && mkdir -p l00_lab && cd l00_lab
  printf 'SAFE_DATA\n' > orig.txt
  ln orig.txt hard.txt && ln -s orig.txt sym.txt
  rm orig.txt
  printf 'hard_content=%s\n' "$(cat hard.txt)"
  printf 'hard_links=%s\n' "$(stat -c %h hard.txt)"
  if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi
  printf 'sym_failed=%s\n' "$sf"
}
if [ "$(uname -s)" = "Linux" ]; then
  run_posix
else
  MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '
    cd /tmp && printf "SAFE_DATA\n" > orig.txt
    ln orig.txt hard.txt && ln -s orig.txt sym.txt && rm orig.txt
    printf "hard_content=%s\n" "$(cat hard.txt)"
    printf "hard_links=%s\n" "$(stat -c %h hard.txt)"
    if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi
    printf "sym_failed=%s\n" "$sf"
  '
fi
