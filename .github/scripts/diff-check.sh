#!/bin/bash
github_sha="$1"
diff_output=$(git diff-tree --no-commit-id --name-only -r "$github_sha")
readarray -t diffs <<<"$diff_output"

file_pattern='solutions/[0-9]+/solution\.(py|cpp)'

for file in "${diffs[@]}"; do
    if [[ "$file" =~ $file_pattern ]]; then
        echo 'status=TRUE' >>"$GITHUB_OUTPUT"
        exit 0
    fi
done

echo 'status=FALSE' >>"$GITHUB_OUTPUT"
