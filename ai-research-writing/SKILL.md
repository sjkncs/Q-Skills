---
name: ai-research-writing
description: Comprehensive AI-assisted academic paper writing workflow. Covers structure drafting, translation, polishing, de-AI cleanup, logic checking, experimental analysis, figure and table captions, reviewer simulation, and domain adaptation. Use when writing, editing, translating, or reviewing academic papers for conferences or journals. Supports both LaTeX and Word workflows. Source repo is yunyunfanfan/awesome-ai-research-writing.
description_zh: "AI辅助学术论文写作全流程，涵盖结构起草、中英翻译、润色、去AI味、逻辑检查、实验分析、图表标题、审稿模拟等"
version: 2.0.0
---

# AI-Assisted Research Paper Writing

Based on awesome-ai-research-writing — curated prompts and workflows from MSRA, Seed, SH AI Lab researchers and PKD/USTC/SJTU students.

## Core Principle

1. Structure first, then paragraphs
2. Logic first, then polish
3. Academic correctness first, then de-AI
4. Main text first, then figures and Related Work

## Recommended Workflow

### Step 0: Prepare Input Materials
Gather: research repo/code, README, experiment logs, result tables, key figures, target conference, one-sentence contribution summary, existing drafts or bullet points.

### Step 1: Draft or Scaffold
- Use 20-ml-paper-writing skill for LaTeX template + section skeleton
- Use doc-coauthoring skill for iterative section-by-section drafting

### Step 2: Write Sections (Abstract then Introduction then Method then Experiments then Related Work then Limitations)
- LaTeX English: Use CN to EN LaTeX prompt to translate Chinese drafts
- Word Chinese: Use CN to CN Word prompt to restructure fragments
- Word English: Use CN to EN Word prompt for direct Word-ready output

### Step 3: Section-Level Iteration
- Structure still messy: doc-coauthoring
- Paragraph too verbose: Abbreviate prompt
- Paragraph too thin: Expand prompt
- Grammar/tone needs polish: Polish (EN) or Polish (CN) prompt

### Step 4: Citations, Tables, Figures
- Find citations / write Related Work: 20-ml-paper-writing skill
- Experimental analysis text: Experimental Analysis prompt
- Chart type recommendation: Chart Recommendation prompt
- Figure/table captions: Figure Caption / Table Caption prompts
- Architecture diagrams: canvas-design skill + Architecture Diagram prompt

### Step 5: Logic Consistency Check
- Section-level quick check: Logic Check prompt
- Full-paper reviewer simulation: Reviewer Perspective prompt

### Step 6: De-AI and Final Cleanup
- First pass: De-AI (LaTeX EN) or De-AI (Word CN) prompt
- Second pass: humanizer skill for style correction
- Focus areas: Abstract, Introduction first 2 paragraphs, Contribution, Conclusion, captions

### Step 7: Pre-Submission Checklist
- Verify: correct template, page limit, anonymization, Broader Impact/Limitations/Checklist, figure captions, citations, appendix
- Word submissions: use docx skill to map content to template

## Prompt Library

### CN to EN (LaTeX)

Role: You are both a top scientific writing expert and a senior conference reviewer (ICML/ICLR). Your academic taste is impeccable.

Task: Process the provided Chinese draft into English academic LaTeX.

Constraints:
1. Visual: No bold/italic/quotes. Keep LaTeX source clean.
2. Style: Rigorous logic, precise words, concise expression. Use common words. No dashes. No item lists, use coherent paragraphs. Remove AI feel.
3. Tense: Present tense for methods/results. Past tense only for specific historical events.
4. Output Part 1 [LaTeX]: Full English. Escape special chars (95 percent becomes 95\%, model_v1 becomes model\_v1, R&D becomes R\&D). Preserve math. Part 2 [Translation]: Chinese literal translation for verification. Nothing else.

### EN to CN (LaTeX)

Role: Senior CS academic translator.

Task: Translate English LaTeX into fluent Chinese text.

Constraints:
1. Remove cite, ref, label commands. Extract text from textbf, emph. Convert math to natural language.
2. Direct translation, no polishing, no restructuring. Keep sentence order consistent with English.
3. Output: Pure Chinese text only. No LaTeX code.

### CN to EN (Word)

Role: Top scientific writing expert + senior conference reviewer.

Task: Translate Chinese draft into English academic text for Word.

Constraints:
1. No Markdown at all. Pure text for direct Word paste.
2. Same style rules as LaTeX version. No dashes, no bullet points, no AI feel.
3. Use standard text symbols (95%, model_v1, R&D). Preserve $ for math.
4. Output: Part 1 [English Draft] + Part 2 [Chinese Translation]. Nothing else.

### CN to CN (Word) — Chinese paper restructuring

Role: Senior Chinese academic journal editor.

Task: Rewrite Chinese draft with colloquialisms/jumps into formal academic paragraphs.

Constraints:
1. Pure text output. Chinese full-width punctuation.
2. Logic reorganization. One paragraph = one core point.
3. Extremely formal. Objective tone. Keep standard English terms (Transformer, CNN, Few-shot).
4. Output: Part 1 [Refined Text] + Part 2 [Logic Flow explanation].

### Abbreviate

Role: Academic editor focused on conciseness.

Task: Slightly reduce English LaTeX by approximately 5-15 words.

Constraints:
1. Preserve all core info, technical details, parameters.
2. Techniques: clause to phrase, passive to active, remove fillers.
3. No bold/italic/quotes. No dashes. No lists. Coherent paragraphs.
4. Output: Part 1 [LaTeX] + Part 2 [Translation] + Part 3 [Modification Log].

### Expand

Role: Academic editor focused on logical depth.

Task: Slightly expand English LaTeX by approximately 5-15 words.

Constraints:
1. No filler. Dig deeper: make implicit conclusions explicit, add logical connectors.
2. Upgrade simple descriptions to more precise academic expressions.
3. Same formatting rules as Abbreviate.
4. Output: Part 1 [LaTeX] + Part 2 [Translation] + Part 3 [Modification Log].

### Polish (English LaTeX)

Role: Senior CS academic editor for NeurIPS/ICLR/ICML.

Task: Deep polish English LaTeX to zero-error publication standard.

Constraints:
1. Fix sentence structure for top-venue norms. Optimize long sentences. Eliminate non-native stiffness.
2. Formal academic register. No contractions (it is, not it's). Simple and clear vocabulary. Avoid noun possessives (use the performance of METHOD not METHOD's performance).
3. Keep abbreviations (LLM stays LLM). Preserve LaTeX commands. Preserve existing formatting but add NO new formatting.
4. No lists, coherent paragraphs only.
5. Output: Part 1 [LaTeX] + Part 2 [Translation, no English in parentheses] + Part 3 [Modification Log].

### Polish (Chinese Word)

Role: Senior Chinese CS academic editor.

Task: Review and polish Chinese paper paragraph. Only fix real problems.

Constraints:
1. Threshold: Only fix colloquialisms, grammar errors, logic gaps, or overly Europeanized sentences. If already good, preserve as-is.
2. Modern academic register. No archaic officialese. Remove colloquial expressions.
3. Pure text. Chinese full-width punctuation.
4. Output: Part 1 [Refined Text or original if no changes needed] + Part 2 [Review Comments].

### Logic Check

Role: Final-proof academic assistant. Red-line review only.

Task: Check English LaTeX for fatal errors only.

Constraints:
1. Assume high-quality draft. Only flag: contradictory statements, unexplained term changes, severe grammar/Chinglish.
2. Skip nice-to-have improvements.
3. Output: If clean, output detection passed. If issues, brief Chinese bullet points.

### De-AI (LaTeX English)

Role: Senior CS academic editor. Remove AI writing artifacts.

Task: Rewrite English LaTeX to sound like a native researcher.

Constraints:
1. Replace overused AI words: leverage becomes use, delve into becomes investigate, tapestry becomes context, etc.
2. Remove mechanical connectors (First and foremost, It is worth noting). Connect via logic, not transition words.
3. Minimize dashes. No bold/italic emphasis.
4. If already natural, preserve original. Output: Part 1 [LaTeX] + Part 2 [Translation] + Part 3 [Modification Log or detection passed].

Common AI-flavored words to flag: Accentuate, Ameliorate, Amplify, Alleviate, Ascertain, Bolster, Culminate, Decipher, Delve, Elucidate, Endeavor, Envision, Foster, Galvanize, Harmonize, Intricate, Leverage, Manifest, Nuanced, Obscure, Perpetuate, Pivotal, Profound, Scrutinize, Substantiate, Tailor, Transcend, Traverse, Underscore, Unveil, Vibrant.

### De-AI (Word Chinese)

Role: Senior Chinese CS academic editor. Remove machine/translation artifacts.

Task: Rewrite Chinese text to sound rigorous, objective, and natural.

Constraints:
1. Replace empty rhetorical expressions with concrete academic descriptions.
2. Eliminate long attributives. Limit passive voice. Avoid mechanical enumeration patterns.
3. No Markdown. Pure text for Word.
4. If already good, preserve. Output: Part 1 [Text] + Part 2 [Modification Log].

### Architecture Diagram (for image generation)

You are a world-class scientific illustrator for CVPR/NeurIPS/ICLR.

Generate a professional academic architecture diagram based on the provided abstract and methodology.

Visual Style:
1. Flat vector, clean lines, academic aesthetic (DeepMind/OpenAI style)
2. Organized flow (L to R or T to B). Group related components logically.
3. Professional pastel tones. White background.
4. Include legible English text labels for key modules/equations.
5. NO photos, NO sketches, NO unreadable text, NO 3D artifacts.

### Experimental Analysis

Role: Senior data scientist with sharp insight.

Task: Analyze experimental data and write LaTeX analysis paragraphs.

Constraints:
1. All conclusions strictly from input data. No fabrication.
2. Focus on comparison, trends, sensitivity, trade-offs. Not just reporting numbers.
3. Use paragraph with core finding heading + analysis text. No bold/italic. No lists.
4. Output: Part 1 [LaTeX] + Part 2 [Translation].

### Figure Caption

Role: Experienced academic editor for figure captions.

Task: Convert Chinese description into English figure caption.

Constraints:
1. Noun phrase uses Title Case. Full sentence uses Sentence case with period.
2. Remove The figure shows prefix, start directly with content.
3. No Figure 1: prefix. Escape special chars. Preserve math.

### Table Caption

Role: Experienced academic editor for table captions.

Task: Convert Chinese description into English table caption.

Constraints:
1. Same case rules as figure captions.
2. Use standard expressions: Comparison with, Ablation study on, Results on.
3. No Table 1: prefix.

### Reviewer Perspective (Full Paper)

Role: Senior, rigorous academic reviewer for top CS venues.

Task: Deep review of uploaded PDF paper for target venue.

Constraints:
1. Objective assessment. Distinguish fatal flaws from fixable issues.
2. Review dimensions: community contribution, rigor (experimental support, fair baselines, ablations), consistency (claims vs. evidence).
3. Output Part 1 [Review Report]: Summary (1 sentence), Strengths (1-3), Weaknesses (specific), Rating (1-10). Part 2 [Strategic Advice]: Root causes, fixability judgment, action items.

### Chart Type Recommendation

Role: Senior data visualization expert for Nature/Science/NeurIPS.

Task: Recommend 1-2 best chart types for experimental data.

Standard Academic Chart Library:
- Value/Performance: vertical grouped bar, horizontal bar, Pareto front, radar, stacked bar
- Trend/Convergence: line with confidence band, zoomed-in line, scatter fit
- Classification: ROC curve, PR curve
- Relationships: heatmap, scatter, bubble
- Distribution: violin, box, donut/pie
- Composite: dual Y-axis, bar-line combo, facet grid

Output:
1. Recommended chart + name
2. Core reasoning
3. Visual design: axes, scale handling, statistical elements, color strategy

## Domain Adaptation Methodology

When adapting a conference paper to a specific domain (e.g., quantitative finance, biomedical, robotics):

1. Extract Core Mechanism: Identify the paper's key algorithmic/structural innovation
2. Map to Domain Problem: Find the analogous problem in the target domain
3. Domain-Specific Constraints: Add realistic constraints (e.g., for finance: liquidity, transaction costs, regulation, non-stationarity)
4. Domain Datasets: Replace generic benchmarks with domain-specific ones (e.g., S&P 500, options chains)
5. Domain Metrics: Use domain-appropriate evaluation (e.g., Sharpe ratio, MaxDD, Calmar ratio for finance)
6. Paper Structure: Follow standard format with Abstract (bilingual), Introduction, Method, Experiments, Discussion, Conclusion

## Model Recommendations

For creative writing and paper drafting: Gemini-3-pro/flash
For experimental code: Claude-4.5 series + Cursor Composer
For de-AI cleanup: Combine prompt-based approach + humanizer skill

## Quick Decision Guide

- Write entire paper from repo: 20-ml-paper-writing skill
- Iterate on one section: doc-coauthoring skill
- Translate/polish one paragraph: Prompt library above
- Make/modify figures: canvas-design skill + diagram prompts
- Final de-AI pass: De-AI prompts + humanizer skill
