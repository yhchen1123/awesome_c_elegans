# C0: Measurement & Tracking（测量与追踪）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: 显微图像到谱系分辨细胞对象：nucleus/membrane segmentation、cell tracking、division detection、lineage reconstruction、tracking benchmark

[← Back to README](../README.md)

## Papers (12)

- **[An automated high-resolution screening platform identifies regulators of anchor cell invasion in C. elegans](https://doi.org/10.1126/sciadv.aef6546)** — Berger et al., *Science Advances* 2026 `T2-adjacent` `peer-reviewed`<br>
  微流控高通量成像 + RNAi 筛选 + 神经网络表型评分的一体化平台（逾 4 万只个体、亚细胞分辨率、41/52 已知基因召回）；虽以幼虫期 anchor cell 侵袭为模型，其「扰动×高通量成像×自动评分」管线可直接迁移到胚胎扰动筛选研究。
- **[Cell tracking with accurate error prediction](https://doi.org/10.1038/s41592-025-02845-6)** — Betjes et al., *Nature Methods* 2025 `T2-adjacent` `peer-reviewed` `uncertainty-quantified`<br>
  OrganoidTracker 2.0：为追踪结果的每一步给出误差概率（类 P 值），支持仅保留高置信片段的全自动分析；直接回应追踪误差沿谱系传播的问题，是不确定性量化硬标准的示范。
- **[CELLECT: contrastive embedding learning for large-scale efficient cell tracking](https://doi.org/10.1038/s41592-025-02886-x)** — Zhou et al., *Nature Methods* 2025 `T2-adjacent` `peer-reviewed`<br>
  CELLECT：对比嵌入学习实现大规模高效细胞追踪；嵌入表示驱动的追踪范式，与细胞表示学习方法天然衔接。
- **[EmbSAM: cell boundary localization and Segment Anything Model for fast images of developing embryos](https://doi.org/10.1038/s42003-025-09220-3)** — Guan et al., *Communications Biology* 2025 `T1-core` `peer-reviewed`<br>
  EmbSAM：面向发育胚胎低信噪比膜图像的 SAM 分割管线（边界定位+Segment Anything）；膜分割的实用工具。
- **[LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532)** — Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint`<br>
  corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。
- **[Sparse Annotation is Sufficient for Bootstrapping Dense Neuron Segmentation](https://doi.org/10.1101/2024.06.14.599135)** — Manor et al., *bioRxiv* 2024 `T3-transfer` `preprint`<br>
  从稀疏 2D 标注自举稠密 3D 分割的通用方法；降低三维标注成本，对胚胎膜分割标注有直接参考价值。
- **[WaveOrder: A differentiable wave-optical framework for scalable biological microscopy with diverse modalities](https://arxiv.org/abs/2412.09775)** — Chandler et al., *arXiv* 2024 `T3-transfer` `preprint`<br>
  WaveOrder：可微波动光学显微框架，统一多种成像模态的正演模型；显微成像物理可微化的参照。
- **[A high-content imaging approach to profile C. elegans embryonic development](https://doi.org/10.1242/dev.174029)** — Wang et al., *Development* 2019 `T1-core` `peer-reviewed`<br>
  高内涵成像剖析线虫胚胎发育，自动提取形态与分裂特征；胚胎表型特征提取管线的代表工作。
- **[In Toto Imaging and Reconstruction of Post-Implantation Mouse Development at the Single-Cell Level](https://doi.org/10.1016/j.cell.2018.09.031)** — McDole et al., *Cell* 2018 `T3-transfer` `peer-reviewed`<br>
  小鼠着床后发育的 in toto 光片成像与单细胞重建（含多胚胎统计动态图谱）；全胚胎动态图谱的范式性工作。
- **[Tissue cartography: compressing bio-image data by dimensional reduction](https://doi.org/10.1038/nmeth.3648)** — Heemskerk et al., *Nature Methods* 2015 `T3-transfer` `peer-reviewed`<br>
  组织制图学通用框架：曲面到平面映射的畸变控制与无缝导航；胚胎表面成像数据降维的方法参照。
- **[Systematic quantification of developmental phenotypes at single-cell resolution during embryogenesis](https://doi.org/10.1242/dev.096040)** — Moore et al., *Development* 2013 `T1-core` `peer-reviewed`<br>
  单细胞分辨的发育表型系统量化（自动图像分析提取数十种测量）；线虫胚胎表型组学的早期方法。
- **[Automated cell lineage tracing in Caenorhabditis elegans](https://doi.org/10.1073/pnas.0511111103)** — Bao et al., *Proceedings of the National Academy of Sciences* 2006 `T1-core` `peer-reviewed`<br>
  StarryNite/AceTree 自动谱系追踪的开山之作；后续测量管线的基线与数据兼容层，其 tracking error 沿长轨迹传播的问题至今仍是改进目标。

## Related categories

- [C1: Cell & Embryo Representation](C1-cell-representation.md) — 细胞与胚胎表示
- [C8: Datasets, Benchmarks & Software](C8-datasets-benchmarks-software.md) — 数据集、基准与软件
