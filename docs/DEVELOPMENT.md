# DEVELOPMENT — awesome_c_elegans 运维手册

本文件面向仓库维护者：如何本地运行流水线、更换 LLM 供应商、调整检索查询、重跑分类、手动添加文献。

## 运行模式：本地定时任务（当前生效）

当前生效的运行模式是 **Kimi Work 本地定时任务「每周文献检索与更新（本地 agent 分类）」**（每周一 14:00 Asia/Shanghai = 06:00 UTC）：

- fetch / dedupe 走 `scripts/` 脚本；**分类由 Kimi Work agent 亲自完成**，不调用外部 LLM API，无需配置 `LLM_API_KEY`；
- 分类规则与 `scripts/classify.py` 的 SYSTEM_PROMPT 完全一致（铁律：书目字段只来自数据源 API 元数据）；
- 每次运行的变更提交到本地分支 `auto/weekly-update-<日期>`，**main 不被自动改动**；维护者审 diff 后 `git merge` 合并，推送远端后即完成审计闭环；
- 若上次更新分支尚未合并，任务会跳过该周运行以避免重复分类（桌面通知会提醒合并）；
- 仓库内的 GitHub Actions workflows 保留：将来在 GitHub 配置 `LLM_API_KEY` 后可直接启用云端链路，两者任选其一。

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

# 3. LLM 分类（需要 LLM_API_KEY）
export LLM_API_KEY=sk-...
python3 scripts/classify.py --in build/candidates_new.json --db data/papers.json

# 4. 渲染 + 校验（CI 强制；渲染产物禁止手工编辑）
python3 scripts/render.py
python3 scripts/validate.py          # 内含 render.py --check
npx --yes awesome-lint README.md     # lint CI 同款检查
```

## 更换 LLM 供应商

分类/摘要走 OpenAI-compatible 接口，三个环境变量即可切换：

| 变量 | 默认 | 说明 |
|---|---|---|
| `LLM_API_KEY` | （无，必填） | API 密钥，仓库 Settings → Secrets and variables → Actions → Secrets |
| `LLM_BASE_URL` | `https://api.moonshot.cn/v1` | 端点，仓库 Variables（vars） |
| `LLM_MODEL` | `kimi-k2-0905-preview` | 模型名，仓库 Variables（vars） |

- 换供应商：改 `LLM_BASE_URL` + `LLM_MODEL` + 对应的 `LLM_API_KEY` 即可，代码零改动。
- 端点不支持 `response_format: json_object` 时，`classify.py` 自动回退为 prompt 约束 + 严格 JSON 解析。
- 若默认的 `kimi-k2-0905-preview` 在你的账户不可用，任选同供应商其他模型名填入 `LLM_MODEL` 变量即可（如 `kimi-k2-turbo-preview` 或更新的 K2 系列）；输出校验与温度 0 设置不变。
- 推荐额外配置 Secret `EPMC_EMAIL`：Europe PMC / OpenAlex 礼貌池标识，降低限流概率。

## 新增 / 收紧检索查询

编辑 `config/queries.yaml`：

- Europe PMC 查询支持 `AND/OR/NOT`、括号、`TITLE_ABS:"..."`、`FIRST_PDATE:[...]`、`SRC:PPR`；窗口占位符 `{from_date}` / `{to_date}` 由 fetch.py 替换。
- arXiv 查询支持 `all:"..."`、`cat:xx.YY` 组合。
- 每条 query 的 `categories_hint` 会作为分类提示传给 LLM。
- 收紧（减少噪声）：增加 `AND` 限定词或缩窄主题词；放宽：反之。
- **查询变更须走 PR 并说明理由**（影响未来所有自动分类结果），合并前本地用 `--window-days 30` 冒烟一次。

## 重跑历史分类（taxonomy 变更后）

taxonomy 调整后，对既有条目重新分类（结果同样经 PR 审计，不直接推 main）：

```bash
# 重跑 2026-09-01 以来入库的条目（manual 精标条目默认跳过）
python3 scripts/classify.py --reclassify --since 2026-09-01
# 连人工精标条目一起重跑
python3 scripts/classify.py --reclassify --since 2026-09-01 --include-manual
# 然后渲染 + 校验，提交 PR
python3 scripts/render.py && python3 scripts/validate.py
```

重分类只更新 LLM 拥有的字段（categories/tags/tier/evidence/standards/relevance_note/confidence/needs_review）；标题、作者、DOI 等书目字段永远以数据源 API 元数据为准。

## 手动添加单篇文献

```bash
python3 scripts/classify.py --add 10.1126/science.aax1971
# 拉取 CrossRef/Europe PMC 元数据 → LLM 分类 → 打印拟入库条目 → 人工确认后入库
python3 scripts/classify.py --add 10.1126/science.aax1971 --yes   # 跳过交互确认
```

随后 `render.py && validate.py`，提交 PR。

## README 渲染的 lint 兼容约定（改 render.py 前必读）

`README.md` 受 `awesome-lint` 约束，render.py 因此采用以下约定（`categories/*.md` 不受 lint，保留规格中的富格式）：

1. H1 用 HTML 写法 `<h1>Awesome <i>C. elegans</i> Embryogenesis</h1>` —— 保持物种名小写（awesome-lint 的 title-case 规则不检查 HTML 标题）。
2. 每篇文献在 README 只出现一次（主分类 = `categories[0]`），多分类条目附 `also filed under` 提示；分类页含完整交叉收录（double-link 规则禁止主链接重复）。
3. 条目格式 `- [标题](url) - 作者, *期刊* 年份 ` + 行内代码徽章 + `<br>` + 斜体中文注解（em-dash 分隔符、加粗链接均不合规）。
4. README 不设 License 章节（awesome-license 规则禁止；许可证见根目录 `LICENSE`）。

## Roadmap

- **硬标准联动**：新论文命中 `standards` 标签（embryo-level-split / open-loop-rollout / uncertainty-quantified / perturbation-holdout / shortcut-audit）时，自动开 issue 提醒维护者关注。
