# Thesis figures (`exp1-thesis-figures`)

Stable paths for thesis / Notion / LaTeX. Sources are copied from `research/*/outputs/` via manifest.

## GitHub remote (figures-only public repo)

| Item | Value |
|------|--------|
| Repo | [wcwuwc/exp1-thesis-figures](https://github.com/wcwuwc/exp1-thesis-figures) |
| Raw URL prefix | `https://raw.githubusercontent.com/wcwuwc/exp1-thesis-figures/main/` |

**One-time setup** (after creating an empty public repo on GitHub):

```bash
# From repo root — only if this clone has no github remote yet
git remote add github git@github.com:wcwuwc/exp1-thesis-figures.git

# Sync plots, commit, push figures tree (first push may use -u)
python3 thesis/scripts/sync_thesis_figures.py
git add thesis/figures/
git commit -m "figures: sync from experiment outputs"
git push github main
```

To publish **only** `thesis/figures/` without mirroring the whole `exp1` tree, use a separate clone or [git subtree split](https://git-scm.com/docs/git-subtree); the manifest and script stay the same.

## Daily workflow

```bash
# 1. Re-run experiments (if needed), then:
python3 thesis/scripts/sync_thesis_figures.py

# 2. Preview Notion markdown lines:
python3 thesis/scripts/sync_thesis_figures.py --markdown

# 3. Commit & push to GitHub
git add thesis/figures/ && git commit -m "figures: update ch4 plots" && git push github main
```

Agent can insert images in Notion with URLs from `manifest.json` (`github.base_url` + `path`).

## Layout

- `ch3/` — demand / QPM
- `ch4/` — solver comparison & sensitivity
- `manifest.json` — source paths, captions, Notion page URLs
