# Dashboard HTML Template Structure

## Overview

Single-file HTML dashboard with inline CSS + JS, using Chart.js CDN. Dark theme, Chinese interface, responsive layout.

## File Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的开发收藏夹 - 数据仪表盘</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>/* inline CSS */</style>
</head>
<body>
  <!-- A) Header with stats bar -->
  <!-- B) Consumer AI Radar Chart -->
  <!-- C) AI Model Radar + API Price Bar -->
  <!-- D) Stock Market Line Chart (dual Y-axis) -->
  <!-- E) Semiconductor Bar Chart -->
  <!-- F) Papers Table (sortable) -->
  <!-- G) Four-Question Analysis (expandable cards) -->
  <!-- H) Tech News Timeline (CSS-based) -->
  <!-- I) Footer -->
  <script>/* inline JS with DATA object + chart initialization */</script>
</body>
</html>
```

## CSS Theme Variables

```css
:root {
  --bg: #1a1a2e;
  --card: #16213e;
  --accent: #0f3460;
  --text: #e0e0e0;
  --accent-light: #1a5276;
  --highlight: #e94560;
  --gold: #f0c040;
  --green: #2ecc71;
  --blue: #3498db;
  --purple: #9b59b6;
  --orange: #e67e22;
  --cyan: #1abc9c;
  --red: #e74c3c;
  --radius: 12px;
  --shadow: 0 4px 20px rgba(0,0,0,0.3);
}
```

## JS DATA Object Structure

```javascript
var DATA = {
  consumerAI: [
    {brand:"品牌名", tool:"工具名", scores:{aiDepth:N, ux:N, scale:N, techBarrier:N, commercialization:N}},
    // ... all brands from favorites.json consumerAI
  ],
  aiModels: [
    {name:"模型名", vendor:"厂商", scores:{reasoning:N, coding:N, multimodal:N, price:N, context:N, ecosystem:N}, pricing:{input:N, output:N}},
    // ... all models from favorites.json aiModels
  ],
  stockMarket: [
    {date:"YYYY-MM", a:N, us:N, hk:N},
    // ... monthly aggregated data
  ],
  papers: [
    {title:"...", authors:"...", conference:"...", summary:"...", url:"..."},
    // ... all papers from favorites.json papers
  ],
  techNews: [
    {date:"YYYY-MM-DD", title:"...", category:"...", importance:N_or_string, summary:"..."},
    // ... all news from favorites.json techNews
  ]
};
```

## Chart Specifications

### (a) Consumer AI Radar
- Type: radar (filled)
- Labels: ['AI深度', '用户体验', '部署规模', '技术壁垒', '商业化']
- One dataset per brand (limit to ~15 brands)
- Color palette: 15 distinct colors

### (b) AI Model Comparison
- Left: Radar chart (6 dimensions: 推理/编程/多模态/价格竞争力/上下文长度/生态)
- Right: Bar chart (API pricing: input + output per model, $/1M tokens)

### (c) Stock Market Line (Dual Y-axis)
- Left Y-axis: 上证综指 (red, #e74c3c)
- Right Y-axis: 纳斯达克 + 恒生科技 (blue + green)
- Fill area under lines, circle markers, tension 0.3

### (d) Semiconductor Bar
- Horizontal bar chart
- 8 key metrics with distinct colors
- Labels include units

### (e) Papers Table
- Sortable by clicking column headers
- Columns: 论文标题, 作者, 会议, 摘要, 链接
- Links to arXiv

### (f) Four-Question Analysis
- Expandable/collapsible cards
- Each card: title + Q1/Q2/Q3 text + Q4 table (角色/建议)
- Click header to toggle

### (g) Tech News Timeline
- CSS-based vertical timeline
- Color-coded dots: red (high), gold (medium), gray (low)
- Tags for category and importance
- Sorted by date

## Responsive Breakpoints

```css
@media(max-width:768px) {
  .grid-2, .grid-3 { grid-template-columns: 1fr }
  .stats-bar { gap: 20px }
}
@media(max-width:520px) {
  .container { padding: 10px }
  .card { padding: 16px }
}
```

## Data Sync Rules

- All chart data comes from the inline DATA object
- DATA object must match favorites.json content
- When updating, regenerate the entire HTML file to ensure consistency
- Stats bar total count must match sum of all categories in meta.totalItems

## Key Implementation Notes

- Chart.js v4+ CDN: `https://cdn.jsdelivr.net/npm/chart.js`
- Chart defaults: `Chart.defaults.color = '#e0e0e0'`, `Chart.defaults.borderColor = 'rgba(255,255,255,0.08)'`
- Radar chart series colors: use `graphicalProperties.solidFill` and `graphicalProperties.line.solidFill`
- Timeline items: use CSS `::before` pseudo-element for dots, `::before` on parent for vertical line
- Expandable cards: use CSS `max-height: 0` + `overflow: hidden` + `.open .expand-body { max-height: 3000px }`
