---
name: dev-favorites-updater
description: Execute the complete daily update workflow for a personal development favorites collection. Covers parallel web searches (tech news, consumer brand AI, stock market, arXiv papers, GitHub trending), writes categorized Markdown files, performs four-question deep analysis, regenerates favorites.xlsx with openpyxl charts and conditional formatting, rebuilds the interactive dashboard.html, syncs to GitHub Pages, and commits to the git repository. Use when the user asks to run the daily update, sync favorites, or perform any combination of these tasks.
description_zh: "执行个人开发收藏集的每日更新工作流，涵盖抓取、分类、去重和发布"
---

# Dev Favorites Daily Updater

## Overview

Maintain and grow a personal development favorites collection stored in `D:\MyDevFavorites` and synced to `https://github.com/sjkncs/my-dev-favorites`.

Seven categories: Tips, Repos, Consumer AI, Tech News, Stock Market, Papers, Analysis Reports.

## Directory Structure

```
D:\MyDevFavorites\
├── favorites.md          # Master Markdown overview (with changelog)
├── favorites.json        # Machine-readable source of truth
├── favorites.xlsx        # Excel view with charts and conditional formatting
├── index.html            # Dashboard copy for GitHub Pages
├── CNAME                 # sjkncs.com (DO NOT DELETE)
├── .nojekyll             # Bypass Jekyll processing (DO NOT DELETE)
├── 01-tips/              # CLI tools, IDE tricks
├── 02-repos/             # Trending open-source projects
├── 03-consumer-ai/       # Brand AI research
├── 04-tech-news/         # Daily news digests
├── 05-papers/            # Conference paper collections
├── 06-stock-market/      # A-shares, US stocks, HK stocks
├── 07-analysis-reports/  # Four-question analysis + dashboard
└── archive/              # Historical archives
```

## Complete Daily Update Workflow

### Step 1: Parallel Search (5 streams)

Run ALL searches simultaneously for maximum efficiency:

**Stream 1 — Tech News (AI/Semiconductor/Chips)**
```
Search queries:
- "AI semiconductor chip news today {date}"
- "AI 半导体 芯片 新闻 {date}"
- "{specific_topic} latest news" (for trending topics)
Target: 3-5 high-impact stories
```

**Stream 2 — Consumer Brand AI**
```
Search queries (cover ALL Tier 1 brands daily):
- "{brand} AI 2026 最新动态" for each brand
- "瑞幸 星巴克 库迪 喜茶 奈雪 蜜雪冰城 霸王茶姬 AI"
- "美团 饿了么 千问App AI 智能"
Target: New product launches, feature updates, strategic moves
```

**Stream 3 — Stock Market**
```
Search queries:
- "A股 上证 深证 创业板 科创板 {date} 收盘"
- "美股 纳斯达克 标普500 道琼斯 {date}"
- "港股 恒生指数 恒生科技 {date}"
- "AI量化交易 证券APP 最新动态"
Target: Index values, % changes, sector impacts, major events
```

**Stream 4 — arXiv Papers**
```
Search queries:
- "arXiv CV ML NLP RL papers {month} {year} new"
- "arXiv 2606 paper agent RL" (adjust month prefix)
- Check: https://arxiv.org/list/cs.CV/recent, cs.CL/recent, cs.LG/current
Target: 5-8 notable papers with clear contributions
```

**Stream 5 — GitHub Trending**
```
Search queries:
- "GitHub trending AI developer tools {month} {year}"
- "GitHub trending repositories"
- Check: https://github.com/trending, https://ossinsight.io/trending/ai
Target: 2-3 interesting repos with star counts
```

### Step 2: Read Existing State

Before writing, read current files to understand what's already there:
```
Read: favorites.json (source of truth for all data)
Read: favorites.md (check changelog format)
Read: Existing dated files for today (if any)
```

### Step 3: Write Categorized Files

Create dated Markdown files with `YYYY-MM-DD` prefix:

**04-tech-news/YYYY-MM-DD-news.md**
```markdown
# YYYY-MM-DD AI/半导体/芯片 科技新闻

## 1. {Title}
{One-paragraph summary}
Source: {Source}
重要程度: {高/中/低}

## 2. {Title}
...
```

**03-consumer-ai/YYYY-MM-DD-brands.md**
```markdown
# YYYY-MM-DD 消费品牌AI动态

## 品牌动态

### {Brand Name}
{Description of AI initiative/update}
涉及技术: {tech stack}

### {Brand Name}
...
```

**06-stock-market/YYYY-MM-DD-market.md**
```markdown
# YYYY-MM-DD 股市行情

## A股（{date}收盘）
| 指数 | 收盘 | 涨跌幅 |
|------|------|--------|
| 上证综指 | {value} | {change}% |
| 深证成指 | {value} | {change}% |
| 创业板指 | {value} | {change}% |
| 科创50 | {value} | {change}% |

## 美股（{date}收盘）
...

## 港股
...

## 重大事件
1. ...
2. ...
```

**05-papers/YYYY-MM-DD-papers.md**
```markdown
# YYYY-MM-DD 本周arXiv前沿论文

### 1. {Title}
- **机构**: {institution}
- **摘要**: {summary}
- **Link**: [arXiv:{id}]({url})
```

### Step 4: Four-Question Deep Analysis

For EACH important item (news, paper, brand update, repo), answer:

**Q1: 它真正想解决的问题是什么？**
剥离营销包装，看本质。问：如果没有这个产品/论文，世界会缺什么？

**Q2: 它声称的贡献是什么？**
对照实际效果评估。问：声称的数字有第三方验证吗？基线是什么？

**Q3: 最可能被reviewer攻击的地方在哪里？**
致命缺陷/盲区/竞争壁垒。问：如果我是审稿人/投资人，我会质疑什么？

**Q4: 如果我是同方向从业者，应该精读/学习/模仿/跳过什么？**
- 🎓 博士生：精读哪些方法，跳过哪些工程细节
- 👨‍💻 工程师：学习哪些架构，模仿哪些实现
- 💰 投资人：关注哪些信号，跳过哪些噪音

Write to `07-analysis-reports/YYYY-MM-DD-analysis.md`.

### Step 5: Update Master Files

**favorites.json** — Append new items, update `meta.lastUpdated` and counts.

**favorites.md** — Update date header and append to changelog table:
```markdown
| YYYY-MM-DD | {Summary of new content} |
```

**favorites.xlsx** — Regenerate using openpyxl with:
- 7 sheets: 概览, 消费品牌AI, AI大模型, 股市趋势, 半导体指标, 顶会论文, 科技新闻
- Charts: RadarChart (consumer AI + model scores), BarChart (API pricing + semiconductor), LineChart (stock trends)
- Conditional formatting: ColorScaleRule (red→yellow→green for scores 0-10)
- Formulas: SUM, AVERAGE (never hardcode computed values)
- See [xlsx-generation.md](xlsx-generation.md) for Python template

### Step 6: Rebuild Dashboard

Rebuild `07-analysis-reports/dashboard.html` with these requirements:
- Single-file HTML, inline CSS + JS, Chart.js CDN
- Dark theme (bg: #1a1a2e, cards: #16213e, accent: #0f3460)
- Chinese interface, responsive layout
- 7 chart modules:
  - (a) Consumer brand AI radar (5 dimensions: AI深度/用户体验/部署规模/技术壁垒/商业化)
  - (b) AI model radar (6 dimensions) + API price bar chart
  - (c) Stock market line chart (dual Y-axis: 上证 left, 纳斯达克/恒生科技 right)
  - (d) Semiconductor bar chart (horizontal, key metrics)
  - (e) Papers table (sortable, with award highlights)
  - (f) Expandable four-question analysis cards
  - (g) Tech news timeline (CSS-based, color-coded by importance)
- All data from favorites.json (inline in JS DATA object)

### Step 7: Sync to GitHub Pages

```bash
copy D:\MyDevFavorites\07-analysis-reports\dashboard.html D:\MyDevFavorites\index.html
```

Verify CNAME and .nojekyll still exist in repo root.

### Step 8: Commit and Push

```bash
cd D:\MyDevFavorites
git add .
git commit -m "update: $(date +%Y-%m-%d) daily update"
git push origin master
```

Handle rejections:
```bash
# If rejected (remote has changes):
git pull --rebase origin master && git push origin master

# If remote not set:
git remote add origin https://github.com/sjkncs/my-dev-favorites.git
```

### Step 9: Verify Deployment

```bash
# Check Pages status
gh api repos/sjkncs/my-dev-favorites/pages --jq '.status + " | CNAME: " + .cname'

# If Pages shows "errored" for >5 minutes, alert user
```

## Priority Brand Monitoring List

**Tier 1 — Daily Check**:
- 瑞幸咖啡 (Luckin) — MCP/CLI/Skill, AI开放平台
- 星巴克 (Starbucks) — Deep Brew, Green Dot Assist
- 库迪咖啡 (Cotti) — 智慧运营体系
- 喜茶 (HeyTea) — 全套智能设备, ChatBI
- 奈雪的茶 (Nayuki) — AI溯源预警
- 蜜雪冰城 (Mixue) — 雪王爱智慧AI公司
- 霸王茶姬 (ChaPanda) — 智能调饮+茶茶圈
- 茶百道 — DeepSeek/豆包大模型接入
- 阿里千问App — 跨品牌"一句话点奶茶"
- 美团 — AI智能推荐/配送, LongCat大模型
- 饿了么 — AI配送调度

**Tier 2 — Weekly Check**:
- 肯德基 (KFC) — AI点餐助手"小K"
- 麦当劳 (McDonald's) — RGM BOSS, 汉堡大学AI
- 海底捞 (Haidilao) — AI智慧巡检+智能体机器人
- 抖音/字节 — 豆包大模型消费场景

## Guardrails

- Do NOT permanently delete user files
- Back up originals before bulk edits
- Do NOT delete CNAME, .nojekyll, or .gitignore from repo root
- Always copy dashboard.html → index.html before committing
- If Excel regeneration fails, warn but do not block other updates
- If push rejected, always resolve with git pull --rebase
- All content in Chinese (中文)

## Additional Resources

- For Excel generation template, see [xlsx-generation.md](xlsx-generation.md)
- For dashboard HTML template structure, see [dashboard-template.md](dashboard-template.md)
