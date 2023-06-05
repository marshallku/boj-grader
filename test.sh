#!/bin/bash

lang='cpp'
file=''

while [[ $# -gt 0 ]]; do
    case "$1" in
    -l | --lang)
        lang="$2"
        shift 2
        ;;
    -f | --file)
        file="$2"
        shift 2
        ;;
    *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done

if [[ -n "$file" ]]; then
    extension="${file##*.}"

    case $extension in
    cpp)
        lang='cpp'
        ;;
    py)
        lang='python'
        ;;
    *)
        echo "Unsupported extension: $extension"
        echo 'Allowed extensions: cpp, py'
        exit 5
        ;;
    esac
fi

case $lang in
cpp | c\+\+)
    lang='cpp'
    ;;
py | python)
    lang='python'
    ;;
*)
    echo "Unsupported language: $lang"
    echo 'C++   : cpp, c++'
    echo 'Python: py, python'
    exit 5
    ;;
esac

if [[ -n "$file" ]]; then
    directory="${file%/*}"
    id_pattern='/([0-9]+)'

    if [[ "$file" =~ $id_pattern ]]; then
        problem_id=${BASH_REMATCH[1]}
        input_file="$directory/input/1.txt"
        output_file="$directory/output/1.txt"

        if [[ -n "$problem_id" ]] && [ ! -e "$input_file" ] || [ ! -e "$output_file" ]; then
            echo "Fetching test cases for $problem_id..."
            bash start.sh "$problem_id" "$directory"
        fi
    fi
fi

python3 test.py "$lang" "$directory"

if [[ -n "$file" ]]; then
    rm -rf "$directory/input"
    rm -rf "$directory/output"
fi
