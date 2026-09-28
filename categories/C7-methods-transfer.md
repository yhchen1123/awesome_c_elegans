# C7: Methods Transfer（方法迁移）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: 非线虫系统但方法可迁移：graph neural dynamics、neural ODE/SDE、物理信息机器学习、单细胞/发育基础模型。占比软上限 30%

[← Back to README](../README.md)

## Papers (5)

- **[Decoding cell division history and lineage-resolved phenotypic patterns from single-cell barcode and transcriptomic data](https://doi.org/10.1101/gr.281734.125)** — Yu et al., *Genome Research* 2026 `T2-adjacent` `peer-reviewed`<br>
  FateScape 框架联合谱系条形码与转录组推断细胞分裂树拓扑并刻画深度分辨的表型分布，在线虫胚胎数据上验证了谱系拓扑重建；为「谱系×分子状态」联合分析提供方法参照，也是 destructive assay 限制下的替代观测路线。
- **[On Growth and Form, and Function: Reusable Regulatory Handles Control Phenotypic Variation](https://arxiv.org/abs/2609.29755)** — Hartl et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  用 LoRA 低秩调制预训练神经胞元自动机（NCA）的发育程序，约 2.5 万个适配器中识别出可复用、可组合的低维表型变异控制方向；对「扰动→形态分布」的计算建模有方法学启发，但目前仅是 2D 玩具系统，迁移价值待验证。
- **[Rethinking Class Imbalance for Single-Cell Foundation Models: A Systematic Benchmark Across Architectures and Long-Tail Loss Functions](https://arxiv.org/abs/2609.23325)** — Dong et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  单细胞基础模型稀有类别失效的系统基准（3 架构 × 3 数据集 × 6 损失 × 162 组受控训练）：稀有类失效在嵌入几何层面已注定，损失函数只能挽救其中一部分；对胚胎稀有细胞状态分类的训练与评估有直接警示价值。
- **[Stochastic Flow Map for Count Data](https://arxiv.org/abs/2609.23290)** — Wei, *arXiv* 2026 `T3-transfer` `preprint`<br>
  直接在计数空间学习有限时间随机转移（Poisson 生 / Binomial 灭）的少步生成模型，应用于单细胞药物扰动响应预测；其「有限时间转移算子」形式与发育动力学的随机转移建模同构，值得借鉴；未在胚胎数据上验证。
- **[LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532)** — Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint`<br>
  corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。

## Related categories

- [C0: Measurement & Tracking](C0-measurement-tracking.md) — 测量与追踪
- [C1: Cell & Embryo Representation](C1-cell-representation.md) — 细胞与胚胎表示
