<h1>Awesome <i>C. elegans</i> Embryogenesis</h1>

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![papers](https://img.shields.io/badge/papers-20-blue) ![last update](https://img.shields.io/badge/last_update-2026--09--28-green)

> AI-curated, human-audited multidisciplinary literature tracking for *C. elegans* embryogenesis research — from lineage-resolved atlases and live imaging to mechanics, molecular regulation, and dynamical modeling. Updated weekly by automation; every update lands as a reviewed PR.

This repository is maintained by an **AI-search + human-PR-audit** loop: a weekly GitHub Actions run queries Europe PMC (PubMed + bioRxiv/medRxiv) and arXiv for new literature, an LLM classifies candidates into the taxonomy below and writes Chinese relevance notes, and all changes are delivered as a pull request for human review — nothing is pushed to `main` directly. A monthly digest summarizes the month's additions by theme and watches for retractions. Each category also has a dedicated page under `categories/` with the full cross-listed entries. See `CONTRIBUTING.md` for inclusion criteria and `docs/DEVELOPMENT.md` for operations. License: CC0-1.0 (see `LICENSE`).

> ⚠️ **C7 soft-cap warning:** T3-transfer entries make up 60% of Methods Transfer (3/5), exceeding the 30% soft cap. Maintainers should consider tightening arXiv queries or triaging low-relevance entries.

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

- [LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532) - Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint` · also filed under `C7`<br>
  *corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。*
- [Automated cell lineage tracing in Caenorhabditis elegans](https://doi.org/10.1073/pnas.0511111103) - Bao et al., *Proceedings of the National Academy of Sciences* 2006 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *StarryNite/AceTree 自动谱系追踪的开山之作；后续测量管线的基线与数据兼容层，其 tracking error 沿长轨迹传播的问题至今仍是改进目标。*

*See the [category page](categories/C0-measurement-tracking.md) for 1 cross-listed entry filed primarily elsewhere.*

## Cell & Embryo Representation

**细胞与胚胎表示** · C1

No entries yet.

## WT Developmental Dynamics

**野生型发育动力学** · C2

- [A kinematic equation for the morphogenetic reproducibility of an animal](https://doi.org/10.65215/ltspreprints.2026.04.04.000174) - Wang et al., *LTS Preprints* 2026 `T1-core` `emerging-evidence`<br>
  *⚠️ emerging evidence: 形态发生可重复性的运动学方程；与发育稳健性/可重复性定量研究直接相关。**注意：按本仓库证据规则视为 emerging evidence，未经同行评审与独立验证前不得作为既定共识引用。***
- [Systems Properties and Spatiotemporal Regulation of Cell Position Variability during Embryogenesis](https://doi.org/10.1016/j.celrep.2018.12.052) - Li et al., *Cell Reports* 2019 `T1-core` `peer-reviewed`<br>
  *细胞位置变异与谱系/对称性/接触相关且存在系统性变异压缩；发育稳健性（canalization）定量研究的重要实证基础。*

## Morphology & Mechanics

**形态与力学** · C3

- [Nematic structures contribute to robust zygotic polarization in C. elegans](https://doi.org/10.1371/journal.pcbi.1014792) - Vanslambrouck et al., *PLOS Computational Biology* 2026 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *建立线虫合子极化的 3D 力学模型（皮层收缩丝网络），复现 cortical flow、表面褶皱与张力各向异性，提出密度依赖收缩的机械负反馈机制；形态-力学耦合建模在单细胞阶段的直接参照，与 FIDES 力推断工作出自同一团队。*
- [Cell lineage-resolved embryonic morphological map reveals signaling associated with cell fate and size asymmetry](https://doi.org/10.1038/s41467-025-58878-0) - Guan et al., *Nature Communications* 2025 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *CMap 谱系分辨形态图谱：位置、体积、表面积、接触面积的全胚胎时空图谱；细胞表示与形态力学研究的核心几何数据源。*
- [Image-based force inference by biomechanical simulation](https://doi.org/10.1371/journal.pcbi.1012629) - Vanslambrouck et al., *PLOS Computational Biology* 2024 `T2-adjacent` `peer-reviewed`<br>
  *FIDES 生物力学仿真力推断；为「形态约束力学但不等同绝对 force」的可识别性讨论提供方法样本。*
- [Embryo mechanics cartography: inference of 3D force atlases from fluorescence microscopy](https://doi.org/10.1038/s41592-023-02084-7) - Ichbiah et al., *Nature Methods* 2023 `T1-core` `peer-reviewed`<br>
  *从荧光显微图像反推 3D 力学图谱；inverse mechanics（由形态反推力学）路线的关键方法参照。*
- [Computable early Caenorhabditis elegans embryo with a phase field model](https://doi.org/10.1371/journal.pcbi.1009755) - Kuang et al., *PLOS Computational Biology* 2022 `T1-core` `peer-reviewed`<br>
  *早期胚胎的可计算 phase-field forward simulator；可计算胚胎形态发生模拟器方向的先行者，也是「力不可唯一识别」问题的实例。*

## Molecular Regulation & Coupling

**分子调控与耦合** · C4

- [Decoding cell division history and lineage-resolved phenotypic patterns from single-cell barcode and transcriptomic data](https://doi.org/10.1101/gr.281734.125) - Yu et al., *Genome Research* 2026 `T2-adjacent` `peer-reviewed` · also filed under `C7`<br>
  *FateScape 框架联合谱系条形码与转录组推断细胞分裂树拓扑并刻画深度分辨的表型分布，在线虫胚胎数据上验证了谱系拓扑重建；为「谱系×分子状态」联合分析提供方法参照，也是 destructive assay 限制下的替代观测路线。*
- [Lineage-resolved analysis of embryonic gene expression evolution in C. elegans and C. briggsae](https://doi.org/10.1126/science.adu8249) - Large et al., *Science* 2025 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *跨物种谱系分辨表达演化；为 lineage 与 transcriptome 非恒定关系及远缘谱系分子收敛提供证据。*
- [Gene regulatory patterning codes in early cell fate specification of the C. elegans embryo](https://doi.org/10.7554/elife.87099) - Cole et al., *eLife* 2024 `T1-core` `peer-reviewed` · also filed under `C6`<br>
  *早期命运决定的调控 patterning code；为「当前状态 → 命运决策 → 新调控状态」的转移规律研究提供分子层证据。*
- [Spatiotemporal analysis of mRNA-protein relationships enhances transcriptome-based developmental inference](https://doi.org/10.1016/j.celrep.2024.113928) - Fan et al., *Cell Reports* 2024 `T1-core` `peer-reviewed`<br>
  *mRNA 与蛋白非同步、非一一对应的直接证据；为发育推断中的 mRNA-蛋白时间延迟建模提供实验依据。*
- [A lineage-resolved molecular atlas of C. elegans embryogenesis at single-cell resolution](https://doi.org/10.1126/science.aax1971) - Packer et al., *Science* 2019 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *谱系分辨单细胞转录组图谱的奠基数据集；谱系-分子联合分析的主要数据来源，destructive assay 导致的纵向轨迹缺失是此类数据的核心观测限制。*

## Perturbation & Causal Inference

**扰动与因果推断** · C5

- [An automated high-resolution screening platform identifies regulators of anchor cell invasion in C. elegans](https://doi.org/10.1126/sciadv.aef6546) - Berger et al., *Science Advances* 2026 `T2-adjacent` `peer-reviewed` · also filed under `C0`<br>
  *微流控高通量成像 + RNAi 筛选 + 神经网络表型评分的一体化平台（逾 4 万只个体、亚细胞分辨率、41/52 已知基因召回）；虽以幼虫期 anchor cell 侵袭为模型，其「扰动×高通量成像×自动评分」管线可直接迁移到胚胎扰动筛选研究。*

## Fate Specification & Lineage Biology

**命运决定与谱系生物学** · C6

- [Cell fate specification in the C. elegans embryo](https://doi.org/10.1002/dvdy.22233) - Maduro, *Developmental Dynamics* 2010 `T1-core` `peer-reviewed` · also filed under `C9`<br>
  *命运决定机制的权威综述；母源因子、非对称分裂与 Wnt/Notch 信号框架是分子调控与谱系生物学条目的知识底座。*
- [The embryonic cell lineage of the nematode Caenorhabditis elegans](https://doi.org/10.1016/0012-1606(83)90201-4) - Sulston et al., *Developmental Biology* 1983 `T1-core` `peer-reviewed` · also filed under `C8`<br>
  *invariant lineage 的奠基工作；所有谱系表示与重建方法的基准真值。*

*See the [category page](categories/C6-fate-lineage-biology.md) for 3 cross-listed entries filed primarily elsewhere.*

## Methods Transfer

**方法迁移** · C7

- [On Growth and Form, and Function: Reusable Regulatory Handles Control Phenotypic Variation](https://arxiv.org/abs/2609.29755) - Hartl et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  *用 LoRA 低秩调制预训练神经胞元自动机（NCA）的发育程序，约 2.5 万个适配器中识别出可复用、可组合的低维表型变异控制方向；对「扰动→形态分布」的计算建模有方法学启发，但目前仅是 2D 玩具系统，迁移价值待验证。*
- [Rethinking Class Imbalance for Single-Cell Foundation Models: A Systematic Benchmark Across Architectures and Long-Tail Loss Functions](https://arxiv.org/abs/2609.23325) - Dong et al., *arXiv* 2026 `T3-transfer` `preprint` · also filed under `C8`<br>
  *单细胞基础模型稀有类别失效的系统基准（3 架构 × 3 数据集 × 6 损失 × 162 组受控训练）：稀有类失效在嵌入几何层面已注定，损失函数只能挽救其中一部分；对胚胎稀有细胞状态分类的训练与评估有直接警示价值。*
- [Stochastic Flow Map for Count Data](https://arxiv.org/abs/2609.23290) - Wei, *arXiv* 2026 `T3-transfer` `preprint`<br>
  *直接在计数空间学习有限时间随机转移（Poisson 生 / Binomial 灭）的少步生成模型，应用于单细胞药物扰动响应预测；其「有限时间转移算子」形式与发育动力学的随机转移建模同构，值得借鉴；未在胚胎数据上验证。*

*See the [category page](categories/C7-methods-transfer.md) for 2 cross-listed entries filed primarily elsewhere.*

## Datasets, Benchmarks & Software

**数据集、基准与软件** · C8

No entries yet.

*See the [category page](categories/C8-datasets-benchmarks-software.md) for 5 cross-listed entries filed primarily elsewhere.*

## Reviews & Perspectives

**综述与观点** · C9

No entries yet.

*See the [category page](categories/C9-reviews-perspectives.md) for 1 cross-listed entry filed primarily elsewhere.*
