#!/usr/bin/env bash
set -euo pipefail

if [[ "$PWD" == "/" ]]; then
  SESSION="dev"
else
  SESSION="$(basename "$PWD")"
fi
SESSION="${SESSION//[^A-Za-z0-9._-]/_}"
SESSION="${SESSION:-dev}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ln -sf "$DIR/tmux.conf" "$HOME/.tmux.conf"
ln -sf "$DIR/status.sh" "$HOME/.tmux-status.sh"
ln -sf "$DIR/find.sh" "$HOME/.tmux-find.sh"
chmod +x "$DIR/find.sh" "$DIR/status.sh"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  exec tmux attach -t "$SESSION"
fi

tmux new-session -d -s "$SESSION" 'ranger'
tmux source-file "$HOME/.tmux.conf"
tmux split-window -h -p 50
tmux split-window -v -p 50
tmux select-pane -t "$SESSION:.-"
tmux send-keys -t "$SESSION:." 'opencode' Enter
tmux select-pane -t "$SESSION:.-"

exec tmux attach -t "$SESSION"
