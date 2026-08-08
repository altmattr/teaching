#!/usr/bin/env bash
set -euo pipefail

# Searchable tmux keybinding finder.
# Run inside a tmux display-popup (see the F1 binding in tmux.conf).
# Shows C-b (prefix) shortcuts plus no-prefix (root) keys, skipping the
# copy-mode and mouse noise. Pick a binding with fzf, then hand the chosen
# command to the tmux command prompt (pre-filled) for review before running.

client="$(tmux list-clients -F '#{client_tty}' | head -n1)"
[[ -n "$client" ]] || exit 0

lines="$(
  {
    tmux list-keys -T prefix |
      awk '{
        line=$0
        sub(/^bind-key( +-r)?( +-N[^ ]*)? +-T prefix +/, "", line)
        key=line; sub(/ .*/, "", key)
        cmd=line; sub(/^[^ ]+ +/, "", cmd)
        printf "%-11s %s\t%s\n", "C-b " key, cmd, $0
      }'
    tmux list-keys -T root |
      grep -vE 'Mouse|Wheel|Click|Drag' |
      awk '{
        line=$0
        sub(/^bind-key( +-r)?( +-N[^ ]*)? +-T root +/, "", line)
        key=line; sub(/ .*/, "", key)
        cmd=line; sub(/^[^ ]+ +/, "", cmd)
        printf "%-11s %s\t%s\n", key, cmd, $0
      }'
  }
)"

choice="$(
  printf '%s\n' "$lines" |
    fzf --height 100% --layout reverse --border rounded \
        --prompt 'keys> ' --no-multi --no-hscroll \
        --header 'type to filter: C-b prefix keys + no-prefix keys' \
        --delimiter $'\t' --with-nth 1 \
    || true
)"

[[ -n "$choice" ]] || exit 0

# fzf returns the full tab-separated line; field 2 is the raw bind-key line.
cmd="$(printf '%s\n' "$choice" | cut -f2 | sed -E 's/^bind-key( +-r)?( +-N[^ ]*)? +-T +[^ ]+ +[^ ]+ +//')"
[[ -n "$cmd" ]] || exit 0

# Close the popup first, then open the command prompt on the real client.
# setsid detaches so closing the popup does not kill the handoff.
export TMUX_FZF_CLIENT="$client" TMUX_FZF_CMD="$cmd"
setsid bash -c 'sleep 0.1; exec tmux command-prompt -t "$TMUX_FZF_CLIENT" -I "$TMUX_FZF_CMD" -T command -p "tmux:"' >/dev/null 2>&1 &
