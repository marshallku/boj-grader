#!/bin/bash

options=()
selected=0
cursor_visible=1
select_message='What is your choice?'

function toggle_cursor() {
    if [ "$cursor_visible" -eq 1 ]; then
        # Hide cursor
        echo -ne "\e[?25l"
        cursor_visible=0
    else
        # Show cursor
        echo -ne "\e[?25h"
        cursor_visible=1
    fi
}

function highlight() {
    tput rev
    echo -n "$1"
    tput sgr0
}

function display_options() {
    echo -n "$select_message ... "
    for i in "${!options[@]}"; do
        if [ "$i" -eq $selected ]; then
            highlight "${options[$i]}"
        else
            echo -n "${options[$i]}"
        fi

        if [ "$i" -lt $((${#options[@]} - 1)) ]; then
            echo -n " / "
        fi
    done
    echo
}

function select_options() {
    if [ ${#options[@]} -le 0 ]; then
        echo 'There are nothing in options'
        exit 5
    fi

    toggle_cursor

    while true; do
        display_options

        read -r -sn 3 key

        case $key in
        # Left arrow
        $'\x1b[D')
            selected=$((selected - 1))
            if [ $selected -lt 0 ]; then
                selected=$((${#options[@]} - 1))
            fi
            ;;
        # Right arrow
        $'\x1b[C')
            selected=$((selected + 1))
            if [ $selected -ge ${#options[@]} ]; then
                selected=0
            fi
            ;;
        # Enter
        "")
            break
            ;;
        esac

        tput cuu1
        tput el
    done

    toggle_cursor
}
