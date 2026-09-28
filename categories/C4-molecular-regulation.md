# C4: Molecular Regulation & Coupling（分子调控与耦合）

<!-- Auto-generated from data/papers.json by scripts/render.py. Do not edit manually. -->

> **Scope**: lineage-resolved scRNA、TF reporter atlas、RNA-protein 时滞、Wnt/Notch 信号、基因调控网络、分子-力学耦合

[← Back to README](../README.md)

## Papers (24)

- **[Decoding cell division history and lineage-resolved phenotypic patterns from single-cell barcode and transcriptomic data](https://doi.org/10.1101/gr.281734.125)** — Yu et al., *Genome Research* 2026 `T2-adjacent` `peer-reviewed`<br>
  FateScape 框架联合谱系条形码与转录组推断细胞分裂树拓扑并刻画深度分辨的表型分布，在线虫胚胎数据上验证了谱系拓扑重建；为「谱系×分子状态」联合分析提供方法参照，也是 destructive assay 限制下的替代观测路线。
- **[Distinct roles for partially redundant transcription factors in Caenorhabditis elegans mesoderm lineage development](https://doi.org/10.64898/2026.09.01.748736)** — Gan et al., *bioRxiv* 2026 `T1-core` `preprint`<br>
  部分冗余转录因子在中胚层谱系发育中的差异化功能拆解；命运决定冗余性与补偿机制的精细证据。
- **[PASTRI: Resolving Stage-Specific Cell-State Dynamics from Annotated Cell Lineage Trees](https://doi.org/10.64898/2026.08.16.745065)** — Yang et al., *bioRxiv* 2026 `T1-core` `preprint`<br>
  PASTRI：从带末端状态标注的谱系树推断阶段特异的细胞状态转移速率，在线虫胚胎谱系上验证；利用不同谱系距离绕过动力学随发育变化的问题。
- **[Whole-embryo spatial transcriptomics at subcellular resolution from gastrulation to organogenesis](https://doi.org/10.1126/science.adt3439)** — Wan et al., *Science* 2026 `T3-transfer` `peer-reviewed`<br>
  全胚胎亚细胞分辨空间转录组（斑马鱼，原肠到器官发生）；空间组学图谱技术的标杆。
- **[Integrating representation learning, permutation, and optimization to detect lineage-related gene expression patterns](https://doi.org/10.1038/s41467-025-56388-7)** — Schlüter et al., *Nature Communications* 2025 `T3-transfer` `peer-reviewed`<br>
  PORCELAN：表示学习+置换检验+优化检测谱系相关基因表达模式；谱系条形码×表达联合分析的新方法。
- **[Lineage-resolved analysis of embryonic gene expression evolution in C. elegans and C. briggsae](https://doi.org/10.1126/science.adu8249)** — Large et al., *Science* 2025 `T1-core` `peer-reviewed`<br>
  跨物种谱系分辨表达演化；为 lineage 与 transcriptome 非恒定关系及远缘谱系分子收敛提供证据。
- **[RNA velocity in growing cells](https://doi.org/10.64898/2025.12.18.695252)** — Shah et al., *bioRxiv* 2025 `T3-transfer` `preprint`<br>
  指出 RNA velocity 因忽略细胞生长而产生根本误差；基于 scRNA 的轨迹推断方法学的重要警示。
- **[Worm Perturb-Seq: massively parallel whole-animal RNAi and RNA-seq](https://doi.org/10.1038/s41467-025-60154-0)** — Zhang et al., *Nature Communications* 2025 `T2-adjacent` `peer-reviewed`<br>
  Worm Perturb-Seq：整动物层面大规模并行 RNAi + RNA-seq；扰动-转录组表型的高通量范式（非胚胎特异但体系直接适用）。
- **[A full-body transcription factor expression atlas with completely resolved cell identities in C. elegans](https://doi.org/10.1038/s41467-023-42677-6)** — Li et al., *Nature Communications* 2024 `T2-adjacent` `peer-reviewed`<br>
  全身转录因子表达图谱（L1 幼虫）与 RAPCAT 自动细胞身份标注工具；细胞身份自动标注方法对胚胎数据同样适用。
- **[A spatiotemporally resolved atlas of mRNA decay in the C. elegans embryo reveals differential regulation of mRNA stability across stages and cell types](https://doi.org/10.1101/gr.278980.124)** — Peng et al., *Genome Research* 2024 `T1-core` `peer-reviewed`<br>
  胚胎 mRNA 降解的时空图谱：mRNA 稳定性按发育阶段与细胞类型差异化调控；表达动力学中降解维度的资源。
- **[Gene regulatory patterning codes in early cell fate specification of the C. elegans embryo](https://doi.org/10.7554/elife.87099)** — Cole et al., *eLife* 2024 `T1-core` `peer-reviewed`<br>
  早期命运决定的调控 patterning code；为「当前状态 → 命运决策 → 新调控状态」的转移规律研究提供分子层证据。
- **[Spatiotemporal analysis of mRNA-protein relationships enhances transcriptome-based developmental inference](https://doi.org/10.1016/j.celrep.2024.113928)** — Fan et al., *Cell Reports* 2024 `T1-core` `peer-reviewed`<br>
  mRNA 与蛋白非同步、非一一对应的直接证据；为发育推断中的 mRNA-蛋白时间延迟建模提供实验依据。
- **[Transcript accumulation rates in the early Caenorhabditis elegans embryo](https://doi.org/10.1126/sciadv.adi1270)** — Sivaramakrishnan et al., *Science Advances* 2023 `T1-core` `peer-reviewed`<br>
  基因组尺度估计合子 mRNA 积累速率（scRNA-seq + 单分子成像校准）；快速转录如何支撑快速命运决定的定量图景。
- **[TedSim: temporal dynamics simulation of single-cell RNA sequencing data and cell division history](https://doi.org/10.1093/nar/gkac235)** — Pan et al., *Nucleic Acids Research* 2022 `T3-transfer` `peer-reviewed`<br>
  TedSim：scRNA 时序动力学与细胞分裂历史联合模拟器；谱系-转录组联合数据方法的基准测试工具。
- **[A 4D single-cell protein atlas of transcription factors delineates spatiotemporal patterning during embryogenesis](https://doi.org/10.1038/s41592-021-01216-1)** — Ma et al., *Nature Methods* 2021 `T1-core` `peer-reviewed`<br>
  转录因子蛋白的 4D（时空+谱系）表达图谱；蛋白层表达动力学的核心资源。
- **[Single‐cell dynamics of chromatin activity during cell lineage differentiation in Caenorhabditis elegans embryos](https://doi.org/10.15252/msb.202010075)** — Zhao et al., *Molecular Systems Biology* 2021 `T1-core` `peer-reviewed`<br>
  利用位置效应推断早期胚胎每个谱系细胞的染色质活性景观：染色质状态区分细胞状态并随谱系分化；表观层状态-命运关联的系统证据。
- **[A lineage-resolved molecular atlas of C. elegans embryogenesis at single-cell resolution](https://doi.org/10.1126/science.aax1971)** — Packer et al., *Science* 2019 `T1-core` `peer-reviewed`<br>
  谱系分辨单细胞转录组图谱的奠基数据集；谱系-分子联合分析的主要数据来源，destructive assay 导致的纵向轨迹缺失是此类数据的核心观测限制。
- **[Homeostasis of protein and mRNA concentrations in growing cells](https://doi.org/10.1038/s41467-018-06714-z)** — Lin et al., *Nature Communications* 2018 `T3-transfer` `peer-reviewed`<br>
  生长细胞中蛋白与 mRNA 浓度稳态的极小模型（聚合酶/核糖体限制）；为表达动力学与剂量效应建模提供理论基线。
- **[A Transcriptional Lineage of the Early C. elegans Embryo](https://doi.org/10.1016/j.devcel.2016.07.025)** — Tintori et al., *Developmental Cell* 2016 `T1-core` `peer-reviewed`<br>
  16 细胞期前每个胚胎细胞的 RNA-seq 转录谱系；细胞级合子基因组激活图谱的奠基数据集。
- **[Mapping and analysis of Caenorhabditis elegans transcription factor sequence specificities](https://doi.org/10.7554/elife.06967)** — Narasimhan et al., *eLife* 2015 `T1-core` `peer-reviewed`<br>
  线虫转录因子序列特异性的系统图谱；TF-DNA 特异性资源，支撑调控 motif 层分析。
- **[Spatiotemporal transcriptomics reveals the evolutionary history of the endoderm germ layer](https://doi.org/10.1038/nature13996)** — Hashimshony et al., *Nature* 2015 `T1-core` `peer-reviewed`<br>
  时空转录组揭示内胚层胚层的演化历史；胚层起源问题的谱系-分子证据（含线虫数据）。
- **[De Novo Inference of Systems-Level Mechanistic Models of Development from Live-Imaging-Based Phenotype Analysis](https://doi.org/10.1016/j.cell.2013.11.046)** — Du et al., *Cell* 2014 `T1-core` `peer-reviewed`<br>
  从活成像表型数据自动推断系统级机制模型（谱系追踪+组织特异表达组合）；数据驱动机制推断的开创性工作。
- **[Regulatory analysis of the C. elegans genome with spatiotemporal resolution](https://doi.org/10.1038/nature13497)** — Araya et al., *Nature* 2014 `T1-core` `peer-reviewed`<br>
  线虫基因组的时空分辨调控分析（转录因子结合图谱）；调控结合的时空资源。
- **[Multidimensional regulation of gene expression in the C. elegans embryo](https://doi.org/10.1101/gr.131920.111)** — Murray et al., *Genome Research* 2012 `T1-core` `peer-reviewed`<br>
  线虫胚胎基因表达的多维调控解析（启动子驱动的时空表达）；时空分辨调控分析的早期系统工作。

## Related categories

- [C5: Perturbation & Causal Inference](C5-perturbation-causal.md) — 扰动与因果推断
- [C6: Fate Specification & Lineage Biology](C6-fate-lineage-biology.md) — 命运决定与谱系生物学
