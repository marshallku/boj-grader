#!/bin/bash
if [[ -z $(git status --porcelain) ]]; then
    exit 0
fi

git config user.name github-actions[bot]
git config user.email 41898282+github-actions[bot]@users.noreply.github.com
git add -A
git commit -m "$MESSAGE"
git push
