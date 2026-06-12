# Excel Generation Template (openpyxl)

## Quick Reference

Use this Python template to regenerate `favorites.xlsx` with charts, conditional formatting, and formulas.

## Complete Script

```python
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import RadarChart, BarChart, LineChart, Reference
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.utils import get_column_letter
from copy import copy

with open(r'D:\MyDevFavorites\favorites.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

wb = Workbook()

# ===== Styles =====
header_font = Font(bold=True, color='FFFFFF', size=11)
header_fill = PatternFill('solid', fgColor='1F4E78')
title_font = Font(bold=True, size=16, color='1F4E78')
subtitle_font = Font(bold=True, size=12, color='1F4E78')
thin_border = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC')
)
center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)

# ===== Sheet 1: 概览 =====
ws = wb.active
ws.title = '概览'
ws['A1'] = '我的开发收藏夹 - 数据概览'
ws['A1'].font = title_font
ws.merge_cells('A1:D1')

# Stats from meta
meta = data['meta']
overview = [
    ['标题', meta['title']],
    ['最后更新', meta['lastUpdated']],
    ['版本', meta['version']],
    ['仓库', meta['repository']],
]
for i, (k, v) in enumerate(overview, start=3):
    ws[f'A{i}'] = k; ws[f'A{i}'].font = subtitle_font
    ws[f'B{i}'] = v

# Count table with SUM formula
stats_headers = ['分类', '条目数']
stats_rows = [
    ['Tips', meta['totalItems']['tips']],
    ['Repos', meta['totalItems']['repos']],
    ['Consumer AI', meta['totalItems']['consumerAI']],
    ['AI Models', meta['totalItems']['aiModels']],
    ['Tech News', meta['totalItems']['techNews']],
    ['Stock Market', meta['totalItems']['stockMarket']],
    ['Papers', meta['totalItems']['papers']],
]
# Write headers + data with borders
# ... (standard pattern: header_font/fill for row N, data for N+1 to N+len)
# Total row: ws.cell(row=total_row, column=2, value='=SUM(B{start}:B{end})')

# ===== Sheet 2: 消费品牌AI =====
# Headers: 品牌, 工具, 类别, AI深度, 用户体验, 部署规模, 技术壁垒, 商业化
# Data from data['consumerAI']
# Conditional formatting for score columns (D-H):
#   ColorScaleRule(start=0/red, mid=5/yellow, end=10/green)
# Average row with AVERAGE formula
# RadarChart: create helper data block, add_data with titles_from_data=True

# ===== Sheet 3: AI大模型 =====
# Headers: 模型, 厂商, 推理, 编程, 多模态, 价格竞争力, 上下文, 生态, 输入价格, 输出价格
# RadarChart (top 6 models) + BarChart (API pricing)
# Conditional formatting for score columns

# ===== Sheet 4: 股市趋势 =====
# Aggregate monthly data from raw stockMarket records:
monthly = {}
for s in data['stockMarket']:
    month = s['date'][:7]
    market = s['market']
    val = s.get('value', 0)
    if month not in monthly:
        monthly[month] = {}
    if '上证' in s.get('index', ''):
        monthly[month]['a'] = val
    elif '纳斯达克' in s.get('index', ''):
        monthly[month]['us'] = val
    elif '恒生科技' in s.get('index', ''):
        monthly[month]['hk'] = val

# LineChart with 3 series (上证/纳斯达克/恒生科技)
# Style: colors = ['E74C3C', '3498DB', '2ECC71'], line width 30000 EMU, circle markers

# ===== Sheet 5: 半导体指标 =====
# Hard-coded key metrics table + horizontal BarChart

# ===== Sheet 6: 顶会论文 =====
# Table with conditional formatting on award column:
#   CellIsRule for "最佳论文" → gold fill
#   CellIsRule for "杰出论文" → silver fill

# ===== Sheet 7: 科技新闻 =====
# Filter recent news (current month), write table

wb.save(r'D:\MyDevFavorites\favorites.xlsx')
```

## Key Patterns

### RadarChart Setup
```python
radar = RadarChart()
radar.type = 'filled'
radar.style = 10
radar.title = '消费品牌 AI 能力雷达图'
radar.y_axis.delete = True
radar.width = 24
radar.height = 16

# Data block: row 1 = dimensions, col 1 = brand names
data_ref = Reference(ws, min_col=2, min_row=start, max_col=6, max_row=end)
cats_ref = Reference(ws, min_col=2, min_row=start, max_col=6, max_row=start)
radar.add_data(data_ref, titles_from_data=True)
radar.set_categories(cats_ref)

# Color series
palette = ['E74C3C', '3498DB', '2ECC71', '9B59B6', 'E67E22', '1ABC9C']
for idx, series in enumerate(radar.series):
    series.graphicalProperties.solidFill = palette[idx % len(palette)]
    series.graphicalProperties.line.solidFill = palette[idx % len(palette)]

ws.add_chart(radar, 'A{position}')
```

### Conditional Formatting (Color Scale)
```python
for col in range(4, 9):
    col_letter = get_column_letter(col)
    range_str = f'{col_letter}4:{col_letter}{3 + count}'
    ws.conditional_formatting.add(range_str,
        ColorScaleRule(
            start_type='num', start_value=0, start_color='F8696B',
            mid_type='num', mid_value=5, mid_color='FFEB84',
            end_type='num', end_value=10, end_color='63BE7B'
        ))
```

### Formula Pattern
```python
# AVERAGE formula
ws.cell(row=avg_row, column=col, value=f'=AVERAGE({col_letter}4:{col_letter}{avg_row-1})')

# SUM formula
ws.cell(row=total_row, column=2, value=f'=SUM(B{start}:B{end})')
```

### LineChart with Styled Series
```python
line = LineChart()
line.style = 10
line.title = '三大股指月度趋势'
line.width = 24
line.height = 16

data_ref = Reference(ws, min_col=2, min_row=3, max_col=4, max_row=end)
cats_ref = Reference(ws, min_col=1, min_row=4, max_row=end)
line.add_data(data_ref, titles_from_data=True)
line.set_categories(cats_ref)

colors = ['E74C3C', '3498DB', '2ECC71']
for idx, series in enumerate(line.series):
    series.graphicalProperties.line.solidFill = colors[idx]
    series.graphicalProperties.line.width = 30000
    series.marker.symbol = 'circle'
    series.marker.size = 7
    series.marker.graphicalProperties.solidFill = colors[idx]
```

## Important Notes

- Stock market data in favorites.json uses individual records per index per month. Aggregate by month before writing to Excel.
- openpyxl RadarChart requires data in a helper block (not inline references).
- Conditional formatting ranges must match actual data row count.
- Always use formulas (SUM, AVERAGE) instead of Python-computed values.
- On Windows, recalc.py may fail due to AF_UNIX not being available. Excel will recalculate formulas when opened.
