#!/bin/bash
# present.sh — Terminal slide deck for COMP3000 lecture rundown
# Usage: ./present.sh <week_number>

WEEK_NUM=$1
RUNDOWN="lecture_rundown.md"

if [ -z "$WEEK_NUM" ]; then
    echo "Usage: $0 <week_number>"
    exit 1
fi

if [ ! -f "$RUNDOWN" ]; then
    echo "Error: $RUNDOWN not found"
    exit 1
fi

# Parse the rundown
declare -a slide_title
declare -a slide_notes
declare -a slide_time_str
declare -a slide_seconds
declare -a slide_commands
slide_count=0
week_heading=""

in_target_week=false
while IFS= read -r line; do
    if [[ "$line" =~ ^##\ Week\ ([0-9]+) ]]; then
        week=${BASH_REMATCH[1]}
        if [ "$week" -eq "$WEEK_NUM" ]; then
            in_target_week=true
            week_heading="${line##*## }"
        elif $in_target_week; then
            break
        fi
    elif $in_target_week && [[ "$line" =~ ^-\ \((.+)\)\ (.+)$ ]]; then
        time_str="${BASH_REMATCH[1]}"
        text="${BASH_REMATCH[2]}"

        hours=${time_str%%:*}
        mins=${time_str##*:}
        hours=$((10#$hours))
        mins=$((10#$mins))
        total_seconds=$((hours * 3600 + mins * 60))

        # Split on first colon
        if [[ "$text" =~ ^([^:]+):\ (.+)$ ]]; then
            slide_title[$slide_count]="${BASH_REMATCH[1]}"
            slide_notes[$slide_count]="${BASH_REMATCH[2]}"
        else
            slide_title[$slide_count]="$text"
            slide_notes[$slide_count]=""
        fi

        # Extract backtick commands from notes
        slide_commands[$slide_count]=""
        remainder="${slide_notes[$slide_count]}"
        while [[ "$remainder" =~ \`([^\`]+)\` ]]; do
            cmd="${BASH_REMATCH[1]}"
            remainder="${remainder#*"${BASH_REMATCH[0]}"}"
            if [ -n "${slide_commands[$slide_count]}" ]; then
                slide_commands[$slide_count]+=$'\n'"$cmd"
            else
                slide_commands[$slide_count]="$cmd"
            fi
        done

        slide_time_str[$slide_count]="$time_str"
        slide_seconds[$slide_count]=$total_seconds
        slide_count=$((slide_count + 1))
    fi
done < "$RUNDOWN"

if [ $slide_count -eq 0 ]; then
    echo "No slides found for week $WEEK_NUM"
    exit 1
fi

# Terminal cleanup
cleanup() {
    printf '\e[?25h'  # show cursor
    printf '\e[0m'    # reset attributes
    clear
}
trap cleanup EXIT
trap 'cleanup; exit 0' INT TERM

# Hide cursor
printf '\e[?25l'

current=0

get_size() {
    local size
    size=$(stty size)
    TERM_LINES=${size%% *}
    TERM_COLS=${size##* }
}

draw() {
    get_size
    clear

    # Centered heading
    local pad=$(( (TERM_COLS - ${#week_heading}) / 2 ))
    printf "%${pad}s%s\n\n" "" "$week_heading"

    # List
    local i
    for ((i=0; i<slide_count; i++)); do
        if [ $i -eq $current ]; then
            printf "    > %s\n" "${slide_title[$i]}"
            if [ -n "${slide_notes[$i]}" ]; then
                printf "        %s\n" "${slide_notes[$i]}"
            fi
            if [ -n "${slide_commands[$i]}" ]; then
                local ncmds
                ncmds=$(printf '%s\n' "${slide_commands[$i]}" | grep -c .)
                if [ "$ncmds" -eq 1 ]; then
                    printf "        \033[36m(o) run command\033[0m\n"
                else
                    printf "        \033[36m(o) run command (%d available)\033[0m\n" "$ncmds"
                fi
            fi
        else
            printf "      %s\n" "${slide_title[$i]}"
        fi
        printf "\n\n"
    done

    # Time in bottom left
    printf "\e[%s;1H\e[2m%s\e[0m" "$TERM_LINES" "${slide_time_str[$current]}"

    # Time in bottom right
    if [ $current -lt $((slide_count - 1)) ]; then
        local next_time="${slide_time_str[$((current + 1))]}"
        local col=$(( TERM_COLS - ${#next_time} + 1 ))
        printf "\e[%s;%sH\e[2m%s\e[0m" "$TERM_LINES" "$col" "$next_time"
    fi
}

run_command() {
    local cmds="$1"
    local selected=""
    local ncmds
    ncmds=$(printf '%s\n' "$cmds" | grep -c .)

    if [ "$ncmds" -gt 1 ]; then
        printf '\e[?25h'
        clear
        echo "Commands available:"
        local i=1
        while IFS= read -r line; do
            printf "  %d) %s\n" "$i" "$line"
            i=$((i + 1))
        done <<< "$cmds"
        printf "  0) Cancel\n"
        printf "Choose: "
        read -r choice
        if [[ "$choice" =~ ^[1-9]+$ ]] && [ "$choice" -le "$ncmds" ]; then
            selected=$(printf '%s\n' "$cmds" | sed -n "${choice}p")
        else
            return
        fi
    else
        selected=$(printf '%s\n' "$cmds" | head -1)
    fi

    printf '\e[?25h'
    clear
    printf '$ \033[33m%s\033[0m\n\n' "$selected"
    bash -c "$selected"
    local rc=$?
    echo ""
    if [ $rc -ne 0 ]; then
        printf "\033[31m(exit code: %d)\033[0m\n" "$rc"
    fi
    echo ""
    printf "Press any key to return..."
    read -rsn1
    printf '\e[?25l'
}

# Main loop
while true; do
    draw

    read -rsn1 key

    if [[ "$key" == "q" ]] || [[ "$key" == $'\x03' ]]; then
        exit 0
    elif [[ "$key" == "o" ]] || [[ "$key" == "O" ]]; then
        if [ -n "${slide_commands[$current]}" ]; then
            run_command "${slide_commands[$current]}"
        fi
    elif [[ "$key" == $'\e' ]]; then
        read -rsn2 key2
        case "$key2" in
            '[C'|'OC'|'[B'|'OB')  # Right or Down
                current=$(( (current + 1) % slide_count ))
                ;;
            '[D'|'OD'|'[A'|'OA')  # Left or Up
                current=$(( (current - 1 + slide_count) % slide_count ))
                ;;
        esac
    fi
done
