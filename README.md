# weedomics
What are the evolutionary origins of glyphosate resistance in *Lolium rigidum* in Southeast Australia? What can we infer from genetic data alone? (and with how much accuracy?)
1. [data_filtering](data_filtering.md): Filtering and parsing of pileup to synchronized pileup (sync) using poolgen
2. [exploratory_analysis](exploratory_analysis.md): Inference of pooled *Lolium rigidum* polymorphism data in Southeast Australia. Detection of characteristics of glyphosate resistance selection at the genomic level.
3. [gudmc_benchmarking.md](gudmc_benchmarking.md): Benchmarking of gudmc (Genomewide Unbiased Discernment of Modes of Convergent evolution) using [quantiNemo2](https://doi.org/10.1093/bioinformatics/bty737) forward simulations

(extra) [smooth_spline_windows](smooth_spline_windows.md): Implementing [Beissinger et al. 2015](https://gsejournal.biomedcentral.com/articles/10.1186/s12711-015-0105-9) smooth spline windows to compute summary statistics with greater statistical power for gudmc.

Exploratory analysis python and rust code in `src/`

The data consists of 246 sequenced and phenotyped *Lolium rigidum* pools from across Southeast Australia. Glyphosate resistance is measured as the proportion of a tested sample still remaining after treatment.
<img src="figures/map.png" alt="map" width="800px"/>

Does not contain data (except plots) - analysis cannot be entirely replicated.