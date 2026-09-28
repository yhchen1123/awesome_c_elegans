# C0: Measurement & Tracking（测量与追踪）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: 显微图像到谱系分辨细胞对象：nucleus/membrane segmentation、cell tracking、division detection、lineage reconstruction、tracking benchmark

[← Back to README](../README.md)

## Papers (3)

- **[An automated high-resolution screening platform identifies regulators of anchor cell invasion in C. elegans](https://doi.org/10.1126/sciadv.aef6546)** — Berger et al., *Science Advances* 2026 `T2-adjacent` `peer-reviewed`<br>
  微流控高通量成像 + RNAi 筛选 + 神经网络表型评分的一体化平台（逾 4 万只个体、亚细胞分辨率、41/52 已知基因召回）；虽以幼虫期 anchor cell 侵袭为模型，其「扰动×高通量成像×自动评分」管线可直接迁移到胚胎扰动筛选研究。
- **[LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532)** — Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint`<br>
  corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。
- **[Automated cell lineage tracing in Caenorhabditis elegans](https://doi.org/10.1073/pnas.0511111103)** — Bao et al., *Proceedings of the National Academy of Sciences* 2006 `T1-core` `peer-reviewed`<br>
  StarryNite/AceTree 自动谱系追踪的开山之作；后续测量管线的基线与数据兼容层，其 tracking error 沿长轨迹传播的问题至今仍是改进目标。

## Related categories

- [C1: Cell & Embryo Representation](C1-cell-representation.md) — 细胞与胚胎表示
- [C8: Datasets, Benchmarks & Software](C8-datasets-benchmarks-software.md) — 数据集、基准与软件
