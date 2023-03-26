#!/usr/bin/env bash

cd ~/workspace/cmini
git add -A authors.json corpora.json likes.json layouts
git commit -m "Sync data"
git push