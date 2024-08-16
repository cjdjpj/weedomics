# 1. Filtering and Parsing data
Generate synchronized pileup file (sync) from pileup for statistical analysis using [poolgen](https://github.com/jeffersonfparil/poolgen/)
```bash
./poolgen/target/release/poolgen pileup2sync \
    -f '/path/to/allpools.mpileup' \
    --phen-fname 'Lolium_phenotype_uncut.csv' \
    --min-coverage-depth 5 \
    --min-coverage-breadth 0.5 \
    --remove-monoallelic \
    --keep-lowercase-reference \
    --phen-value-col 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 \
    --n-threads 32 \
    -o 'genome.sync' &
```

# 2. Computing population genetics summary statistics
A summary of summary statistics
1. $\theta$ (Watterson's estimator) is the number of polymorphic sites/segregating sites
	- $\theta = 4N_e\mu$ assuming infinite loci
2. $\pi$ (heterozygosity) tells us how genetically diverse a population is
3. $d_{xy}$ tells us how genetically differentiated two populations are
4. $F_{st}$ combines $\pi$ and $d_{xy}$ to tell us how much variation is within vs between populations, i.e. differentiation due to population structure
	- allows us to estimate migration rates under Wright's finite island model
5. Tajima's D combines $\pi$ and $\theta$ to tell us if a population is evolving neutrally

Computing $F_{st}$ and $\pi$ using popgen
```bash
../poolgen/target/release/poolgen heterozygosity \
    -f 'cut_genome_chr.sync' \
    --phen-fname '../Lolium_phenotype_cut.csv' \
    --n-threads 32 \
    --window-size-bp 10000 \
    --window-slide-size-bp 5000 \
    -o 'ws10000/genome_10000_het.csv' &
```
```bash
../poolgen/target/release/poolgen fst\
    -f 'cut_genome_chr_d.sync' \
    --phen-fname '../Lolium_phenotype_cut_for_distance.csv' \
    --n-threads 32 \
    --window-size-bp 10000 \
    --window-slide-size-bp 5000 \
    -o 'ws10000/genome_fst.csv' &
```
> visualize with `plot_het.py` and `plot_fst.py`

![Heterozygosity](https://github.com/cjdjpj/weedomics/blob/main/figures/heterozygosity.png)
![Fst](https://github.com/cjdjpj/weedomics/blob/main/figures/fst.png)
Overall, our ryegrass populations are not too differentiated.

# 3. Identifying structural patterns
We wish to identify structural patterns in our populations to learn more about demographical and evolutionary forces acting on our populations, as well as test them against what we expect under standard population genetic theory.

This will also allow us to identify patterns that we can measure up against glyphosate resistance.

#### Hierarchical clustering
Since $F_{st}$ is a genetic "distance", we can conduct a naive clustering based on $F_{st}$ using hierarchical clustering.
![Hierarchical_clustering_fst](https://github.com/cjdjpj/weedomics/blob/main/figures/dendrogram_fst.png)
From the dendrogram, we can see that overall, clusters are not well defined and thus this analysis isn't too informative. 
We can compare this dendrogram to hierarchical clustering based on **geographic distance** (km), where there are much more distinct clusters (populations of ryegrass generally collected at hotspots).

To compute an accurate measure of geographical distance, we use the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula)
> visualize with `plot_dendrogram.py`

![Hierarchical_clustering_distance](https://github.com/cjdjpj/weedomics/blob/main/figures/dendrogram_dist.png)

### Isolation by distance
We expect isolation by distance - that genetic differentiation increases with increasing geographical distance - among our populations. This is because of an expected decrease in dispersal of gametes/gene flow for populations further apart.

We can test this hypothesis by computing correlation statistics between our two measures of distance.

From this analysis, only 167 of our 246 pools will be used, since the rest do not have coordinate data.

#### Mantel test
Since both $F_{st}$ and geographical distances are $n \times n$ distance matrices, a reasonable and valid test for correlation is the mantel test. ([Legendre P, Fortin MJ](https://doi.org/10.1111/j.1755-0998.2010.02866.x))
> compute mantel statistic using `mantel_t.py`

We get an r-value of $0.1175$ and a p-value of $0.0109$, showing a statistically significant positive correlation between geographical distance and $F_{st}$ and  supporting isolation by distance.

#### Linear regression
Another way to detect correlations between $F_{st}$ and geographical distance is to collapse the $n \times n$ matrix into a 1D array of pairwise distances to conduct a simple linear regression analysis. This flattened collection would remove redundancy (symmetric pairs - AxB is the same as BxA) and be of length $\frac{n \times (n-1)}{2}$

This allows us to isolate specific pairs of pools that support/do not support isolation by distance.
> visualize using `plot_fst_vs_dist.py`

![linreg](https://github.com/cjdjpj/weedomics/blob/main/figures/linreg.png)

Using a linear regression, we reinforce our result from the mantel test - getting a statistically significant positive correlation between $F_{st}$ and geographical distance.
However, we also see some sort of structural separation, a very clear upper cluster with higher $F_{st}$ than the rest of the pools and a less well defined middle cluster. Most of the pool pairs exist in the bottom cluster.

#### Linear regression clusters
We can separate the clusters (by eyeball) and conduct separate linear regressions for each of the clusters.
> visualize using `plot_fst_vs_dist_clusters.py`

![linreg_clusters](https://github.com/cjdjpj/weedomics/blob/main/figures/linreg_clusters.png)

While the middle cluster is still statistically significant in its positive correlation, the upper cluster is not ($p = 0.175$).
In order to know why these clusters exist, we need to first identify which pools are represented in each cluster.

Each pool appears 167 times in the data set, since each pool has a pair with each other pair. We can count the frequency of each pool's appearance in each cluster.
For each pool, our null comparative for how often we would expect it to appear can simply be the number of points in each cluster divided by the total number of points ($\frac{167*(167-1)}{2} = 13861$). This will be indicated by a red line.
> visualize using `plot_fst_vs_dist_clusters_freq.py`

![cluster1](https://github.com/cjdjpj/weedomics/blob/main/figures/cluster1.png)
![cluster2](https://github.com/cjdjpj/weedomics/blob/main/figures/cluster2.png)
![cluster3](https://github.com/cjdjpj/weedomics/blob/main/figures/cluster3.png)

From this, we can clearly see that the clusters are caused by only a couple of pools.
They are: ACC115 in the middle cluster, and GLYPH-UoA-616.1-21 and GLYPH-UoA-632.1-21 in the upper cluster.

# 4. Competitive mapping of outlier pools
