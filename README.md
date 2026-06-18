# Q-Skills

QoderWork Skills Collection — **203** agent skills with bilingual descriptions (EN/CN).

All skills include `description_zh` fields in their SKILL.md frontmatter for Chinese-language display in QoderWork.

## Skills by Category / 按类别分类

### AI/ML Engineering | AI/机器学习工程 (7)

| Skill | 中文描述 |
|---|---|
| `get-available-resources` | 在执行计算密集型科学任务前检测可用计算资源（CPU/GPU/内存/磁盘） |
| `image-enhancer` | 改善图像质量（尤其是截图），增强分辨率、清晰度和可读性 |
| `pufferlib` | 高性能强化学习框架，针对速度和规模优化，适用于大规模RL训练 |
| `pytorch-lightning` | PyTorch Lightning深度学习框架，组织PyTorch代码为LightningModule和Trainer |
| `stable-baselines3` | 生产级强化学习算法（PPO/SAC/DQN/TD3/DDPG/A2C），配合scikit-learn接口 |
| `torch-geometric` | PyTorch Geometric（PyG）图神经网络——节点/边/图分类、消息传递和图Transformer |
| `transformers` | Hugging Face Transformers，用于加载Hub模型、流水线推理、文本生成和Trainer微调 |

### Bioinformatics & Life Sciences | 生物信息与生命科学 (58)

| Skill | 中文描述 |
|---|---|
| `anndata` | 单细胞分析中的标注矩阵数据结构，用于处理.h5ad文件和AnnData对象操作 |
| `arboreto` | 从基因表达数据推断基因调控网络（GRN），使用GRNBoost2和RF-MDS等可扩展算法 |
| `benchling-integration` | Benchling Python SDK和REST API集成，管理注册实体、库存、ELN条目、工作流和分子序列 |
| `bgpt-paper-search` | 搜索科学论文并从全文研究中提取结构化实验数据，支持BioGPT驱动的文献检索 |
| `bids` | 脑成像数据结构（BIDS）格式规范，用于组织和描述神经影像学数据集 |
| `biopython` | 综合分子生物学工具包，用于序列操作、文件解析（FASTA/GenBank/PDB）、BLAST搜索和系统发育分析 |
| `bioservices` | 统一的Python接口访问40+生物信息学服务，支持UniProt、KEGG、NCBI等多数据库联合查询 |
| `bulk-rnaseq` | 端到端bulk RNA-seq分析流程，从原始FASTQ读段经QC、修剪、比对到差异表达分析 |
| `cellxgene-census` | 程序化查询CZ CELLxGENE Census，获取版本化的公共单细胞和空间转录组数据集 |
| `cobrapy` | 约束型代谢建模（COBRA），支持FBA、FVA、基因敲除、通量采样和SBML模型操作 |
| `datamol` | RDKit的Python封装，提供简化接口和合理默认值，适用于标准化分子操作和化学信息学流水线 |
| `deepchem` | 分子机器学习工具，包含多种分子特征化器和预构建数据集，用于性质预测（ADMET/毒性/溶解度） |
| `depmap` | 查询癌症依赖图谱（DepMap），获取癌细胞系基因依赖评分（CRISPR Chronos和RNAi） |
| `diffdock` | DiffDock分子对接工具，用于蛋白质-小分子复合物构象预测（从PDB或UniProt ID出发） |
| `dnanexus-integration` | DNAnexus云基因组学平台，构建应用/小程序、管理数据（上传/下载）、使用dxpy Python SDK |
| `esm` | ESM Python SDK，用于ESM3/ESMC模型推理、Forge/Biohub推理API和蛋白质结构预测 |
| `flowio` | 解析FCS（流式细胞术标准）文件v2.0-3.1，提取事件为NumPy数组并读取元数据 |
| `general-ppt` | 处理.pptx文件的通用技能，包括创建、编辑、分析和转换PowerPoint演示文稿 |
| `generate-image` | 使用AI模型（FLUX、Nano Banana 2）生成或编辑图像，适用于通用图像生成任务 |
| `geniml` | 基因组区间数据（BED文件）机器学习工具，用于训练和评估基因组ML模型 |
| `gget` | 快速CLI/Python查询20+生物信息学数据库，支持基因信息、BLAST/BLAT等快速检索 |
| `ginkgo-cloud-lab` | 在Ginkgo Bioworks云实验室提交和管理实验方案，提供基于Web的自动化实验接口 |
| `glycoengineering` | 分析和工程化蛋白质糖基化，扫描序列中的N-糖基化位点并预测糖型 |
| `gtars` | 高性能基因组区间分析工具包（Rust+Python），用于大规模基因组区间操作 |
| `histolab` | 轻量级WSI切片提取和预处理，用于基础病理切片处理和组织检测 |
| `hypothesis-generation` | 从观察结果中结构化地生成假设，适用于有实验观察需要形成可测试假设的场景 |
| `labarchive-integration` | 电子实验室笔记本API集成，访问笔记本、管理条目/附件、备份笔记本数据 |
| `lamindb` | 开源血统原生数据湖仓，用于生物数据集和ML实验的版本化管理 |
| `latchbio-integration` | Latch生物信息学工作流平台，使用Latch SDK和@workflow/@task装饰器构建流水线 |
| `matchms` | 代谢组学中的光谱相似性和化合物识别工具，用于比较质谱和计算分子相似度 |
| `medchem` | 药物化学过滤器，用于化合物筛选（Lipinski/Veber/CNS规则）、骨架分析和ADMET评估 |
| `molecular-dynamics` | 使用OpenMM和MDAnalysis运行和分析分子动力学模拟，设置蛋白质/小分子体系 |
| `molfeat` | 分子特征化工具（100+特征化器），包括ECFP、MACCS、描述符和预训练模型 |
| `neurokit2` | 综合生物信号处理工具包，分析ECG、EEG、EDA、PPG等生理数据 |
| `neuropixels-analysis` | 使用SpikeInterface端到端分析Neuropixels胞外记录，覆盖SpikeGLX数据加载到sorting |
| `omero-integration` | 显微数据管理平台，通过Python访问图像、检索数据集、分析像素和管理元数据 |
| `opentrons-integration` | Opentrons官方协议API，用于OT-2和Flex液体处理机器人的协议编写 |
| `pathml` | 全功能计算病理学工具包，用于高级WSI分析（多重免疫荧光、空间转录组） |
| `pathway-enrichment` | 对基因列表或排序基因数据运行通路和基因集富集分析，并解读结果 |
| `phylogenetics` | 使用MAFFT（多序列比对）和IQ-TREE 2（最大似然法）构建和分析系统发育树 |
| `polars-bio` | 基于Polars DataFrame的高性能基因组区间操作和生物信息学文件I/O |
| `primekg` | 查询精准医学知识图谱（PrimeKG），获取基因-疾病-药物-通路等多尺度生物数据 |
| `protocolsio-integration` | protocols.io API集成，管理和搜索科学实验方案 |
| `pydeseq2` | 使用PyDESeq2进行bulk RNA-seq差异基因表达分析，支持公式化设计和Wald/LRT检验 |
| `pyhealth` | 使用PyHealth构建临床/医疗深度学习流水线，加载EHR/信号/影像数据集 |
| `pyopenms` | 完整质谱分析平台，用于蛋白质组学和代谢组学（特征检测、鉴定、定量） |
| `pysam` | 基因组文件工具包，读写SAM/BAM/CRAM比对、VCF/BCF变异和FASTA/FASTQ序列 |
| `pytdc` | 治疗数据公共库（TDC），提供AI药物发现数据集（ADME/毒性/DTI）和基准评测 |
| `rdkit` | 化学信息学工具包，支持精细分子控制——SMILES/SDF解析、描述符计算和子结构搜索 |
| `rowan` | Rowan云原生分子建模和药物化学工作流平台，提供Python API |
| `scanpy` | 标准单细胞RNA-seq分析流水线，用于QC、归一化、降维、聚类和差异表达分析 |
| `scientific-schematics` | 使用Nano Banana 2 AI创建出版质量的科学示意图，支持智能迭代优化 |
| `scikit-bio` | 生物数据工具包，涵盖序列分析、比对、系统发育树和多样性度量（alpha/beta） |
| `scvelo` | 使用scVelo进行RNA速度分析，从未剪接/剪接mRNA动态估计细胞状态转换 |
| `scvi-tools` | 单细胞组学的深度生成模型，用于概率批次校正（scVI）和细胞类型注释 |
| `tailored-resume-generator` | 分析职位描述并生成定制简历，突出相关经验和技能匹配 |
| `tiledbvcf` | 使用TileDB高效存储和检索基因组变异数据，支持可扩展VCF/BCF摄取 |
| `torchdrug` | PyTorch原生分子和蛋白质图神经网络，用于构建自定义GNN架构 |

### Data Analysis & Visualization | 数据分析与可视化 (24)

| Skill | 中文描述 |
|---|---|
| `analytics-data-analysis` | 数据分析与可视化最佳实践，使用Python/Jupyter进行统计分析和交互式可视化 |
| `community-survey-analysis` | 社区调研分析，将原始访谈转写文本（含图片）结构化为专业列表，支持编码分析、多维含量分析和稳定性对比 |
| `dask` | 分布式计算框架，用于超出内存限制的pandas/NumPy工作流，支持扩展现有代码到集群规模 |
| `database-lookup` | 确定性查询78个公共科学、生物医学、材料科学、监管和金融数据库 |
| `excel-analysis` | 分析Excel电子表格、创建数据透视表、生成图表并执行数据分析 |
| `exploratory-data-analysis` | 对200+种文件格式的科学数据执行综合探索性数据分析 |
| `imaging-data-commons` | 从NCI影像数据公共库查询和下载公共癌症影像数据，使用idc-index工具 |
| `markitdown` | 将文件和Office文档转换为Markdown，支持PDF、DOCX、PPTX、XLSX和图像（含OCR） |
| `matplotlib` | 底层绑图库，提供完全自定义控制，适用于需要精细调节每个图形元素的场景 |
| `networkx` | 在Python中使用NetworkX创建、分析和可视化复杂网络和图结构 |
| `polars` | 高性能DataFrame库，用于Python ETL、数据分析和pandas迁移，支持表达式API |
| `sci-xlsx` | 面向科学数据的Excel电子表格（.xlsx/.xlsm）创建、编辑和分析技能 |
| `scikit-learn` | Python机器学习库，用于监督学习（分类/回归）、无监督学习和特征工程 |
| `scikit-survival` | Python生存分析和时间-事件建模综合工具包 |
| `seaborn` | 基于pandas的统计可视化，用于快速探索分布、关系和统计模式 |
| `shap` | 使用SHAP进行模型可解释性和可解释AI分析，量化特征对预测的贡献 |
| `statistical-analysis` | 引导式统计分析和检验选择，帮助选择合适的统计方法并规范报告结果 |
| `statistical-power` | 样本量和统计功效计算，用于研究规划（回答“需要多少样本”类问题） |
| `statsmodels` | Python统计模型库，提供OLS/GLM/混合模型等特定模型类 |
| `umap-learn` | 使用UMAP-learn进行非线性降维、2D/3D嵌入和聚类预处理 |
| `usfiscaldata` | 查询美国财政部财政数据REST API获取联邦财务数据，无需API密钥 |
| `vaex` | 处理和分析超出内存限制的大型表格数据集（数十亿行），使用Vaex的懒加载和核外计算 |
| `xlsx` | 当电子表格文件是主要输入或输出时使用此技能。包括：打开、读取、编辑或修复现有的 .xlsx、.xlsm、.csv 或 .... |
| `zarr-python` | 云端存储的分块N维数组（Zarr-Python 3），支持压缩数组、并行I/O、S3/GCS云存储，兼容NumPy/Da... |

### Document & Content | 文档与内容 (17)

| Skill | 中文描述 |
|---|---|
| `ai-research-writing` | AI辅助学术论文写作全流程，涵盖结构起草、中英翻译、润色、去AI味、逻辑检查、实验分析、图表标题、审稿模拟等 |
| `content-research-writer` | 通过调研辅助高质量内容写作，添加引用、改善开头、优化结构和语气 |
| `docx` | 当用户需要创建、读取、编辑或操作 Word 文档（.docx 文件）时使用此技能。触发条件包括：任何提及 'Word 文... |
| `drafter-diagram` | 帮你把「系统怎么组成、流程怎么走、模块怎么连」画成一张好读的技术示意图，看起来像工整的工程图纸，线条清爽、不花哨。你只要... |
| `infographics` | 使用Nano Banana Pro AI创建专业信息图，支持智能迭代优化 |
| `latex-posters` | 使用beamerposter、tikzposter或baposter创建专业LaTeX研究海报 |
| `markdown-mermaid-writing` | 综合Markdown和Mermaid图表写作技能，创建科学文档、技术报告和流程图 |
| `notion-infographic` | 根据参考文稿批量生成 Notion 风格松弛感手绘信息图组图。当用户需要阅读文档并生成一组社交媒体传播用的信息图时使用此... |
| `pdf` | 当用户需要对 PDF 文件执行任何操作时使用此技能。包括：读取或提取 PDF 中的文本/表格、合并多个 PDF、拆分 P... |
| `pptx` | 当 .pptx 文件以任何方式涉及时使用此技能——无论是作为输入、输出还是两者兼有。包括：创建幻灯片、演示文稿或路演材料... |
| `pptx-posters` | 使用HTML/CSS创建可导出为PDF或PPTX的研究海报 |
| `qoderwork-ppt` | 生成 QoderWork 风格演示文稿。根据主题自动匹配 14 种模板，输出可编辑的 .pptx 文件。 |
| `sci-docx` | 面向科学写作的Word文档（.docx）创建、编辑和操作技能 |
| `sci-pdf` | 面向科学写作的PDF文件处理技能，包括阅读、提取和生成学术PDF |
| `sci-pptx` | 面向科学演示的PowerPoint（.pptx）文件处理技能 |
| `venue-templates` | 访问主要科学会议的LaTeX模板、格式要求和投稿指南 |
| `writing-great-skills` | 技能编写参考——编写和编辑高质量Agent技能的词汇和原则 |

### Research & Academic | 科研与学术 (12)

| Skill | 中文描述 |
|---|---|
| `citation-management` | 学术引用管理，搜索Google Scholar和PubMed获取论文，生成规范引用格式 |
| `deep-research` | 对技术主题进行系统性深度研究，包含来源验证、三角互证和引用分析 |
| `exa-search` | 基于Exa的网络搜索工具，针对科学和技术内容优化，支持语义搜索和结构化结果 |
| `exam-cheatsheet` | 从课程材料（PPT/PDF/DOCX）生成综合2页A4考试速查表，结合公式、定义和关键概念 |
| `literature-review` | 使用多个学术数据库（PubMed/arXiv/Semantic Scholar等）进行综合系统文献综述 |
| `market-research-reports` | 生成综合市场研究报告（50+页），模仿McKinsey/BCG等顶级咨询公司的报告风格 |
| `paper-lookup` | 通过REST API搜索10个学术论文数据库，获取研究论文、预印本和学术文章 |
| `paperzilla` | 与Agent讨论Paperzilla中的项目、推荐和经典论文，管理研究知识库 |
| `parallel-web` | 基于parallel-cli的综合网络工具包，针对学术和科学搜索优化 |
| `research-grants` | 撰写竞争性研究基金申请（NSF/NIH/DOE/DARPA等），包含机构特定格式和预算模板 |
| `research-lookup` | 使用parallel-cli搜索引擎查找最新研究信息和学术文献 |
| `scholar-evaluation` | 使用ScholarEval框架系统性评估学术作品，提供结构化评估报告 |

### Infrastructure & DevOps | 基础设施与运维 (5)

| Skill | 中文描述 |
|---|---|
| `cloudflare-deploy` | 使用Workers、Pages等平台服务将应用和基础设施部署到Cloudflare |
| `git-guardrails-claude-code` | 设置Git安全护栏，阻止危险命令（push、reset --hard、clean、branch -D等） |
| `modal` | Modal无服务器云平台，按需运行Python代码（含按需GPU），适用于云GPU计算任务 |
| `setup-pre-commit` | 在当前项目中设置Husky预提交钩子（Prettier/类型检查/测试） |
| `vercel-deploy` | 将应用程序和网站部署到 Vercel。适用于用户请求部署操作，如"部署我的应用"、"部署并给我链接"、"上线"或"创建预... |

### Scientific Computing | 科学计算 (22)

| Skill | 中文描述 |
|---|---|
| `astropy` | 天文学和天体物理学核心Python库，涵盖单位转换、坐标系、FITS文件、天文时间等API |
| `cirq` | Google量子计算框架，用于设计量子电路、噪声感知编程和在Google Quantum AI硬件上运行 |
| `experimental-design` | 数据采集前的实验设计，包括选择设计方案、随机化、区组化和样本量计算 |
| `fluidsim` | 基于Python的计算流体力学模拟框架，用于运行流体动力学仿真 |
| `hugging-science` | 在科学领域（生物/化学/物理/天文）进行AI/ML工作时使用，整合Hugging Face生态 |
| `matlab` | MATLAB和GNU Octave数值计算，涵盖矩阵运算、数据分析、可视化和信号处理 |
| `optimize-for-gpu` | 使用CuPy、Numba CUDA、Warp、cuDF、cuML等库对Python代码进行GPU加速 |
| `peer-review` | 结构化稿件/基金评审，使用清单式评估方法撰写正式同行评审报告 |
| `pennylane` | 硬件无关的量子机器学习框架，支持自动微分，用于训练量子电路 |
| `pymatgen` | 材料科学工具包，处理晶体结构（CIF/POSCAR）、相图、能带结构和态密度 |
| `pymc` | 使用PyMC进行贝叶斯建模，构建层次模型、MCMC（NUTS）、变分推断和LOO/WAIC模型比较 |
| `pymoo` | 多目标优化框架，支持NSGA-II/III、MOEA/D、Pareto前沿和约束处理 |
| `qiskit` | IBM量子计算框架，用于在IBM Quantum硬件和Qiskit Runtime上设计和运行量子程序 |
| `qutip` | 量子物理仿真库，用于开放量子系统研究（主方程/Lindblad/量子光学） |
| `scientific-brainstorming` | 创造性研究头脑风暴和探索，用于开放式的跨学科思维和研究灵感激发 |
| `scientific-critical-thinking` | 评估科学论断和证据质量，用于检验实验设计有效性和识别方法论缺陷 |
| `scientific-slides` | 为学术报告构建幻灯片和演示文稿，适用于会议演讲和学术答辩 |
| `scientific-visualization` | 出版质量图形的元技能，用于创建需要多库协作的期刊投稿图 |
| `scientific-writing` | 科学写作的核心技能，以流畅段落（非列表）撰写完整科学手稿 |
| `simpy` | Python中的基于进程的离散事件仿真框架，用于构建仿真模型 |
| `sympy` | Python精确符号数学——代数、微积分、方程求解和符号线性代数 |
| `timesfm-forecasting` | 使用Google TimesFM基础模型进行零样本时间序列预测，适用于单变量预测任务 |

### Healthcare & Clinical | 医疗与临床 (5)

| Skill | 中文描述 |
|---|---|
| `clinical-decision-support` | 为药物研发和临床研究生成专业的临床决策支持（CDS）文档 |
| `clinical-reports` | 撰写综合临床报告，包括病例报告（CARE指南）、诊断报告等，遵循医学写作规范 |
| `iso-13485-certification` | 综合工具包，用于准备ISO 13485医疗器械质量管理体系认证文档 |
| `pydicom` | Python DICOM（医学数字成像和通信）文件处理库，读写和解析医学影像数据 |
| `treatment-plans` | 以LaTeX/PDF格式生成简洁（3-4页）聚焦的医学治疗方案，涵盖所有临床专科 |

### Productivity & Workflow | 效率与工作流 (53)

| Skill | 中文描述 |
|---|---|
| `adaptyv` | Adaptyv Bio Foundry API和Python SDK集成，用于蛋白质实验设计、提交和结果分析 |
| `aeon` | 时间序列机器学习技能，涵盖分类、回归、聚类等任务，支持aeon框架的时间序列分析 |
| `arbor` | 自主改进实际制品（代码、训练配方、Agent框架、数据流水线、提示词），通过迭代反思提升质量 |
| `ask-matt` | 技能路由器，询问当前情境应使用哪个技能或流程，覆盖本仓库中所有用户可调用的技能 |
| `autoskill` | 通过屏幕监控检测重复研究工作流，自动匹配已有技能并建议新技能创建 |
| `c-drive-cleaner` | 分析和清理Windows C盘空间，扫描大文件和文件夹并分类（可移动/可压缩/可删除） |
| `check-meituan-progress` | 监控美团商家评论采集进度，完成后运行分析并导出结果 |
| `codebase-design` | 代码库设计共享词汇，用于设计深度模块和改进代码架构 |
| `consciousness-council` | 运行多视角心智会议审议，对任何问题进行多角色深度讨论和决策 |
| `create-plan` | 将需求转化为可执行的故事卡，包含任务、依赖关系和针对性技术指导 |
| `create-skill` | 引导用户为 QoderWork 创建有效的 Agent 技能。当用户想要创建、编写或制作新技能，或询问技能结构、最佳实践... |
| `deeptools` | NGS分析工具包，支持BAM到bigWig转换、QC（相关性/PCA/指纹）、热图和谱图分析 |
| `dev-favorites-updater` | 执行个人开发收藏集的每日更新工作流，涵盖抓取、分类、去重和发布 |
| `dhdna-profiler` | 从文本中提取认知模式和思维指纹，分析用户的思考方式和决策风格 |
| `diagnosing-bugs` | 疑难Bug和性能回退的诊断循环，用于系统排查“诊断/调试”类问题 |
| `domain-modeling` | 构建和打磨项目领域模型，锁定领域术语和业务逻辑的精确表达 |
| `dws` | 管理钉钉产品能力（AI/日历/通讯录/群聊/消息/平台文档/审批文档/考勤/日志/DING消息/智能平台文档/开放文档/... |
| `etetoolkit` | 系统发育树工具包（ETE），支持树操作（Newick/NHX）、进化事件检测和直系同源分析 |
| `find-skills` | 从官方市场、社区源以及企业技能市场（若通过 MCP 可用）搜索并安装专用技能。处理任何实质性任务前应先调用此技能查找可用... |
| `frontend-design` | 创建独特的生产级前端界面，追求高设计质量和用户体验 |
| `geomaster` | 综合地理空间科学技能，涵盖遥感、GIS、空间分析、机器学习和地球科学可视化 |
| `geopandas` | Python地理空间矢量数据库，支持Shapefile、GeoJSON和GeoPackage格式操作 |
| `grill-me` | 不间断的面试式问答，用于打磨方案或设计的细节和逻辑 |
| `grill-with-docs` | 面试式问答加文档生成，在打磨方案的同时创建ADR和术语表文档 |
| `grilling` | 对方案或设计进行不间断的质疑和压力测试，找出潜在问题和改进点 |
| `handoff` | 将当前对话压缩为交接文档，供另一个Agent接手继续工作 |
| `hypogenic` | 基于LLM的自动化假设生成和验证，系统性探索表格数据集中的假设空间 |
| `implement` | 基于PRD或Issue列表实现具体功能，将规划转化为可运行代码 |
| `improve-codebase-architecture` | 扫描代码库寻找深化机会，生成可视化HTML报告并逐步改进架构 |
| `install-skill-dependency` | 诊断并修复已安装技能所需的缺失依赖、二进制文件或运行时环境。当技能因缺少资源、二进制文件未找到、运行时依赖不可用而失败时... |
| `liteparse` | 本地文档和PDF解析，提取空间文本和边界框，适用于结构化文档信息提取 |
| `migrate-to-shoehorn` | 将测试文件从as类型断言迁移到@total-typescript/shoehorn格式 |
| `my-coffee` | 瑞幸咖啡点单助手，搜索门店/产品、查询取餐码/订单状态和管理咖啡订单 |
| `nextflow` | 构建、运行和调试Nextflow数据流水线和nf-core工作流 |
| `open-notebook` | 自托管开源Google NotebookLM替代品，用于AI驱动的研究和文档分析 |
| `pacsomatic` | nf-core/pacsomatic配对肿瘤-正常样本工作流操作工具包，从BAM输入开始处理 |
| `pi-agent` | 使用Pi（极简终端编码工具）进行开发和配置，管理Pi安装和项目设置 |
| `plugin-creator` | 创建、定制或修改 QoderWork 专家套件。当用户想要创建新套件、定制已有套件或编辑套件内的技能/指令时使用。 |
| `prototype` | 构建一次性原型——可运行的终端应用，用于验证状态/业务逻辑设计 |
| `pylabrobot` | 厂商无关的实验室自动化框架，控制多种设备（Hamilton/Tecan/Opentrons） |
| `pyzotero` | 使用pyzotero客户端与Zotero文献管理库交互，检索、创建和管理引用 |
| `quickbi-smartq-chat` | QuickBI智能问答，通过对话方式查询和分析数据 |
| `resolving-merge-conflicts` | 解决正在进行的git合并/变基冲突，提供交互式冲突解决指导 |
| `scaffold-exercises` | 创建包含章节、问题、答案和解释器的练习目录结构，支持literate模式 |
| `setup-matt-pocock-skills` | 配置工程技能仓库，设置Issue追踪器、分类标签和项目工作流 |
| `tdd` | 测试驱动开发，先写测试再实现功能或修复Bug的TDD工作流 |
| `teach` | 在工作空间中教授用户新技能或概念，采用循序渐进的教学方式 |
| `to-issues` | 将计划、规格或PRD拆分为独立可领取的Issue，发布到项目Issue追踪器 |
| `to-prd` | 将当前对话转化为PRD并发布到项目Issue追踪器，无需额外访谈 |
| `triage` | 将Issue通过状态机推进——分类、复现、深度质疑并撰写分析报告 |
| `vm-error-recovery` | 诊断并引导用户自行修复安全工作环境准备错误。当用户提到安全工作环境启动失败、无法连接、下载出错或任何安全工作环境相关异常... |
| `weekly-report-writer` | 个人周报生成器，综合Obsidian笔记库中的条目和任务记录，生成结构化的每周工作总结 |
| `what-if-oracle` | 运行结构化假设分析（What-If），探索4-6个分支可能性（最佳/最可能/最差/意外/对比） |

## Usage / 使用方法

Skills are designed for [QoderWork](https://docs.qoder.com/qoderwork/introduction). Each skill directory contains a `SKILL.md` manifest defining behavior, triggers, and tools.

技能适用于 [QoderWork](https://docs.qoder.com/qoderwork/introduction)。每个技能目录包含定义行为、触发条件和工具的 `SKILL.md` 清单文件。

## License / 许可证

Personal skill collection aggregated from multiple sources. See individual skill directories for specific licensing.
