#!/usr/bin/env bash
set -u
exec < <(tr -d '\r')
read -r DATA DEL_ORIG
run_posix() {
  local d="$1" del="$2"
  cd /tmp && rm -rf l00_lab && mkdir -p l00_lab && cd l00_lab
  printf '%s\n' "$d" > orig.txt
  ln orig.txt hard.txt && ln -s orig.txt sym.txt
  [ "$del" = "1" ] && rm orig.txt
  printf 'hard_content=%s\n' "$(cat hard.txt)"
  printf 'hard_links=%s\n' "$(stat -c %h hard.txt)"
  if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi
  printf 'sym_failed=%s\n' "$sf"
}
if [ "$(uname -s)" = "Linux" ]; then
  run_posix "$DATA" "$DEL_ORIG"
else
  MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '
    d="$1"; del="$2"
    cd /tmp && printf "%s\n" "$d" > orig.txt
    ln orig.txt hard.txt && ln -s orig.txt sym.txt
    [ "$del" = "1" ] && rm orig.txt
    printf "hard_content=%s\n" "$(cat hard.txt)"
    printf "hard_links=%s\n" "$(stat -c %h hard.txt)"
    if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi
    printf "sym_failed=%s\n" "$sf"
  ' -- "$DATA" "$DEL_ORIG"
fi
