name: Build search indexes

on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - "gpts.csv"
      - "gpts/**"
      - "scripts/build_index.py"

permissions:
  contents: write   # lai drīkst iekomitēt docs/*.json

jobs:
  build-indexes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }

      - name: Build indexes (modules/terms/articles)
        run: python scripts/build_index.py

      - name: Commit docs/*.json if changed
        run: |
          if ! git diff --quiet -- docs/index.json docs/terms.json docs/articles.json; then
            git config user.name  "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add docs/index.json docs/terms.json docs/articles.json
            git commit -m "Rebuild search indexes [skip ci]"
            git push
          else
            echo "No changes."
          fi
