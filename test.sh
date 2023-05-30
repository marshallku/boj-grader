#!/bin/bash

lang='cpp'

while [[ $# -gt 0 ]]; do
    case "$1" in
    -l | --lang)
        lang="$2"
        shift 2
        ;;
    *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done

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
    exit 1
    ;;
esac

python3 test.py "$lang"
