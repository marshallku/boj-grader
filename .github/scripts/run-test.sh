#!/bin/bash
github_sha="$1"
diff_output=$(git diff-tree --no-commit-id --name-only -r "$github_sha")
readarray -t diffs <<<"$diff_output"

file_pattern='solutions/[0-9]+/solution\.(py|cpp)'

for file in "${diffs[@]}"; do
    if [[ "$file" =~ $file_pattern ]]; then
        bash test.sh -f "$file" --write-output &
    fi
done

for job in $(jobs -p); do
    wait "$job"
done
