#!/bin/bash

SRC_DIR="source"

REPO_URL="https://github.com/username/repo.git"

if [ ! -d "$SRC_DIR" ]; then
  git clone "$REPO_URL" "$SRC_DIR"
fi

cd "$SRC_DIR"

git pull

find . -name "*.py" -exec sed -i '/^\s*#/d' {} +

python manage.py runserver my_project
