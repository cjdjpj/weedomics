# Data Filtering
There are 2 components to generating sync from pileup with [poolgen](https://github.com/jeffersonfparil/poolgen/)
1. Pileup pool-seq data
```
/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/AllPop_Weedomics.mpileup
```
2. Phenotype description of pools
```
# ALL POOLS
/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/Lolium_phenotype_uncut.csv

# Only ACC, Boxer, Cleth, Gly, Sak (246 populations)
/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/Lolium_phenotype_cut.csv
```

### Filtering options
1. `--min-coverage-breadth` (float): At least this proportion of the pools must have `--min-coverage-depth` coverage
2. `--min-coverage-depth` (integer): At least `--min-coverage-breadth` proportion of the pools must have this coverage

e.g. if `min-coverage-breadth 0.5` and `min-coverage-depth 5`, then at least 50% of the pools must have a minimum coverage of 5 at any locus, or that locus is removed.

3. `--remove-monoallelic` (boolean): Remove loci with no coverage of any alternative alleles
4. `--keep-lowercase-reference` (boolean): Treat lowercase bases as their uppercase counterparts, rather than labeling them as `N`. Lowercase bases may indicate low quality reads which is why they may want to be ignored.

Example:
```bash
./poolgen/target/release/poolgen pileup2sync \
    -f '/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/AllPop_Weedomics.mpileup' \
    --phen-fname '/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/Lolium_phenotype_uncut.csv' \
    --min-coverage-depth 5 \
    --min-coverage-breadth 0.5 \
    --remove-monoallelic \
    --keep-lowercase-reference \
    --phen-value-col 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 \
    --n-threads 32 \
    -o 'genome.sync' &
```

### Pre-made sync files
```
--min-coverage-depth 5
--min-coverage-breadth 0.5
--remove-monoallelic
--keep-lowercase-reference
```

With all pools:
```
/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/sync/genome.sync
```
With only ACC, Boxer, Cleth, Gly, Sak (246 populations):
```
/data/Lolium/Genomics/SEQUENCES/DNA/Illumina_ALL_SEQUENCES/MERGED/sync/cut_genome.sync
```
