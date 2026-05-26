# 论文插图语义索引（Agent 必读）

> **目的**：图床 URL 只提供像素，不提供含义。任何需要**理解、引用、改写**论文插图的 Agent，必须先通过本规范把「图文件」关联到「结构化描述」，再决定是否下载 PNG 做视觉核对。

与 [`../agent_workflow/FIGURES_NOTION_GITHUB.md`](../agent_workflow/FIGURES_NOTION_GITHUB.md)（同步/推送/Notion 外链）配合使用。

---

## 1. 三个文件的分工

| 文件 | 作用 | Agent 何时读 |
|------|------|----------------|
| [`manifest.json`](manifest.json) | 路径、`caption`、`source`、Notion 页，以及 **`topic` / `purpose` / `illustrates` / `not_about` / `summary`**（本图要说明什么） | **理解插图意图时先读**；同步/外链时也要读 |
| [`descriptions.json`](descriptions.json) | 完整语义：`visual_description`、`axes`、`key_findings`、`key_numbers` | 需要写法细节或引用数字时读 |
| 本文件 `AGENT_READ_FIGURES.md` | 解析规则、禁止事项、与其他 Agent 的交接格式 | 第一次接触插图体系时读 |

**禁止**：仅凭 PNG 或 `caption` 猜图意（caption 只有标题，没有论证目的）。  
**推荐**：`manifest.json` 的 `purpose` + `topic` → `descriptions.json` → `source` 下 CSV/REPORT/result.json → 最后才 fetch PNG。

`manifest.json` 顶层 `topic_glossary` 解释各 `topic` 标签（如 `request_traffic_timeseries` = 请求波动时序，而非调度图）。

---

## 2. 从「图」反查描述（解析规则）

### 2.1 统一主键：`id`

每张图在 manifest / descriptions 中使用同一字符串主键，例如 `ch2_multi_qps`。

### 2.2 从输入反推 `id`（按优先级）

1. **显式 id**：正文、任务单、patch 脚本里写了 `figure_id: ch2_multi_qps` → 直接用。
2. **仓库相对路径**：`thesis/figures/ch2/ch2_multi_qps.png` → 去掉目录与扩展名 → `ch2_multi_qps`。
3. **GitHub raw URL**：  
   `https://raw.githubusercontent.com/wcwuwc/exp1-thesis-figures/main/thesis/figures/ch2/ch2_multi_qps.png`  
   → 取路径 basename 无扩展名 → `ch2_multi_qps`。
4. **Notion 图注**：用 `manifest.json` 里 `caption` 模糊匹配；匹配多条时**必须**用路径或 URL 消歧，不得猜。

### 2.3 加载描述

```python
import json
from pathlib import Path

root = Path(".../exp1")  # 仓库根
desc = json.loads((root / "thesis/figures/descriptions.json").read_text())
by_id = {x["id"]: x for x in desc["figures"]}
entry = by_id["ch2_multi_qps"]
# 必读字段：visual_description, key_findings, axes, data_source, key_numbers（若有）
```

### 2.4 关联字段用法

| 字段 | 所在文件 | 用法 |
|------|----------|------|
| `purpose` | manifest | **本图要论证/说明什么**（必读） |
| `topic` | manifest | 机器标签；查 `topic_glossary` |
| `illustrates` / `not_about` | manifest | 适用/不适用场景，避免与其它图混淆 |
| `summary` | manifest | 一句话摘要 |
| `visual_description` | descriptions | 图中应看到什么；写 Notion/论文时据此叙述 |
| `key_findings` | 可引用的结论 bullet；改数字前须回查 `related_data` / `source` |
| `key_numbers` | 允许直接引用的标量（仍建议核对 CSV） |
| `related_figures` | 同节其它图，避免重复叙述 |
| `related_data` | 复现统计的 CSV/脚本输出 |
| `source` + `provenance` | 回到实验目录核对 |
| `notion_page` | 该图应出现的 Notion 章节 |
| `mapping_note` | 脱敏 id 与生产名的对应说明（**正文仍用 model_00x**） |

---

## 3. 标准阅读流程（交给其它 Agent 的指令模板）

把下面整段复制给子 Agent 即可：

```text
【论文插图阅读协议】
1. 先读 thesis/figures/AGENT_READ_FIGURES.md 与 thesis/agent_workflow/FIGURES_NOTION_GITHUB.md。
2. 若任务涉及某张图，用 URL/路径解析 figure id，在 thesis/figures/descriptions.json 中 lookup。
3. 用该条的 visual_description + key_findings + key_numbers 理解含义；写正文时引用 figure_label（如「图2-1」）与 id。
4. 需要改数字或声称「图中可见 X」时：读 descriptions 中的 related_data / source，打开对应 CSV 或 REPORT.md / result.json 复核。
5. 禁止从 PNG 像素目测估计百分比、相关系数等；禁止在对外稿中恢复 anonymization_mapping 中的真实业务名。
6. 仅当描述与源码/数据冲突时，再下载 raw_url 上的 PNG 做视觉核对，并在 OUTPUT 中注明冲突点。
```

---

## 4. 命名与脱敏

- 论文与 Notion：**只写** `model_001` … `model_009`。
- 内部对照：[`data/raw/newdata/anonymization_mapping.csv`](../../data/raw/newdata/anonymization_mapping.csv)（例如 `model_003`↔tianji，`model_008`↔tarot）。**勿**在对外材料写回原名。
- 第二章定量：**9** 个参与全局调度的活跃模型；公司约 **32** 模型线上，冷模型不进本章图。

---

## 5. 维护与再生

| 操作 | 命令 |
|------|------|
| 新增图到 manifest 后生成/更新描述 | `python3 thesis/scripts/build_figure_descriptions.py` |
| 复制 PNG 到 thesis/figures | `python3 thesis/scripts/sync_thesis_figures.py` |
| 丰富语义 | 编辑 `thesis/scripts/build_figure_descriptions.py` 内 `META` / `CH4_TEMPLATES`，再运行 build |

第二章精细描述的数据依据：  
`research/demand_inference/scripts/outputs/ch2_211/model_traffic_summary.csv`  
脚本：`research/demand_inference/scripts/analyze_ch211_newdata.py`

---

## 6. 与其它 Agent 工作流的衔接

- `02_cause_diagnosis`：优先引用 `ch2_*` 三张图及 descriptions 中 §2.1.1 数字。
- `03_method_design` / `04_model_formulation`：第三章图见 `ch3_*`；分布结论以 `dice_best_distribution.csv` 为准。
- `06_results_analysis`：第四章图见 `ch4_*`；数值以各 `outputs/*/REPORT.md` 与 `result.json` 为准。

在阶段 `OUTPUT.md` 中引用图时建议格式：

```markdown
- **图2-1** (`ch2_multi_qps`)：头部 model_003 占约 68% 均值流量（见 descriptions.json / model_traffic_summary.csv）。
```

---

## 7. 完整性检查

- [ ] 每个 manifest `id` 在 `descriptions.json` 中有一条且含 `visual_description`
- [ ] `build_figure_descriptions.py` 运行无 “without visual_description”
- [ ] 改图后已重新 sync 并 push GitHub 图仓
- [ ] Notion 外链 URL 与 manifest `path` 一致
