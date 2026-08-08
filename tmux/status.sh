#!/usr/bin/env bash
prev=/tmp/tmux-status-cpu.prev

read -r total idle <<< "$(awk 'NR==1{print $2+$3+$4+$5+$6+$7+$8+$9, $5+$6}' /proc/stat)"
if [[ -f "$prev" ]]; then
  read -r ptotal pidle < "$prev"
  dt=$((total-ptotal)); di=$((idle-pidle))
  (( dt > 0 )) && cpu=$((100*(dt-di)/dt)) || cpu=0
else
  cpu=0
fi
echo "$total $idle" > "$prev"

temp=$(awk '{printf "%.1f", $1/1000}' /sys/class/thermal/thermal_zone0/temp 2>/dev/null || printf '?')
printf 'CPU %s%% %s°C\n' "$cpu" "$temp"
