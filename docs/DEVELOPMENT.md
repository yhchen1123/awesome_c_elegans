# DEVELOPMENT — awesome_c_elegans 运维手册

本文件面向仓库维护者：运行模式、本地流水线、更换 LLM、调整查询、重跑分类、手动/批量添加文献、GitHub 侧设置。

仓库地址：<https://github.com/yhchen1123/awesome_c_elegans>

## 运行模式：本地定时任务（当前生效）

当前生效的运行模式是 **Kimi Work 本地定时任务「每周文献检索与更新（本地 agent 分类）」**（每周一 14:00 Asia/Shanghai = 06:00 UTC，绑定本工作区）：

- fetch / dedupe 走 `scripts/` 脚本；**分类由 Kimi Work agent 亲自完成**，不调用外部 LLM API，无需配置 `LLM_API_KEY`；
- 分类规则与 `scripts/classify.py` 的 SYSTEM_PROMPT 完全一致（铁律：书目字段只来自数据源 API 元数据）；
- **保密红线**：本仓库公开。所有入库文本（尤其 relevance_note）只使用公开科学语言，不得包含任何未公开的项目内部信息；该约束已写入定时任务的最高优先级规则；
- 每次运行的变更提交到本地分支 `auto/weekly-update-<日期>`，**main 不被自动改动**；维护者审 diff 后 `git merge` 合并并推送，即完成审计闭环；
- 若上次更新分支尚未合并，任务会跳过该周运行以避免重复分类（桌面通知会提醒合并）；
- 仓库内的 GitHub Actions workflows 保留作备选：将来在 GitHub 配置 `LLM_API_KEY` 后可启用云端链路，两者任选其一。**本地模式生效期间，请在 GitHub Actions 页禁用 `weekly-literature-update` 与 `monthly-digest`**，否则每周会因缺 secret 产生失败邮件。

## 环境准备

```bash
python3.12 -m venv .venv && source .venv/bin/activate   # 或任何 Python 3.12 环境
pip install -r requirements.txt                          # requests / pyyaml / jsonschema（仅此三项）
```

所有脚本只依赖这三项 + 标准库；arXiv 抓取在 Python HTTP 栈被其 CDN 按 TLS 指纹拦截（HTTP 406）时自动回退到系统 `curl`（macOS / Linux / GitHub Actions 均自带）。

## 本地运行流水线

```bash
# 1. 抓取候选（默认窗口 = config/queries.yaml 的 window_days=10；冒烟测试可放宽）
python3 scripts/fetch.py --out build/candidates_raw.json --report build/fetch_report.json
python3 scripts/fetch.py --window-days 30 --out build/candidates_raw.json --report build/fetch_report.json

# 2. 去重（DOI → arXiv/bioRxiv ID → 标题指纹 三级；含 preprint→published 合并）
python3 scripts/dedupe.py --in build/candidates_raw.json --db data/papers.json --out build/candidates_new.json

# 3. 分类（二选一）
#    a) 云端/API 模式：需要 LLM_API_KEY
export LLM_API_KEY=sk-...
python3 scripts/classify.py --in build/candidates_new.json --db data/papers.json
#    b) 本地模式（当前默认）：由 Kimi Work agent 按 classify.py 的 SYSTEM_PROMPT 亲自分类，
#       无需 LLM_API_KEY（定时任务走的就是这条路）

# 4. 渲染 + 校验（CI 强制；渲染产物禁止手工编辑）
python3 scripts/render.py
python3 scripts/validate.py          # 内含 render.py --check
npx --yes awesome-lint README.md     # lint CI 同款检查
```

## 月度 digest

`scripts/digest.py` 生成上一自然月的简报：按 C0–C9 分类分节（可选 LLM 生成小节中文摘要）、OpenAlex 全库引用数刷新（Citation movers Top 10）、撤稿扫描（命中自动置 `retracted: true`）：

```bash
python3 scripts/digest.py            # 完整运行（引用/撤稿会写回 papers.json）
python3 scripts/digest.py --dry-run  # 只生成分节骨架，无网络、不写库
python3 scripts/digest.py --month 2026-09 --summaries build/section_summaries.json --insights build/insights_2026-09.md
# 本地 agent 模式：--summaries 注入 agent 撰写的分节摘要（JSON: 分类码 -> 摘要），
#                  --insights 注入 agent 撰写的交叉洞察 markdown（方法组合/张力/猜想种子）
```

digest 结构：分类分节（含小节摘要）→ **Cross-links 交叉洞察**（不同论文方法/发现/观点之间的相互作用，目标是催生新猜想与新方法）→ Citation movers。交叉洞察只允许基于已收录条目的公开信息撰写，便于读者与 AI 二次加工。

云端 `monthly-digest.yml`（每月 1 日 06:00 UTC）保留作备选；本地模式的月度定时任务尚未创建（见 Roadmap）。

## 更换 LLM 供应商（云端/API 模式）

分类/摘要走 OpenAI-compatible 接口，三个环境变量即可切换：

| 变量 | 默认 | 说明 |
|---|---|---|
| `LLM_API_KEY` | （无，必填） | API 密钥，仓库 Settings → Secrets and variables → Actions → Secrets |
| `LLM_BASE_URL` | `https://api.moonshot.cn/v1` | 端点，仓库 Variables（vars） |
| `LLM_MODEL` | `kimi-k2-0905-preview` | 模型名，仓库 Variables（vars） |

- 换供应商：改 `LLM_BASE_URL` + `LLM_MODEL` + 对应的 `LLM_API_KEY` 即可，代码零改动。
- 端点不支持 `response_format: json_object` 时，`classify.py` 自动回退为 prompt 约束 + 严格 JSON 解析。
- 若默认模型在账户不可用，任选同供应商其他模型名填入 `LLM_MODEL` 即可；输出校验与温度 0 设置不变。
- 推荐额外配置 Secret `EPMC_EMAIL`：Europe PMC / OpenAlex 礼貌池标识，降低限流概率。

## 新增 / 收紧检索查询

编辑 `config/queries.yaml`：

- Europe PMC 查询支持 `AND/OR/NOT`、括号、`TITLE_ABS:"..."`、`FIRST_PDATE:[...]`、`SRC:PPR`；窗口占位符 `{from_date}` / `{to_date}` 由 fetch.py 替换。
- arXiv 查询支持 `all:"..."`、`cat:xx.YY` 组合。**注意 OR 组必须加括号**——`cat:cs.LG OR cat:q-bio.QM AND ...` 会按 `cat:cs.LG OR (cat:q-bio.QM AND ...)` 解释（AND 优先级更高），命中整个 cs.LG 分类（2026-09-28 已修正 methods_dynamics 查询）。
- 每条 query 的 `categories_hint` 会作为分类提示传给分类器。
- 收紧（减少噪声）：增加 `AND` 限定词或缩窄主题词；放宽：反之。
- **查询变更须走 PR 并说明理由**（影响未来所有自动分类结果），合并前本地用 `--window-days 30` 冒烟一次。

## 重跑历史分类（taxonomy 变更后）

taxonomy 调整后，对既有条目重新分类（结果同样经审计分支，不直接推 main）：

```bash
# 重跑 2026-09-01 以来入库的条目（manual 精标条目默认跳过）
python3 scripts/classify.py --reclassify --since 2026-09-01
# 连人工精标条目一起重跑
python3 scripts/classify.py --reclassify --since 2026-09-01 --include-manual
# 然后渲染 + 校验，提交审计分支
python3 scripts/render.py && python3 scripts/validate.py
```

重分类只更新 LLM 拥有的字段（categories/tags/tier/evidence/standards/relevance_note/confidence/needs_review）；标题、作者、DOI 等书目字段永远以数据源 API 元数据为准。需要 `LLM_API_KEY`；无 key 时由 Kimi Work agent 按同一规则代跑。

## 添加文献

### 单篇（API 模式）

```bash
python3 scripts/classify.py --add 10.1126/science.aax1971
# 拉取 CrossRef/Europe PMC 元数据 → LLM 分类 → 打印拟入库条目 → 人工确认后入库
python3 scripts/classify.py --add 10.1126/science.aax1971 --yes   # 跳过交互确认
```

### 单篇 / 批量（本地 agent 模式，无需 LLM_API_KEY）

直接把文献（PDF、DOI 清单或标题清单）交给 Kimi Work agent：agent 读摘要、按 taxonomy 甄别收录口径、用 CrossRef/EPMC/arXiv 核实元数据、写入 `papers.json` 并渲染校验。已有成规模实践：2026-09-28 从 82 篇 PDF 归档中甄别收录 64 篇（剔除 10 篇库内重复 + 8 篇口径不符）。

### 通用纪律

- 入库一律 `source: "manual"` 或 `epmc` / `arxiv` / `issue`，书目字段只用 API 元数据；
- 变更提交到 `auto/*` 审计分支，合并进 main 后推送；随后 `render.py && validate.py` 必须全绿。

## README 渲染的 lint 兼容约定（改 render.py 前必读）

`README.md` 受 `awesome-lint` 约束，render.py 因此采用以下约定（`categories/*.md` 不受 lint，保留富格式）：

1. H1 用 HTML 写法 `<h1>Awesome <i>C. elegans</i> Embryogenesis</h1>` —— 保持物种名小写（awesome-lint 的 title-case 规则不检查 HTML 标题）。
2. 每篇文献在 README 只出现一次（主分类 = `categories[0]`），多分类条目附 `also filed under` 提示；分类页含完整交叉收录（double-link 规则禁止主链接重复）。
3. 条目格式 `- [标题](url) - 作者, *期刊* 年份 ` + 行内代码徽章 + `<br>` + 斜体中文注解（em-dash 分隔符、加粗链接均不合规）；分类节标题下的中文副标题行格式为 `**中文名** · C0`（纯粗体段落会被 no-emphasis-as-heading 误伤）。
4. README 不设 License 章节（awesome-license 规则禁止；许可证见根目录 `LICENSE`）。
5. 本地新建分支后跑 lint 前，需 `git config branch.<分支名>.remote origin`（awesome-github 规则要读分支远端配置，否则误报「not a valid git repository」）；CI 中 checkout 自动配置，不受影响。

## GitHub 侧一次性设置

- [ ] 仓库主页加 description 与 topics（`awesome`、`awesome-list`），否则 lint CI 的 github 规则报错；
- [ ] Settings → Branches：main 开启分支保护（Require a pull request before merging）；
- [ ] 本地模式生效期间：Actions 页禁用 `weekly-literature-update` 与 `monthly-digest`；
- [ ] 若启用云端链路：Secrets 配 `LLM_API_KEY`（必需）、`EPMC_EMAIL`（推荐），Variables 可选 `LLM_BASE_URL` / `LLM_MODEL`。

## Roadmap

- **月度 digest 本地定时任务**：每月 1 日跑 `digest.py`（分类简报 + 引用刷新 + 撤稿扫描），与周更任务同模式；
- **硬标准联动**：新论文命中 `standards` 标签（embryo-level-split / open-loop-rollout / uncertainty-quantified / perturbation-holdout / shortcut-audit）时，自动开 issue 提醒维护者关注。

## 知识图谱可视化（webapp/）

`webapp/` 是基于 React + Vite + Tailwind + shadcn/ui 的文献知识图谱界面（Sigma.js WebGL 渲染 + ForceAtlas2 确定性布局 + Louvain 聚类）：

- 数据来自 `scripts/graph.py`（`data/papers.json` 的渲染产物，确定性生成）：论文/分类/作者/期刊/标签五类节点，belongs_to / authored_by / published_in / has_tag / related（共同作者+主题重叠）五类边；作者与期刊节点仅保留库内 ≥2 篇的实体以保持可读性；
- **每次 papers.json 变更后重新生成**：`python3 scripts/graph.py`（输出 `webapp/public/graph-data.json`，已入库以支持静态部署）；
- 本地开发：`cd webapp && npm install && npm run dev`；构建：`npm run build`（`dist/` 为纯静态站点，可直接部署 GitHub Pages / Vercel / Netlify）；
- 功能：分类/层级/证据筛选、标题作者期刊搜索、作者·期刊·标签·关联边开关、节点详情面板（含关联文献跳转与原文链接）、选中节点相机飞行定位与邻居高亮；
- 布局只在数据加载时计算一次（环形初始化 + ForceAtlas2，同一输入同一布局），筛选仅切换节点/边的 hidden 属性，位置稳定不跳动；
- 注意：sigma 把节点/边的 `type` 属性当作渲染程序名，语义类型在图谱构建时改名为 `nodeType` / `linkType`（构建侧已处理）。
