# C3: Morphology & Mechanics（形态与力学）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: 3D 形态图谱、接触面积/曲率/tricellular junction、force inference（FIDES/foam/phase-field）、可微形态发生模拟器、eggshell confinement

[← Back to README](../README.md)

## Papers (5)

- **[Nematic structures contribute to robust zygotic polarization in C. elegans](https://doi.org/10.1371/journal.pcbi.1014792)** — Vanslambrouck et al., *PLOS Computational Biology* 2026 `T1-core` `peer-reviewed`<br>
  建立线虫合子极化的 3D 力学模型（皮层收缩丝网络），复现 cortical flow、表面褶皱与张力各向异性，提出密度依赖收缩的机械负反馈机制；形态-力学耦合建模在单细胞阶段的直接参照，与 FIDES 力推断工作出自同一团队。
- **[Cell lineage-resolved embryonic morphological map reveals signaling associated with cell fate and size asymmetry](https://doi.org/10.1038/s41467-025-58878-0)** — Guan et al., *Nature Communications* 2025 `T1-core` `peer-reviewed`<br>
  CMap 谱系分辨形态图谱：位置、体积、表面积、接触面积的全胚胎时空图谱；细胞表示与形态力学研究的核心几何数据源。
- **[Image-based force inference by biomechanical simulation](https://doi.org/10.1371/journal.pcbi.1012629)** — Vanslambrouck et al., *PLOS Computational Biology* 2024 `T2-adjacent` `peer-reviewed`<br>
  FIDES 生物力学仿真力推断；为「形态约束力学但不等同绝对 force」的可识别性讨论提供方法样本。
- **[Embryo mechanics cartography: inference of 3D force atlases from fluorescence microscopy](https://doi.org/10.1038/s41592-023-02084-7)** — Ichbiah et al., *Nature Methods* 2023 `T1-core` `peer-reviewed`<br>
  从荧光显微图像反推 3D 力学图谱；inverse mechanics（由形态反推力学）路线的关键方法参照。
- **[Computable early Caenorhabditis elegans embryo with a phase field model](https://doi.org/10.1371/journal.pcbi.1009755)** — Kuang et al., *PLOS Computational Biology* 2022 `T1-core` `peer-reviewed`<br>
  早期胚胎的可计算 phase-field forward simulator；可计算胚胎形态发生模拟器方向的先行者，也是「力不可唯一识别」问题的实例。

## Related categories

- [C2: WT Developmental Dynamics](C2-wt-dynamics.md) — 野生型发育动力学
- [C4: Molecular Regulation & Coupling](C4-molecular-regulation.md) — 分子调控与耦合
- [C5: Perturbation & Causal Inference](C5-perturbation-causal.md) — 扰动与因果推断
