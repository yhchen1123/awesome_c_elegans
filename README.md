<h1>Awesome <i>C. elegans</i> Embryogenesis</h1>

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![papers](https://img.shields.io/badge/papers-84-blue) ![last update](https://img.shields.io/badge/last_update-2026--09--28-green)

> AI-curated, human-audited multidisciplinary literature tracking for *C. elegans* embryogenesis research — from lineage-resolved atlases and live imaging to mechanics, molecular regulation, and dynamical modeling. Updated weekly by automation; every update lands as a reviewed PR.

This repository is maintained by an **AI-search + human-PR-audit** loop: a weekly GitHub Actions run queries Europe PMC (PubMed + bioRxiv/medRxiv) and arXiv for new literature, an LLM classifies candidates into the taxonomy below and writes Chinese relevance notes, and all changes are delivered as a pull request for human review — nothing is pushed to `main` directly. A monthly digest summarizes the month's additions by theme and watches for retractions. Each category also has a dedicated page under `categories/` with the full cross-listed entries. See `CONTRIBUTING.md` for inclusion criteria and `docs/DEVELOPMENT.md` for operations. License: CC0-1.0 (see `LICENSE`).

> ⚠️ **C7 soft-cap warning:** T3-transfer entries make up 86% of Methods Transfer (12/14), exceeding the 30% soft cap. Maintainers should consider tightening arXiv queries or triaging low-relevance entries.

## Contents

- [Measurement & Tracking](#measurement--tracking)
- [Cell & Embryo Representation](#cell--embryo-representation)
- [WT Developmental Dynamics](#wt-developmental-dynamics)
- [Morphology & Mechanics](#morphology--mechanics)
- [Molecular Regulation & Coupling](#molecular-regulation--coupling)
- [Perturbation & Causal Inference](#perturbation--causal-inference)
- [Fate Specification & Lineage Biology](#fate-specification--lineage-biology)
- [Methods Transfer](#methods-transfer)
- [Datasets, Benchmarks & Software](#datasets-benchmarks--software)
- [Reviews & Perspectives](#reviews--perspectives)

## Measurement & Tracking

**测量与追踪** · C0

- [EmbSAM: cell boundary localization and Segment Anything Model for fast images of developing embryos](https://doi.org/10.1038/s42003-025-09220-3) - Guan et al., *Communications Biology* 2025 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *EmbSAM：面向发育胚胎低信噪比膜图像的 SAM 分割管线（边界定位+Segment Anything）；膜分割的实用工具。*
- [LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532) - Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint` · also filed under `C7`<br>
  *corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。*
- [Sparse Annotation is Sufficient for Bootstrapping Dense Neuron Segmentation](https://doi.org/10.1101/2024.06.14.599135) - Manor et al., *bioRxiv* 2024 `T3-transfer` `preprint` · also filed under `C7`<br>
  *从稀疏 2D 标注自举稠密 3D 分割的通用方法；降低三维标注成本，对胚胎膜分割标注有直接参考价值。*
- [WaveOrder: A differentiable wave-optical framework for scalable biological microscopy with diverse modalities](https://arxiv.org/abs/2412.09775) - Chandler et al., *arXiv* 2024 `T3-transfer` `preprint` · also filed under `C7`<br>
  *WaveOrder：可微波动光学显微框架，统一多种成像模态的正演模型；显微成像物理可微化的参照。*
- [A high-content imaging approach to profile C. elegans embryonic development](https://doi.org/10.1242/dev.174029) - Wang et al., *Development* 2019 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *高内涵成像剖析线虫胚胎发育，自动提取形态与分裂特征；胚胎表型特征提取管线的代表工作。*
- [In Toto Imaging and Reconstruction of Post-Implantation Mouse Development at the Single-Cell Level](https://doi.org/10.1016/j.cell.2018.09.031) - McDole et al., *Cell* 2018 `T3-transfer` `peer-reviewed` · also filed under `C8`<br>
  *小鼠着床后发育的 in toto 光片成像与单细胞重建（含多胚胎统计动态图谱）；全胚胎动态图谱的范式性工作。*
- [Tissue cartography: compressing bio-image data by dimensional reduction](https://doi.org/10.1038/nmeth.3648) - Heemskerk et al., *Nature Methods* 2015 `T3-transfer` `peer-reviewed` · also filed under `C8`<br>
  *组织制图学通用框架：曲面到平面映射的畸变控制与无缝导航；胚胎表面成像数据降维的方法参照。*
- [Systematic quantification of developmental phenotypes at single-cell resolution during embryogenesis](https://doi.org/10.1242/dev.096040) - Moore et al., *Development* 2013 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *单细胞分辨的发育表型系统量化（自动图像分析提取数十种测量）；线虫胚胎表型组学的早期方法。*
- [Automated cell lineage tracing in Caenorhabditis elegans](https://doi.org/10.1073/pnas.0511111103) - Bao et al., *Proceedings of the National Academy of Sciences* 2006 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *StarryNite/AceTree 自动谱系追踪的开山之作；后续测量管线的基线与数据兼容层，其 tracking error 沿长轨迹传播的问题至今仍是改进目标。*

*See the [category page](categories/C0-measurement-tracking.md) for 1 cross-listed entry filed primarily elsewhere.*

## Cell & Embryo Representation

**细胞与胚胎表示** · C1

- [MultiCell: geometric learning in multicellular development](https://doi.org/10.1038/s41592-025-02983-x) - Yang et al., *Nature Methods* 2026 `T3-transfer` `peer-reviewed` · also filed under `C7`<br>
  *MultiCell：几何深度学习预测多细胞发育中每个细胞的行为；几何归纳偏置用于发育建模的代表工作。*
- [Interpretable representation learning for 3D multi-piece intracellular structures using point clouds](https://doi.org/10.1038/s41592-025-02729-9) - Vasan et al., *Nature Methods* 2025 `T3-transfer` `peer-reviewed` · also filed under `C7`<br>
  *点云表示学习刻画 3D 胞内多部件结构且保持可解释；3D 生物结构表示学习的参照。*
- [Characterizing Cellular Physiological States with Three-Dimensional Shape Descriptors for Cell Membranes](https://doi.org/10.3390/membranes14060137) - Guan et al., *Membranes* 2024 `T1-core` `peer-reviewed` · also filed under `C3`<br>
  *三维细胞膜形状描述子刻画细胞生理状态；谱系分辨胚胎细胞形态表示的基础方法。*
- [Morphodynamical cell state description via live-cell imaging trajectory embedding](https://doi.org/10.1038/s42003-023-04837-8) - Copperman et al., *Communications Biology* 2023 `T3-transfer` `peer-reviewed` · also filed under `C7`<br>
  *活细胞成像轨迹嵌入的形态动力学细胞状态描述；以轨迹历史而非单帧特征表示细胞状态的方法。*

## WT Developmental Dynamics

**野生型发育动力学** · C2

- [A kinematic equation for the morphogenetic reproducibility of an animal](https://doi.org/10.65215/ltspreprints.2026.04.04.000174) - Wang et al., *LTS Preprints* 2026 `T1-core` `emerging-evidence`<br>
  *⚠️ emerging evidence: 形态发生可重复性的运动学方程；与发育稳健性/可重复性定量研究直接相关。**注意：按本仓库证据规则视为 emerging evidence，未经同行评审与独立验证前不得作为既定共识引用。***
- [Developmental chronology of mouse embryo from 2-cell stage through birth](https://doi.org/10.1038/s41556-026-01971-3) - Cao et al., *Nature Cell Biology* 2026 `T3-transfer` `peer-reviewed` · also filed under `C8`<br>
  *小鼠胚胎从 2 细胞到出生的发育年表资源；跨物种发育时序参照系。*
- [Geometry-driven asymmetric cell divisions pattern cell cycles and zygotic genome activation in the zebrafish embryo](https://doi.org/10.1038/s41567-025-03122-1) - Mishra et al., *Nature Physics* 2026 `T3-transfer` `peer-reviewed` · also filed under `C3`<br>
  *斑马鱼受精几何（曲率/体积）作为初始条件触发不对称分裂与细胞周期梯度，进而影响合子激活；几何决定发育可重复性的范例。*
- [Intracellular buffering enables developmental robustness after genome doubling in C. elegans embryos](https://doi.org/10.1016/j.celrep.2026.117005) - Yang et al., *Cell Reports* 2026 `T1-core` `peer-reviewed` · also filed under `C5`<br>
  *基因组加倍后细胞内缓冲保障发育稳健性；倍性扰动下稳健性机制的直接证据。*
- [Quantitative Resolving Cell Fate in the Early Embryogenesis of Caenorhabditis elegans](https://doi.org/10.1101/2024.10.25.620330) - Xiong et al., *bioRxiv* 2024 `T1-core` `preprint` · also filed under `C6`<br>
  *用景观/路径类方法定量解析早期胚胎的细胞命运决定；不变谱系框架下命运景观的定量尝试。*
- [Temporal variability and cell mechanics control robustness in mammalian embryogenesis](https://doi.org/10.1126/science.adh1145) - Fabrèges et al., *Science* 2024 `T3-transfer` `peer-reviewed` · also filed under `C3`<br>
  *哺乳动物胚胎中时间变异与细胞力学共同控制发育稳健性；变异并非纯噪声而可成为稳健性来源的跨物种定量证据。*
- [Defect-buffering cellular plasticity increases robustness of metazoan embryogenesis](https://doi.org/10.1016/j.cels.2022.07.001) - Xiao et al., *Cell Systems* 2022 `T1-core` `peer-reviewed` · also filed under `C5`<br>
  *系统量化保守基因敲低诱导的细胞缺陷，揭示细胞可塑性对缺陷的缓冲机制；「扰动→缺陷→缓冲」发育稳健性框架的实证基础。*
- [Maps of variability in cell lineage trees](https://doi.org/10.1371/journal.pcbi.1006745) - Hicks et al., *PLOS Computational Biology* 2019 `T3-transfer` `peer-reviewed`<br>
  *谱系树变异图谱的统计框架；在树结构上定量比较变异分布的可迁移工具。*
- [Systems Properties and Spatiotemporal Regulation of Cell Position Variability during Embryogenesis](https://doi.org/10.1016/j.celrep.2018.12.052) - Li et al., *Cell Reports* 2019 `T1-core` `peer-reviewed`<br>
  *细胞位置变异与谱系/对称性/接触相关且存在系统性变异压缩；发育稳健性（canalization）定量研究的重要实证基础。*
- [Control of cell cycle timing during C. elegans embryogenesis](https://doi.org/10.1016/j.ydbio.2008.02.054) - Bao et al., *Developmental Biology* 2008 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *细胞周期时序的统计分析：分裂同步性与顺序不变性同命运分化耦合，提出命运控制细胞周期节奏的三层模型；WT 发育时序的基础定量工作。*

*See the [category page](categories/C2-wt-dynamics.md) for 3 cross-listed entries filed primarily elsewhere.*

## Morphology & Mechanics

**形态与力学** · C3

- [Boundary geometry controls a topological defect transition that determines lumen nucleation in embryonic development](https://doi.org/10.1038/s41563-026-02594-7) - Guruciaga et al., *Nature Materials* 2026 `T3-transfer` `peer-reviewed`<br>
  *边界几何控制三维拓扑缺陷转变并决定小鼠胚胎腔体成核位置；边界条件-缺陷-形态发生链条的实验证据。*
- [Boundary-guided cell alignment drives mouse epiblast maturation](https://doi.org/10.1038/s41567-026-03176-9) - Ichikawa et al., *Nature Physics* 2026 `T3-transfer` `peer-reviewed`<br>
  *边界引导的细胞对齐驱动小鼠上胚层成熟与放射状构型形成；边界几何约束组织模式的直接证据。*
- [Integrated quantitative imaging and biomechanical modeling of early gastrulation in C. elegans](https://doi.org/10.64898/2026.03.30.715391) - Thiels et al., *bioRxiv* 2026 `T1-core` `preprint`<br>
  *线虫早期原肠形成（Ea/Ep 内陷）的定量成像与生物力学建模整合分析；顶端收缩驱动内陷的系统力学拆解。*
- [Keratins coordinate tissue spreading by balancing spreading forces with tissue material properties](https://doi.org/10.1038/s41467-026-72366-z) - Naik et al., *Nature Communications* 2026 `T3-transfer` `peer-reviewed`<br>
  *角蛋白网络通过平衡扩展力与组织材料性质协调组织扩展；组织材料性质与主动力耦合的定量案例。*
- [Morphospace analysis reveals divergent cellular behaviours driving tissue internalisation during insect gastrulation](https://doi.org/10.64898/2026.06.30.735526) - Battistara et al., *bioRxiv* 2026 `T3-transfer` `preprint`<br>
  *昆虫原肠形成的形态空间分析，量化多种细胞行为路径驱动组织内化；形态空间比较方法可迁移至其他胚胎系统。*
- [Nematic structures contribute to robust zygotic polarization in C. elegans](https://doi.org/10.1371/journal.pcbi.1014792) - Vanslambrouck et al., *PLOS Computational Biology* 2026 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *建立线虫合子极化的 3D 力学模型（皮层收缩丝网络），复现 cortical flow、表面褶皱与张力各向异性，提出密度依赖收缩的机械负反馈机制；形态-力学耦合建模在单细胞阶段的直接参照，与 FIDES 力推断工作出自同一团队。*
- [Quantifying the Single‐Cell Morphological Landscape of Cellular Transdifferentiation through Force Field Reconstruction](https://doi.org/10.1002/advs.202512325) - Yu et al., *Advanced Science* 2026 `T3-transfer` `peer-reviewed` · also filed under `C7`<br>
  *从跨分化快照重建单细胞形态景观与力场（无细胞特异速度信息）；形态动力学重建方法可迁移至胚胎形态数据。*
- [Spatiotemporal mapping of the contractile and adhesive forces sculpting early C. elegans embryos](https://doi.org/10.1016/j.devcel.2026.04.013) - Yamamoto et al., *Developmental Cell* 2026 `T1-core` `peer-reviewed`<br>
  *早期线虫胚胎收缩力与粘附力的时空图谱；力图谱从皮层张力扩展到细胞-细胞粘附维度。*
- [VertAX: a differentiable vertex model for learning epithelial tissue mechanics](https://arxiv.org/abs/2604.06896) - Pasqui et al., *arXiv* 2026 `T3-transfer` `preprint` · also filed under `C7`<br>
  *VertAX：可微顶点模型，以梯度优化学习上皮组织力学参数；可微组织力学模拟器路线的新成员。*
- [&lt;b&gt;Genetic-Morphological Synergy Governs Cell Fate Specification in Development&lt;/b&gt;](https://doi.org/10.65215/rmqcg166) - Guan et al., *LTS Preprints* 2025 `T1-core` `preprint` · also filed under `C6`<br>
  *遗传与形态的协同支配发育中的命运决定；基因型-形态表型联合定量分析框架。*
- [Cell lineage-resolved embryonic morphological map reveals signaling associated with cell fate and size asymmetry](https://doi.org/10.1038/s41467-025-58878-0) - Guan et al., *Nature Communications* 2025 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *CMap 谱系分辨形态图谱：位置、体积、表面积、接触面积的全胚胎时空图谱；细胞表示与形态力学研究的核心几何数据源。*
- [Image-based force inference by biomechanical simulation](https://doi.org/10.1371/journal.pcbi.1012629) - Vanslambrouck et al., *PLOS Computational Biology* 2024 `T2-adjacent` `peer-reviewed`<br>
  *FIDES 生物力学仿真力推断；为「形态约束力学但不等同绝对 force」的可识别性讨论提供方法样本。*
- [Self-organized tissue mechanics underlie embryonic regulation](https://doi.org/10.1038/s41586-024-07934-8) - Caldarelli et al., *Nature* 2024 `T3-transfer` `peer-reviewed` · also filed under `C5`<br>
  *鸟类胚胎自组织组织力学支撑的胚胎调节现象（分割后重建完整胚胎）；扰动-恢复与自修复的力学基础。*
- [Axis convergence in C. elegans embryos](https://doi.org/10.1016/j.cub.2023.10.050) - Bhatnagar et al., *Current Biology* 2023 `T1-core` `peer-reviewed`<br>
  *肌动球蛋白流驱动单细胞胚胎 AP 轴向长轴收敛，假分裂沟为主要驱动而胞质流贡献较小；合子期力学-几何耦合的定量拆解。*
- [Embryo mechanics cartography: inference of 3D force atlases from fluorescence microscopy](https://doi.org/10.1038/s41592-023-02084-7) - Ichbiah et al., *Nature Methods* 2023 `T1-core` `peer-reviewed`<br>
  *从荧光显微图像反推 3D 力学图谱；inverse mechanics（由形态反推力学）路线的关键方法参照。*
- [Computable early Caenorhabditis elegans embryo with a phase field model](https://doi.org/10.1371/journal.pcbi.1009755) - Kuang et al., *PLOS Computational Biology* 2022 `T1-core` `peer-reviewed`<br>
  *早期胚胎的可计算 phase-field forward simulator；可计算胚胎形态发生模拟器方向的先行者，也是「力不可唯一识别」问题的实例。*
- [System-Level Quantification and Phenotyping of Early Embryonic Morphogenesis of Caenorhabditis elegans](https://doi.org/10.1101/776062) - Guan et al., *bioRxiv* 2019 `T1-core` `preprint` · also filed under `C2`<br>
  *早期胚胎形态发生的系统级定量与表型分析；全胚胎形态变异定量的早期框架（bioRxiv 预印本）。*
- [Glass-like dynamics of collective cell migration](https://doi.org/10.1073/pnas.1010059108) - Angelini et al., *Proceedings of the National Academy of Sciences* 2011 `T3-transfer` `peer-reviewed`<br>
  *集体细胞迁移的类玻璃动力学（jamming）奠基描述；细胞集体运动的物理框架，可迁移至胚胎细胞重排分析。*
- [Chiral Forces Organize Left-Right Patterning in C. elegans by Uncoupling Midline and Anteroposterior Axis](https://doi.org/10.1016/j.devcel.2010.08.014) - Pohl et al., *Developmental Cell* 2010 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *手性力通过解耦中线与前后轴组织线虫左右图式形成；皮层力学驱动体轴图式的经典案例。*

*See the [category page](categories/C3-morphology-mechanics.md) for 6 cross-listed entries filed primarily elsewhere.*

## Molecular Regulation & Coupling

**分子调控与耦合** · C4

- [Decoding cell division history and lineage-resolved phenotypic patterns from single-cell barcode and transcriptomic data](https://doi.org/10.1101/gr.281734.125) - Yu et al., *Genome Research* 2026 `T2-adjacent` `peer-reviewed` · also filed under `C7`<br>
  *FateScape 框架联合谱系条形码与转录组推断细胞分裂树拓扑并刻画深度分辨的表型分布，在线虫胚胎数据上验证了谱系拓扑重建；为「谱系×分子状态」联合分析提供方法参照，也是 destructive assay 限制下的替代观测路线。*
- [PASTRI: Resolving Stage-Specific Cell-State Dynamics from Annotated Cell Lineage Trees](https://doi.org/10.64898/2026.08.16.745065) - Yang et al., *bioRxiv* 2026 `T1-core` `preprint` · also filed under `C2`<br>
  *PASTRI：从带末端状态标注的谱系树推断阶段特异的细胞状态转移速率，在线虫胚胎谱系上验证；利用不同谱系距离绕过动力学随发育变化的问题。*
- [Integrating representation learning, permutation, and optimization to detect lineage-related gene expression patterns](https://doi.org/10.1038/s41467-025-56388-7) - Schlüter et al., *Nature Communications* 2025 `T3-transfer` `peer-reviewed` · also filed under `C7`<br>
  *PORCELAN：表示学习+置换检验+优化检测谱系相关基因表达模式；谱系条形码×表达联合分析的新方法。*
- [Lineage-resolved analysis of embryonic gene expression evolution in C. elegans and C. briggsae](https://doi.org/10.1126/science.adu8249) - Large et al., *Science* 2025 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *跨物种谱系分辨表达演化；为 lineage 与 transcriptome 非恒定关系及远缘谱系分子收敛提供证据。*
- [RNA velocity in growing cells](https://doi.org/10.64898/2025.12.18.695252) - Shah et al., *bioRxiv* 2025 `T3-transfer` `preprint` · also filed under `C7`<br>
  *指出 RNA velocity 因忽略细胞生长而产生根本误差；基于 scRNA 的轨迹推断方法学的重要警示。*
- [A spatiotemporally resolved atlas of mRNA decay in the C. elegans embryo reveals differential regulation of mRNA stability across stages and cell types](https://doi.org/10.1101/gr.278980.124) - Peng et al., *Genome Research* 2024 `T1-core` `peer-reviewed`<br>
  *胚胎 mRNA 降解的时空图谱：mRNA 稳定性按发育阶段与细胞类型差异化调控；表达动力学中降解维度的资源。*
- [Gene regulatory patterning codes in early cell fate specification of the C. elegans embryo](https://doi.org/10.7554/elife.87099) - Cole et al., *eLife* 2024 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *早期命运决定的调控 patterning code；为「当前状态 → 命运决策 → 新调控状态」的转移规律研究提供分子层证据。*
- [Spatiotemporal analysis of mRNA-protein relationships enhances transcriptome-based developmental inference](https://doi.org/10.1016/j.celrep.2024.113928) - Fan et al., *Cell Reports* 2024 `T1-core` `peer-reviewed`<br>
  *mRNA 与蛋白非同步、非一一对应的直接证据；为发育推断中的 mRNA-蛋白时间延迟建模提供实验依据。*
- [Transcript accumulation rates in the early Caenorhabditis elegans embryo](https://doi.org/10.1126/sciadv.adi1270) - Sivaramakrishnan et al., *Science Advances* 2023 `T1-core` `peer-reviewed`<br>
  *基因组尺度估计合子 mRNA 积累速率（scRNA-seq + 单分子成像校准）；快速转录如何支撑快速命运决定的定量图景。*
- [A 4D single-cell protein atlas of transcription factors delineates spatiotemporal patterning during embryogenesis](https://doi.org/10.1038/s41592-021-01216-1) - Ma et al., *Nature Methods* 2021 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *转录因子蛋白的 4D（时空+谱系）表达图谱；蛋白层表达动力学的核心资源。*
- [Single‐cell dynamics of chromatin activity during cell lineage differentiation in Caenorhabditis elegans embryos](https://doi.org/10.15252/msb.202010075) - Zhao et al., *Molecular Systems Biology* 2021 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *利用位置效应推断早期胚胎每个谱系细胞的染色质活性景观：染色质状态区分细胞状态并随谱系分化；表观层状态-命运关联的系统证据。*
- [A lineage-resolved molecular atlas of C. elegans embryogenesis at single-cell resolution](https://doi.org/10.1126/science.aax1971) - Packer et al., *Science* 2019 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *谱系分辨单细胞转录组图谱的奠基数据集；谱系-分子联合分析的主要数据来源，destructive assay 导致的纵向轨迹缺失是此类数据的核心观测限制。*
- [Homeostasis of protein and mRNA concentrations in growing cells](https://doi.org/10.1038/s41467-018-06714-z) - Lin et al., *Nature Communications* 2018 `T3-transfer` `peer-reviewed`<br>
  *生长细胞中蛋白与 mRNA 浓度稳态的极小模型（聚合酶/核糖体限制）；为表达动力学与剂量效应建模提供理论基线。*
- [A Transcriptional Lineage of the Early C. elegans Embryo](https://doi.org/10.1016/j.devcel.2016.07.025) - Tintori et al., *Developmental Cell* 2016 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *16 细胞期前每个胚胎细胞的 RNA-seq 转录谱系；细胞级合子基因组激活图谱的奠基数据集。*
- [Mapping and analysis of Caenorhabditis elegans transcription factor sequence specificities](https://doi.org/10.7554/elife.06967) - Narasimhan et al., *eLife* 2015 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *线虫转录因子序列特异性的系统图谱；TF-DNA 特异性资源，支撑调控 motif 层分析。*
- [De Novo Inference of Systems-Level Mechanistic Models of Development from Live-Imaging-Based Phenotype Analysis](https://doi.org/10.1016/j.cell.2013.11.046) - Du et al., *Cell* 2014 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *从活成像表型数据自动推断系统级机制模型（谱系追踪+组织特异表达组合）；数据驱动机制推断的开创性工作。*
- [Regulatory analysis of the C. elegans genome with spatiotemporal resolution](https://doi.org/10.1038/nature13497) - Araya et al., *Nature* 2014 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *线虫基因组的时空分辨调控分析（转录因子结合图谱）；调控结合的时空资源。*
- [Multidimensional regulation of gene expression in the C. elegans embryo](https://doi.org/10.1101/gr.131920.111) - Murray et al., *Genome Research* 2012 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *线虫胚胎基因表达的多维调控解析（启动子驱动的时空表达）；时空分辨调控分析的早期系统工作。*

*See the [category page](categories/C4-molecular-regulation.md) for 6 cross-listed entries filed primarily elsewhere.*

## Perturbation & Causal Inference

**扰动与因果推断** · C5

- [An automated high-resolution screening platform identifies regulators of anchor cell invasion in C. elegans](https://doi.org/10.1126/sciadv.aef6546) - Berger et al., *Science Advances* 2026 `T2-adjacent` `peer-reviewed` · also filed under `C0`<br>
  *微流控高通量成像 + RNAi 筛选 + 神经网络表型评分的一体化平台（逾 4 万只个体、亚细胞分辨率、41/52 已知基因召回）；虽以幼虫期 anchor cell 侵袭为模型，其「扰动×高通量成像×自动评分」管线可直接迁移到胚胎扰动筛选研究。*
- [Learning Perturbation Effects Through Contrastive Alignment of Multimodal Biological Embeddings](https://doi.org/10.64898/2026.06.23.734145) - Long et al., *bioRxiv* 2026 `T3-transfer` `preprint` · also filed under `C8`<br>
  *多模态扰动图谱定义细胞形态表型的分辨率极限；扰动-形态表型分析规模化的方法参照。*
- [Robust spatiotemporal organization of mitotic events in mechanically perturbed C. elegans embryos](https://doi.org/10.1016/j.bpj.2024.03.041) - Borne et al., *Biophysical Journal* 2025 `T1-core` `peer-reviewed` · also filed under `C2`<br>
  *不破卵壳机械压缩早期胚胎后，细胞分裂时序与细胞定位仍高度稳健；机械扰动下发育程序稳健性的直接定量证据。*
- [Worm Perturb-Seq: massively parallel whole-animal RNAi and RNA-seq](https://doi.org/10.1038/s41467-025-60154-0) - Zhang et al., *Nature Communications* 2025 `T2-adjacent` `peer-reviewed` · also filed under `C4`<br>
  *Worm Perturb-Seq：整动物层面大规模并行 RNAi + RNA-seq；扰动-转录组表型的高通量范式（非胚胎特异但体系直接适用）。*
- [Automated profiling of gene function during embryonic development](https://doi.org/10.1016/j.cell.2024.04.012) - Green et al., *Cell* 2024 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *500 个基因敲低的 4D 成像自动表型剖析与 PhenoBank 资源；自动化扰动表型组学的规模化样板。*
- [The Regulatory Landscape of Lineage Differentiation in a Metazoan Embryo](https://doi.org/10.1016/j.devcel.2015.07.014) - Du et al., *Developmental Cell* 2015 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *系统 RNAi 绘制谱系分化的调控景观：命运沟渠化、二元命运开关与多尺度分化模型；扰动-表型系统分析的奠基资源。*

*See the [category page](categories/C5-perturbation-causal.md) for 3 cross-listed entries filed primarily elsewhere.*

## Fate Specification & Lineage Biology

**命运决定与谱系生物学** · C6

- [Distinct roles for partially redundant transcription factors in Caenorhabditis elegans mesoderm lineage development](https://doi.org/10.64898/2026.09.01.748736) - Gan et al., *bioRxiv* 2026 `T1-core` `preprint` · also filed under `C4`<br>
  *部分冗余转录因子在中胚层谱系发育中的差异化功能拆解；命运决定冗余性与补偿机制的精细证据。*
- [Spatiotemporal transcriptomics reveals the evolutionary history of the endoderm germ layer](https://doi.org/10.1038/nature13996) - Hashimshony et al., *Nature* 2015 `T1-core` `peer-reviewed` · also filed under `C4`<br>
  *时空转录组揭示内胚层胚层的演化历史；胚层起源问题的谱系-分子证据（含线虫数据）。*
- [Cell fate specification in the C. elegans embryo](https://doi.org/10.1002/dvdy.22233) - Maduro, *Developmental Dynamics* 2010 `T1-core` `peer-reviewed` · also filed under `C9`<br>
  *命运决定机制的权威综述；母源因子、非对称分裂与 Wnt/Notch 信号框架是分子调控与谱系生物学条目的知识底座。*
- [The embryonic cell lineage of the nematode Caenorhabditis elegans](https://doi.org/10.1016/0012-1606(83)90201-4) - Sulston et al., *Developmental Biology* 1983 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *invariant lineage 的奠基工作；所有谱系表示与重建方法的基准真值。*

*See the [category page](categories/C6-fate-lineage-biology.md) for 13 cross-listed entries filed primarily elsewhere.*

## Methods Transfer

**方法迁移** · C7

- [On Growth and Form, and Function: Reusable Regulatory Handles Control Phenotypic Variation](https://arxiv.org/abs/2609.29755) - Hartl et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  *用 LoRA 低秩调制预训练神经胞元自动机（NCA）的发育程序，约 2.5 万个适配器中识别出可复用、可组合的低维表型变异控制方向；对「扰动→形态分布」的计算建模有方法学启发，但目前仅是 2D 玩具系统，迁移价值待验证。*
- [Rethinking Class Imbalance for Single-Cell Foundation Models: A Systematic Benchmark Across Architectures and Long-Tail Loss Functions](https://arxiv.org/abs/2609.23325) - Dong et al., *arXiv* 2026 `T3-transfer` `preprint` · also filed under `C8`<br>
  *单细胞基础模型稀有类别失效的系统基准（3 架构 × 3 数据集 × 6 损失 × 162 组受控训练）：稀有类失效在嵌入几何层面已注定，损失函数只能挽救其中一部分；对胚胎稀有细胞状态分类的训练与评估有直接警示价值。*
- [Stochastic Flow Map for Count Data](https://arxiv.org/abs/2609.23290) - Wei, *arXiv* 2026 `T3-transfer` `preprint`<br>
  *直接在计数空间学习有限时间随机转移（Poisson 生 / Binomial 灭）的少步生成模型，应用于单细胞药物扰动响应预测；其「有限时间转移算子」形式与发育动力学的随机转移建模同构，值得借鉴；未在胚胎数据上验证。*

*See the [category page](categories/C7-methods-transfer.md) for 11 cross-listed entries filed primarily elsewhere.*

## Datasets, Benchmarks & Software

**数据集、基准与软件** · C8

- [DynamicAtlas: a morphodynamic atlas for Drosophila development](https://doi.org/10.1038/s41592-025-02897-8) - Lefebvre et al., *Nature Methods* 2026 `T3-transfer` `peer-reviewed` · also filed under `C3`<br>
  *DynamicAtlas：果蝇发育的形态动力学图谱；活体动态形态图谱资源的代表。*
- [Whole-embryo spatial transcriptomics at subcellular resolution from gastrulation to organogenesis](https://doi.org/10.1126/science.adt3439) - Wan et al., *Science* 2026 `T3-transfer` `peer-reviewed` · also filed under `C4`<br>
  *全胚胎亚细胞分辨空间转录组（斑马鱼，原肠到器官发生）；空间组学图谱技术的标杆。*
- [A full-body transcription factor expression atlas with completely resolved cell identities in C. elegans](https://doi.org/10.1038/s41467-023-42677-6) - Li et al., *Nature Communications* 2024 `T2-adjacent` `peer-reviewed` · also filed under `C4`<br>
  *全身转录因子表达图谱（L1 幼虫）与 RAPCAT 自动细胞身份标注工具；细胞身份自动标注方法对胚胎数据同样适用。*
- [TedSim: temporal dynamics simulation of single-cell RNA sequencing data and cell division history](https://doi.org/10.1093/nar/gkac235) - Pan et al., *Nucleic Acids Research* 2022 `T3-transfer` `peer-reviewed` · also filed under `C4`<br>
  *TedSim：scRNA 时序动力学与细胞分裂历史联合模拟器；谱系-转录组联合数据方法的基准测试工具。*
- [Digital development: a database of cell lineage differentiation inC. eleganswith lineage phenotypes, cell-specific gene functions and a multiscale model](https://doi.org/10.1093/nar/gkv1119) - Santella et al., *Nucleic Acids Research* 2016 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *Digital Development 数据库：谱系分化表型、细胞特异基因功能与多尺度模型；扰动表型的公开数据资源。*

*See the [category page](categories/C8-datasets-benchmarks-software.md) for 16 cross-listed entries filed primarily elsewhere.*

## Reviews & Perspectives

**综述与观点** · C9

- [Cellular Processes and Forces Shaping the Embryo: Lessons from C. elegans](https://doi.org/10.3390/cells15070645) - Labouesse et al., *Cells* 2026 `T1-core` `peer-reviewed` · also filed under `C3`<br>
  *塑造胚胎的细胞过程与力：以线虫为视角的综述；胚胎力学的线虫专门评述。*
- [Decoding the origins of cellular self-organization for engineered biology](https://doi.org/10.1038/s41587-026-03161-w) - Chen et al., *Nature Biotechnology* 2026 `T3-transfer` `peer-reviewed`<br>
  *解码细胞自组织起源的观点文章；自组织物理约束与工程化生物的视角。*
- [Embryo models as experiments in self-organization: The logic of productive failure](https://doi.org/10.1016/j.devcel.2026.06.009) - Zernicka-Goetz et al., *Developmental Cell* 2026 `T3-transfer` `peer-reviewed`<br>
  *胚胎模型作为自组织实验：「有效失败」的逻辑；干细胞胚胎模型的方法论观点。*
- [Towards predictive virtual embryos with genomics and AI](https://doi.org/10.1038/s41592-026-03055-4) - Cao et al., *Nature Methods* 2026 `T3-transfer` `peer-reviewed`<br>
  *迈向基因组学与 AI 结合的预测性虚拟胚胎（评论）；虚拟胚胎方向的路线图式观点。*
- [Mechanical regulation of early vertebrate embryogenesis](https://doi.org/10.1038/s41580-021-00424-z) - Valet et al., *Nature Reviews Molecular Cell Biology* 2022 `T3-transfer` `peer-reviewed` · also filed under `C3`<br>
  *脊椎动物胚胎发生机械调控的权威综述；力学-图式形成领域的系统性评述。*
- [Self-Organization in Pattern Formation](https://doi.org/10.1016/j.devcel.2019.05.019) - Schweisguth et al., *Developmental Cell* 2019 `T3-transfer` `peer-reviewed`<br>
  *图式形成中自组织的综述；从对称性破缺到组织模式的自组织概念框架。*

*See the [category page](categories/C9-reviews-perspectives.md) for 1 cross-listed entry filed primarily elsewhere.*
