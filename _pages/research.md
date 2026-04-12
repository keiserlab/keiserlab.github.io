---
layout: single
title: Research
permalink: /research/
excerpt: “The Keiser Lab developed AI/ML methods for drug discovery, biomedical image analysis, and complex scientific research at UCSF.”
tags: [research, AI, machine learning, deep learning, generative models, diffusion models, language models, representation learning, drug discovery, systems pharmacology, neuropathology, phenotypic profiling, molecular design, adversarial evaluation]
modified: 
comments: false
header:
   image: /assets/images/bar-network.webp
---

Over a decade, the Keiser Lab developed AI and machine learning across a progression of scientific challenges: from predicting how drugs interact with protein targets, to decoding complex biological systems, to advancing the AI methods themselves.

### Systems pharmacology & molecular prediction

[![Predicted drug-target network from Keiser et al., Nature 2009](/assets/images/research-sea-network.webp){: .align-right style="max-width: 50%;"}](https://doi.org/10.1038/nature08506)

The lab’s earliest work addressed a foundational problem: drugs rarely act on a single target. The [Similarity Ensemble Approach (SEA)](http://sea.bkslab.org/) used the statistical similarity of ligand sets to predict unexpected drug-target interactions, revealing that many approved drugs hit targets no one had anticipated ([*Nat Biotechnol* 2007](https://doi.org/10.1038/nbt1284); [*Nature* 2009](https://doi.org/10.1038/nature08506)). These predictions were validated at scale, identifying clinically relevant off-target effects across hundreds of drugs ([*Nature* 2012](https://doi.org/10.1038/nature11159)) and informing FDA drug safety surveillance ([*Clin Pharmacol Ther* 2015](https://doi.org/10.1002/cpt.2)).

To move beyond ligand similarity, the lab developed new molecular representations using deep learning. [E3FP](https://github.com/keiserlab/e3fp) encoded 3D molecular shape into learnable fingerprints ([*J Med Chem* 2017](https://doi.org/10.1021/acs.jmedchem.7b00696)), and later work advanced molecular representation learning for medicinal chemistry more broadly ([*J Med Chem* 2020](https://doi.org/10.1021/acs.jmedchem.0c00385)). These efforts laid the groundwork for increasingly powerful AI approaches to molecular interaction.

### AI for complex biological systems

The lab applied deep learning to problems where the biological complexity exceeded what traditional computational methods could address.

[![Trans-channel fluorescence learning predicts AT8-pTau from DAPI and YFP-tau channels, from Wong et al., Nature Machine Intelligence 2022](/assets/images/research-transchannel.webp){: .align-right style="max-width: 50%;"}](https://doi.org/10.1038/s42256-022-00490-8)

In **phenotypic profiling**, deep metric learning models decoded zebrafish behavioral responses to thousands of neuroactive compounds, identifying drugs with novel mechanisms of action that conventional target-based screening would miss ([*Nat Commun* 2024](https://doi.org/10.1038/s41467-024-54375-y); [*Nat Commun* 2019](https://doi.org/10.1038/s41467-019-11936-w)). Trans-channel fluorescence learning generated informative image channels from high-content screens, unlocking historical datasets for Alzheimer’s drug discovery ([*Nat Mach Intell* 2022](https://doi.org/10.1038/s42256-022-00490-8)).

In **neuropathology**, the lab built convolutional neural network pipelines for interpretable classification of Alzheimer’s disease pathologies ([*Nat Commun* 2019](https://doi.org/10.1038/s41467-019-10212-1)), validated amyloid detection models across institutions ([*Acta Neuropathol Commun* 2020](https://doi.org/10.1186/s40478-020-00927-4); [*Commun Biol* 2023](https://doi.org/10.1038/s42003-023-05031-6)), and developed [tangle-tracer](https://github.com/keiserlab/tangle-tracer) for precise neurofibrillary tangle segmentation from rapid point annotations. This work contributed to network-directed combination therapies for neurodegeneration ([*Cell* 2025](https://doi.org/10.1016/j.cell.2025.06.035)).

In **genomics**, the lab discovered that repetitive elements serve as key determinants of 3D genome folding ([*Cell Genom* 2023](https://doi.org/10.1016/j.xgen.2023.100410)) and developed [ChromaFactor](https://github.com/lgunsalus/ChromaFactor) for deconvolution of single-molecule chromatin organization ([*PLoS Comput Biol* 2025](https://doi.org/10.1371/journal.pcbi.1012841)).

### Advancing AI methods for science

The lab’s work progressively advanced the frontier of AI methods, not just applying existing models to scientific problems but developing new architectures, training paradigms, and evaluation frameworks.

[![AutoFragDiff: generative diffusion model designing a ligand inside a protein binding pocket, from Ghorbani et al., NeurIPS GenBio 2023](/assets/images/research-autofragdiff.webp){: .align-right style="max-width: 50%;"}](https://arxiv.org/abs/2401.05370)

**Generative models** for molecular design represented the most forward-looking direction. [AutoFragDiff](https://github.com/keiserlab/autofragdiff) introduced autoregressive fragment-based diffusion for pocket-aware ligand design, combining diffusion generative models with the structural constraints of protein binding sites ([*NeurIPS GenBio* 2023](https://arxiv.org/abs/2401.05370)). Attention-based learning on molecular ensembles explored how attention mechanisms could capture conformational diversity ([*NeurIPS ML4Molecules* 2020](https://doi.org/10.48550/arXiv.2011.12820)). And the [exceiver](https://github.com/keiserlab/exceiver), a single-cell gene expression language model, applied transformer architectures to learn biological representations directly from transcriptomic data ([*NeurIPS LMRL* 2022](https://doi.org/10.48550/arXiv.2210.14330)).

**Rigorous evaluation of AI** was a parallel theme. The lab demonstrated that adversarial controls are essential for scientific machine learning, showing how standard benchmarks can mislead ([*ACS Chem Biol* 2018](https://doi.org/10.1021/acschembio.8b00881); [*Science* 2018](https://doi.org/10.1126/science.aat8603)), developed robust concept activation vectors for semantic interpretability ([*ICML WHI* 2020](https://doi.org/10.48550/arXiv.2104.02768)), and stress-tested diagnostic AI models for clinical readiness ([*NPJ Digit Med* 2021](https://doi.org/10.1038/s41746-020-00380-6)). Methods for [stochastic negative sampling](https://github.com/keiserlab/stochastic-negatives-paper) improved molecular bioactivity prediction ([*J Chem Inf Model* 2020](https://doi.org/10.1021/acs.jcim.0c00565)), and VAE-based anomaly generation provided new tools for fuzz testing molecular representations ([*J Chem Inf Model* 2025](https://doi.org/10.1021/acs.jcim.4c01876)).

**Retrieval-augmented and scalable approaches** connected learned representations with efficient search. [RAD](https://github.com/keiserlab/rad) applied hierarchical navigable small worlds to molecular docking ([*J Chem Inf Model* 2024](https://doi.org/10.1021/acs.jcim.4c00683)), and [autoparty](https://github.com/keiserlab/autoparty) used machine learning to automate the visual inspection bottleneck in structure-based drug discovery ([*J Chem Inf Model* 2025](https://doi.org/10.1021/acs.jcim.5c00850)).
