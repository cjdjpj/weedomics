# 1. Filtering and Parsing data
Generate sync file of dataset for statistical analysis using [poolgen](https://github.com/jeffersonfparil/poolgen/)
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
../poolgen/target/release/poolgen fst\
    -f 'cut_genome_chr_d.sync' \
    --phen-fname '../Lolium_phenotype_cut_for_distance.csv' \
    --n-threads 32 \
    --window-size-bp 10000 \
    --window-slide-size-bp 5000 \
    -o 'ws10000/genome_fst.csv' &
```
```bash
../poolgen/target/release/poolgen heterozygosity \
    -f 'cut_genome_chr.sync' \
    --phen-fname '../Lolium_phenotype_cut.csv' \
    --n-threads 32 \
    --window-size-bp 10000 \
    --window-slide-size-bp 5000 \
    -o 'ws10000/genome_10000_het.csv' &
```
![Fst](https://github.com/cjdjpj/weedomics/blob/main/figures/fst.png)
![Heterozygosity](https://github.com/cjdjpj/weedomics/blob/main/figures/heterozygosity.png)
# 3. Looking deeper into the data
We wish to identify structural patterns in the ryegrass dataset, as well as test them against what we expect under standard population genetic theory.
This will also allow us to identify patterns that we can further investigate with regards to their correlation with glyphosate resistance.

### Hierarchical clustering
Since $F_{st}$ is a genetic "distance", we can conduct a naive clustering based on $F_{st}$ using hierarchical clustering.
![Hierarchical_clustering_fst](https://github.com/cjdjpj/weedomics/blob/main/figures/dendrogram_fst.png)
From the dendrogram, we can see that overall, there are very few distinct clusters and thus isn't too useful. 
We can compare the dendrogram to hierarchical clustering based on **geographic distance** (km), where there are much more distinct clusters (populations of ryegrass generally collected at hotspots).

![Hierarchical_clustering_distance](https://github.com/cjdjpj/weedomics/blob/main/figures/dendrogram_dist.png)

### Isolation by distance
#### Mantel test
#### Linear regression
#### Linear regression clusters
### Competitive mapping of outlier pools
