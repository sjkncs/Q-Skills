# Exam Cheat Sheet Generator - Reference

## PPT Content Extraction Methods

### From PDF courseware
```python
import pdfplumber
with pdfplumber.open("courseware.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

### From DOCX answer files
```python
import docx
doc = docx.Document("answers.docx")
# Parse by heading structure
headings = [(i, p.style.name, p.text) for i, p in enumerate(doc.paragraphs) if 'Heading' in p.style.name]
# Extract sections between headings
```

## Formula Categories (Common in ML/AI Courses)

1. **Architecture**: PE, Self-Attention, Multi-Head, FFN, Residual, RMSNorm, SwiGLU, RoPE
2. **Training**: Loss functions, Mixed precision (16Φ), ZeRO, Gradient accumulation
3. **Fine-tuning**: LoRA (W+BA), AdaLoRA, QLoRA, ALiBi
4. **RL**: Policy gradient, GAE, PPO-Clip/Penalty, Reward model, Importance sampling
5. **Evaluation**: P/R/F1, BLEU, ROUGE-N/L, PPL, McNemar, Kappa, MSLE/MedAE

## Knowledge Map Structure Pattern

```python
chapters = [
    ("第N章 章名", [
        ("N.M 节名", [
            "概念1: 简短描述(关键数值)",
            "概念2: 公式或对比",
            ...
        ]),
    ]),
]
```

Each section should have 4-8 bullet points. Include numerical values inline (e.g., "LoRA: ΔW=BA, 350GB→35MB").

## CSS Multi-Column Layout Notes

- `column-count` + fixed `height` forces content to fill columns evenly
- `column-rule` adds visual separator between columns
- `column-span: all` on h1 breaks column flow (use sparingly)
- `break-inside: avoid` on small blocks (h2, .sec) but NOT on large containers (.ch)
- `overflow: hidden` on .page prevents content spilling to page 3

## Chrome Headless PDF Tips

- `--virtual-time-budget=15000` gives KaTeX 15s to render all formulas
- `--print-to-pdf-no-header` removes Chrome's default header/footer
- `--run-all-compositor-stages-before-draw` ensures all CSS is applied
- For Windows: use `file:///C:/path/to/file.html` URL format
- Output PDF page size matches CSS `@page { size: ... }`

## Common Pitfalls

1. **LaTeX in HTML**: Must escape `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;` inside LaTeX strings
2. **f-string backslashes**: Cannot use `\` in Python f-string expressions; write LaTeX to file instead
3. **python-pptx slide reorder**: Use `prs._element` (not `prs.presentation._element`) for XML access
4. **AF_UNIX on Windows**: `socket.AF_UNIX` doesn't exist on Windows; skip thumbnail generation
5. **Chinese encoding in PDF**: Chrome handles UTF-8 natively, but console output may show garbled text
