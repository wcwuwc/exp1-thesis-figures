# Thesis figures (`exp1-thesis-figures`)

Stable paths for thesis / Notion / LaTeX. Sources are copied from `research/*/outputs/` via manifest.

## GitHub remote (figures-only public repo)

| Item | Value |
|------|--------|
| Repo | [wcwuwc/exp1-thesis-figures](https://github.com/wcwuwc/exp1-thesis-figures) |
| Raw URL prefix | `https://raw.githubusercontent.com/wcwuwc/exp1-thesis-figures/main/` |

**Agent 完整说明：** [`../agent_workflow/FIGURES_NOTION_GITHUB.md`](../agent_workflow/FIGURES_NOTION_GITHUB.md)

**One-time setup** (repo already exists on GitHub):

```bash
git remote add github git@github.com:wcwuwc/exp1-thesis-figures.git 2>/dev/null || true
python3 thesis/scripts/sync_thesis_figures.py
git add thesis/figures/
git commit -m "figures: sync from experiment outputs"
# 仅推 figures 提交，勿推整个 exp1 main：
git push github HEAD:refs/heads/main
```

## Daily workflow

```bash
python3 thesis/scripts/sync_thesis_figures.py
python3 thesis/scripts/sync_thesis_figures.py --markdown   # Notion 预览
git add thesis/figures/ && git commit -m "figures: update ch4 plots"
git push github HEAD:refs/heads/main
```

⚠️ Do **not** use `git push github main` unless `main` only contains figure commits.

## Layout

- `ch3/` — demand / QPM
- `ch4/` — solver comparison & sensitivity
- `manifest.json` — source paths, captions, Notion page URLs
