# C7: Methods Transfer（方法迁移）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: 非线虫系统但方法可迁移：graph neural dynamics、neural ODE/SDE、物理信息机器学习、单细胞/发育基础模型。占比软上限 30%

[← Back to README](../README.md)

## Papers (25)

- **[Decoding cell division history and lineage-resolved phenotypic patterns from single-cell barcode and transcriptomic data](https://doi.org/10.1101/gr.281734.125)** — Yu et al., *Genome Research* 2026 `T2-adjacent` `peer-reviewed`<br>
  FateScape 框架联合谱系条形码与转录组推断细胞分裂树拓扑并刻画深度分辨的表型分布，在线虫胚胎数据上验证了谱系拓扑重建；为「谱系×分子状态」联合分析提供方法参照，也是 destructive assay 限制下的替代观测路线。
- **[MultiCell: geometric learning in multicellular development](https://doi.org/10.1038/s41592-025-02983-x)** — Yang et al., *Nature Methods* 2026 `T3-transfer` `peer-reviewed`<br>
  MultiCell：几何深度学习预测多细胞发育中每个细胞的行为；几何归纳偏置用于发育建模的代表工作。
- **[On Growth and Form, and Function: Reusable Regulatory Handles Control Phenotypic Variation](https://arxiv.org/abs/2609.29755)** — Hartl et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  用 LoRA 低秩调制预训练神经胞元自动机（NCA）的发育程序，约 2.5 万个适配器中识别出可复用、可组合的低维表型变异控制方向；对「扰动→形态分布」的计算建模有方法学启发，但目前仅是 2D 玩具系统，迁移价值待验证。
- **[Quantifying the Single‐Cell Morphological Landscape of Cellular Transdifferentiation through Force Field Reconstruction](https://doi.org/10.1002/advs.202512325)** — Yu et al., *Advanced Science* 2026 `T3-transfer` `peer-reviewed`<br>
  从跨分化快照重建单细胞形态景观与力场（无细胞特异速度信息）；形态动力学重建方法可迁移至胚胎形态数据。
- **[Rethinking Class Imbalance for Single-Cell Foundation Models: A Systematic Benchmark Across Architectures and Long-Tail Loss Functions](https://arxiv.org/abs/2609.23325)** — Dong et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  单细胞基础模型稀有类别失效的系统基准（3 架构 × 3 数据集 × 6 损失 × 162 组受控训练）：稀有类失效在嵌入几何层面已注定，损失函数只能挽救其中一部分；对胚胎稀有细胞状态分类的训练与评估有直接警示价值。
- **[Stochastic Flow Map for Count Data](https://arxiv.org/abs/2609.23290)** — Wei, *arXiv* 2026 `T3-transfer` `preprint`<br>
  直接在计数空间学习有限时间随机转移（Poisson 生 / Binomial 灭）的少步生成模型，应用于单细胞药物扰动响应预测；其「有限时间转移算子」形式与发育动力学的随机转移建模同构，值得借鉴；未在胚胎数据上验证。
- **[VertAX: a differentiable vertex model for learning epithelial tissue mechanics](https://arxiv.org/abs/2604.06896)** — Pasqui et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  VertAX：可微顶点模型，以梯度优化学习上皮组织力学参数；可微组织力学模拟器路线的新成员。
- **[Wound-induced syncytia outpace mononucleate neighbors during Drosophila wound repair.](https://doi.org/10.7554/elife.92593)** — JS et al., *eLife* 2026 `T3-transfer` `peer-reviewed`<br>
  结合活体成像与组织流动性计算模型，发现伤口诱导的合胞体形成可加速上皮伤口闭合；其细胞融合与组织尺度力学建模思路对形态与力学（C3）及相关模拟方法具有迁移参考价值。
- **[Mapping Embryonic Mouse Lung Development Using Enhanced Spatial Transcriptomics.](https://doi.org/10.1002/advs.77678)** — P et al., *Advanced Science* 2026 `T3-transfer` `peer-reviewed`<br>
  优化 DBiT-seq 空间转录组流程绘制早期小鼠肺发育的空间图谱，平均转录本回收率较此前提升约两倍；空间组学方法对胚胎分子调控研究（C4）具有迁移参考价值。
- **[Real-Time Monitoring of Mass and Mechanical Properties in Single Cells and Multicellular Spheroids.](https://doi.org/10.1002/advs.77926)** — I et al., *Advanced Science* 2026 `T3-transfer` `peer-reviewed`<br>
  基于光热驱动微悬臂梁联用光学显微，实现单细胞与多细胞球体质量、形态及力学耗散（Q 因子）的毫秒级实时同步监测；为细胞与胚胎样系统的力学性质测量方法（C7/C3）提供新工具。
- **[CellMSA: Context Modeling for Single-Cell Representation Learning](https://arxiv.org/abs/2609.38908)** — Zhao et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  CellMSA 将蛋白质建模中多序列比对（MSA）的上下文归纳偏置引入单细胞转录组建模，跨批次检索相关细胞作为上下文学习基因对表示，在约 1.09 亿细胞语料上预训练；为单细胞表示学习提供新架构思路。
- **[CellSplat4D: PSF-Aware 4D Gaussian Splatting for Sparse Robotic Live-Cell Imaging](https://arxiv.org/abs/2610.04199)** — Tao et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  CellSplat4D 面向稀疏采样的机器人活细胞成像，用 PSF 感知的 4D 高斯泼溅重建任意缺失时间点的体积并维持细胞身份与分裂记录；对稀疏时序下的细胞追踪与谱系记录（C0）具有直接方法迁移价值。
- **[Generalizable single-cell perturbation response prediction using energy-guided flow matching](https://arxiv.org/abs/2610.02232)** — Wei et al., *arXiv* 2026 `T3-transfer` `preprint` `perturbation-holdout`<br>
  scEGFlow 用条件流匹配加能量引导预测单细胞扰动响应，无需重训练即可适配新扰动条件，并在未见扰动上整体留出评估；对扰动响应预测与跨条件泛化（C5/C7）具有参考价值。
- **[KoopCell: Koopman-Based Generative Model for Learning Single-Cell Dynamics from Distribution Snapshots](https://arxiv.org/abs/2609.33350)** — Lu et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  基于 Koopman-Mori-Zwanzig 理论从非配对分布快照学习单细胞群体动力学的生成框架，可外推训练时程之外并建模发育分支（非马尔可夫记忆嵌入）；对群体层面发育轨迹建模具有直接方法迁移价值。
- **[Simulation-Free Learning of Population Dynamics with Wasserstein Lagrangian Residuals](https://arxiv.org/abs/2610.03679)** — Sergeev et al., *arXiv* 2026 `T3-transfer` `preprint`<br>
  提出 Double-Stitch：免仿真的 Wasserstein 拉格朗日力学学习方法，从非配对快照重建并外推保守/周期型群体动力学，训练速度较仿真式方法提升 4-14 倍；为细胞群体动力学建模提供新的数学工具。
- **[CELLECT: contrastive embedding learning for large-scale efficient cell tracking](https://doi.org/10.1038/s41592-025-02886-x)** — Zhou et al., *Nature Methods* 2025 `T2-adjacent` `peer-reviewed`<br>
  CELLECT：对比嵌入学习实现大规模高效细胞追踪；嵌入表示驱动的追踪范式，与细胞表示学习方法天然衔接。
- **[Integrating representation learning, permutation, and optimization to detect lineage-related gene expression patterns](https://doi.org/10.1038/s41467-025-56388-7)** — Schlüter et al., *Nature Communications* 2025 `T3-transfer` `peer-reviewed`<br>
  PORCELAN：表示学习+置换检验+优化检测谱系相关基因表达模式；谱系条形码×表达联合分析的新方法。
- **[Interpretable representation learning for 3D multi-piece intracellular structures using point clouds](https://doi.org/10.1038/s41592-025-02729-9)** — Vasan et al., *Nature Methods* 2025 `T3-transfer` `peer-reviewed`<br>
  点云表示学习刻画 3D 胞内多部件结构且保持可解释；3D 生物结构表示学习的参照。
- **[LivecellX: Corrective Deep Learning for Object-Oriented Single-Cell Analysis in Live-Cell Imaging](https://doi.org/10.1101/2025.02.23.639532)** — Ni et al., *bioRxiv* 2025 `T2-adjacent` `preprint`<br>
  corrective deep learning 追踪框架；替代 StarryNite/AceTree 单点依赖、避免错误沿长轨迹累积的候选路线。
- **[RNA velocity in growing cells](https://doi.org/10.64898/2025.12.18.695252)** — Shah et al., *bioRxiv* 2025 `T3-transfer` `preprint`<br>
  指出 RNA velocity 因忽略细胞生长而产生根本误差；基于 scRNA 的轨迹推断方法学的重要警示。
- **[Sparse Annotation is Sufficient for Bootstrapping Dense Neuron Segmentation](https://doi.org/10.1101/2024.06.14.599135)** — Manor et al., *bioRxiv* 2024 `T3-transfer` `preprint`<br>
  从稀疏 2D 标注自举稠密 3D 分割的通用方法；降低三维标注成本，对胚胎膜分割标注有直接参考价值。
- **[WaveOrder: A differentiable wave-optical framework for scalable biological microscopy with diverse modalities](https://arxiv.org/abs/2412.09775)** — Chandler et al., *arXiv* 2024 `T3-transfer` `preprint`<br>
  WaveOrder：可微波动光学显微框架，统一多种成像模态的正演模型；显微成像物理可微化的参照。
- **[Morphodynamical cell state description via live-cell imaging trajectory embedding](https://doi.org/10.1038/s42003-023-04837-8)** — Copperman et al., *Communications Biology* 2023 `T3-transfer` `peer-reviewed`<br>
  活细胞成像轨迹嵌入的形态动力学细胞状态描述；以轨迹历史而非单帧特征表示细胞状态的方法。
- **[Hierarchical deep reinforcement learning reveals a modular mechanism of cell movement](https://doi.org/10.1038/s42256-021-00431-x)** — Wang et al., *Nature Machine Intelligence* 2022 `T1-core` `peer-reviewed`<br>
  层级深度强化学习揭示胚胎细胞运动的模块化机制；从轨迹数据反演运动策略的 RL 方法。
- **[A Whole-Cell Computational Model Predicts Phenotype from Genotype](https://doi.org/10.1016/j.cell.2012.05.044)** — Karr et al., *Cell* 2012 `T3-transfer` `peer-reviewed`<br>
  首个全细胞计算模型（M. genitalium）：28 个模块耦合并行推进、由基因型预测表型；全细胞/全胚胎尺度「多过程耦合模拟」的奠基范式。

## Related categories

- [C0: Measurement & Tracking](C0-measurement-tracking.md) — 测量与追踪
- [C1: Cell & Embryo Representation](C1-cell-representation.md) — 细胞与胚胎表示
