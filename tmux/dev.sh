#!/usr/bin/env bash
set -euo pipefail

SESSION="dev"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ln -sf "$DIR/tmux.conf" "$HOME/.tmux.conf"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  exec tmux attach -t "$SESSION"
fi

tmux new-session -d -s "$SESSION" 'ranger'
tmux source-file "$HOME/.tmux.conf"
tmux split-window -h -p 50
tmux select-pane -t "$SESSION:0.1"
tmux split-window -v -p 50
tmux send-keys -t "$SESSION:0.1" 'opencode' Enter
tmux select-pane -t "$SESSION:0.0"

exec tmux attach -t "$SESSION"
