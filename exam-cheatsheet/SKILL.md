---
name: exam-cheatsheet
description: Generate comprehensive 2-page A4 exam cheat sheets from course materials (PPT/PDF/DOCX). Combines formulas (LaTeX via KaTeX), numerical values, knowledge maps, calculation problems, essay templates, and Q&A into a dense multi-column HTML, then converts to PDF via Chrome headless. Use when the user wants a cheat sheet, exam reference, quick-lookup sheet, or study guide from course materials.
---

# Exam Cheat Sheet Generator

Generate dense, 2-page A4 cheat sheets from course materials (PPT courseware PDFs, answer DOCX files, existing cheat sheets). Output is a LaTeX-rendered HTML converted to pixel-perfect PDF.

## Workflow

```
Task Progress:
- [ ] Step 1: Extract content from all source materials
- [ ] Step 2: Gap analysis - identify missing items
- [ ] Step 3: Build HTML with KaTeX LaTeX formulas
- [ ] Step 4: Convert HTML to PDF via Chrome headless
- [ ] Step 5: Verify exactly 2 A4 pages
- [ ] Step 6: Present PDF to user
```

### Step 1: Extract Content

Extract from ALL source files in parallel:

- **PPT courseware PDF**: Use `pdfplumber` for text, formulas, numerical values
- **Answer DOCX**: Use `python-docx` to parse MCQ/fill-blank/definition/short-answer/application/calculation/essay sections
- **Existing cheat sheets**: Compare against new extraction to avoid duplication

```python
import docx
doc = docx.Document("source.docx")
paras = [(p.style.name, p.text.strip()) for p in doc.paragraphs]
tables = [[[c.text.strip() for c in r.cells] for r in tb.rows] for tb in doc.tables]
```

### Step 2: Gap Analysis

Delegate to a subagent (Task tool) for thorough comparison:

- Compare PPT content vs existing extractions
- Identify missing: formulas, numerical values, concepts, comparisons, code snippets
- Prioritize by exam relevance (specific numbers, named formulas, comparison tables)

### Step 3: Build HTML

Use the generator pattern from `gen_v7.py`. Key structure:

**Page 1 (6-column layout)** - Answers + Formulas + Values:
- A. Formula collection (43+ core formulas in LaTeX)
- B. Key numerical values (34+ entries)
- C. Comparison tables (from DOCX)
- D. Essay templates (论述万能结构 + 对比题)
- E. Pre-exam quick recall (考前速记)
- F-L. MCQ answers, fill-blank, definitions, short-answer, application, calculations

**Page 2 (5-column layout)** - Knowledge mind map:
- Full chapter/section/subsection tree
- Each subsection has key concepts with numerical values embedded
- Color coding: blue=chapter header, red=section border

### Step 4: HTML→PDF Conversion

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" \
  --headless=new --disable-gpu --no-sandbox \
  --run-all-compositor-stages-before-draw \
  --print-to-pdf-no-header \
  --print-to-pdf="output.pdf" \
  --virtual-time-budget=15000 \
  "file:///path/to/input.html"
```

### Step 5: Verify

```python
from PyPDF2 import PdfReader
reader = PdfReader("output.pdf")
assert len(reader.pages) == 2  # Must be exactly 2 pages
```

## Critical CSS Layout Settings

```css
@page { size: A4 portrait; margin: 2mm 2mm 2mm 2mm; }
html,body { font-size: 3.8pt; line-height: 1.18; }
.page { width: 206mm; height: 294mm; overflow: hidden; }
.cols6 { column-count: 6; column-gap: 1.6mm; height: 292mm; }  /* Page 1 */
.cols5 { column-count: 5; column-gap: 2mm; height: 292mm; }    /* Page 2 */
.katex { font-size: 0.74em !important; }
```

**Key rules**:
- NEVER use `break-inside: avoid` on chapter containers (`.ch`) - it blocks cross-column flow and causes massive white space
- Use `break-inside: avoid` only on `h2` headers and small `.sec` blocks
- Font size sweet spot: 3.3-3.8pt body, 0.68-0.74em KaTeX
- `overflow: hidden` on `.page` to enforce strict 2-page limit

## KaTeX Formula Rendering

Load from CDN, render on page load:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {
    delimiters: [{left: '\\(', right: '\\)', display: false}],
    throwOnError: false, fontSize: '0.74em'
  });"></script>
```

Use inline LaTeX delimiters `\( ... \)` for all formulas. HTML entities (`&lt;`, `&gt;`, `&amp;`) must be used inside LaTeX for `<`, `>`, `&`.

## Content Sections Template

### Calculation Problems (计算题)
12 problems with step-by-step solutions covering:
- Mixed precision memory (16Φ formula)
- ZeRO memory reduction ratios
- LoRA parameter savings
- Distributed training communication volume
- ROUGE/BLEU/McNemar/PPL calculations
- Data pipeline statistics

### Essay Templates (论述题万能结构)
4 universal structures:
1. **技术流程类**: 目标→数据→模块→过程→优势/风险
2. **对比类**: 定义→对象/输入/过程/优点/缺点/场景 六维对比
3. **系统设计类**: 流程画→输入→预处理→核心→输出→评估
4. **风险分析类**: 数据/模型/推理/安全/评估 五维度

### Knowledge Mind Map
Full chapter tree with embedded values. Format:
```
Chapter > Section > "concept1 · concept2(数值) · concept3"
```

## Filling A4 Pages - Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Page 2 left side only | `break-inside:avoid` on `.ch` | Remove it from chapter containers |
| Too much white space | Font too small | Increase to 3.5-3.8pt |
| Content overflows to page 3 | Too much content | Reduce font or cut lower-priority items |
| Content not filling columns | Sparse knowledge map | Add more detail per section |

## Dependencies

```
pip install python-docx pdfplumber PyPDF2
```

Chrome/Chromium must be installed for PDF generation.

## Reference Generator

See `gen_v7.py` in the workspace for the complete working implementation with all sections, formulas, numerical values, and knowledge map for the embodied LLM theory course.
