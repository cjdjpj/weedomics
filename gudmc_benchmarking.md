### gudmc
Genome-wide Unbiased Discernment of the Modes of Convergent evolution (gudmc) can be used to identify the most likely evolutionary models of resistance using Tajima's D and $F_{st}$

5 hypotheses:
1. de novo mutations
2. standing genetic variation
3. independent emergence
4. migration
5. shared ancestry

Using quantiNemo2 forward simulations to model each of the evolutionary scenarios, we can assess the accuracy of predictions made by gudmc

2 stages of simulation
1. Burn in
	- Ancestral population is allowed to grow rapidly to a carrying capacity, accumulating heterozygosity
	- Only mutation and drift
	- Depending on tested hypothesis, QTLs are/are not introduced
2. Dispersal
	- Ancestral population disperses into three new environments with varying selection and migration

### Parameterization
Use `rust_utils/create_genome` to generate the files genetic maps and indices (`ntrl_genome`, `qtl_genome`, `ntrl_index`, `qtl_index`).
Both neutral and quantitative loci are equally distributed across 7 chromosomes.

#### Burn in
```
### GENERAL ###
folder "RUN_burnin"
filename "burnin"

set t1 1800

### DEMOGRAPHY ###
generations                   t1
patch_capacity                5000
patch_ini_size                50
mating_nb_offspring_model     8
growth_rate                   0.1

### DISPERSAL ###
##### NONE ######

### GENOTYPE ###
ntrl_loci                     7000
quanti_loci                   100
ntrl_all                      4
quanti_all                    4
ntrl_ini_allele_model         1
quanti_ini_allele_model       1
ntrl_mutation_rate            10e-7
quanti_mutation_rate          10e-7
quanti_mutation_model         2
ntrl_genome                   $../ntrl_genome
quanti_genome                 $../qtl_genome
ntrl_locus_index              $../ntrl_index
quanti_locus_index            $../qtl_index

### SELECTION ###
##### NONE ######

### OUTPUT ###
stat {adlt.nbInd
	  n.adlt.nbAll
	  q.adlt.nbAll
	  q.VgW}

ntrl_save_genotype            1
quanti_save_genotype          1
ntrl_genot_filename           ntrl
quanti_genot_filename         quanti
ntrl_genot_logtime            t1
quanti_genot_logtime          t1
```

Outputs a `ntrl_g1800.dat` and `quanti_g1800.dat`
We wish to use this burned in pool for all our evolutionary scenarios. To do this, we randomly sample the first 150 individuals, distributing 50 into each of the 3 patches in our hypothesis testing run.
- This was done manually, giving us `burned_in_ntrl1800.dat` and `burned_in_quanti1800.dat`

#### Standing genetic variation
```
### GENERAL ###
folder "RUN_standingv"
filename "standingv"

set t2 300

### DEMOGRAPHY ###
generations                   t2
patch_number                  3
patch_capacity                {{1 5000}{2 5000}{3 5000}}
patch_ini_size                {{1 50}{2 50}{3 50}}
mating_nb_offspring_model     8
growth_rate                   0.1

### DISPERSAL ###
##### NONE ######

### GENOTYPE ###
ntrl_loci                     7000
quanti_loci                   100
ntrl_all                      4
quanti_all                    4
ntrl_ini_genotypes            "../burned_in_ntrl1800.dat"
quanti_ini_genotypes          "../burned_in_quanti1800.dat"
ntrl_mutation_rate            10e-7
quanti_mutation_rate          10e-7
quanti_mutation_model         2
ntrl_genome                   $../ntrl_genome
quanti_genome                 $../qtl_genome
ntrl_locus_index              $../ntrl_index
quanti_locus_index            $../qtl_index

### SELECTION ###
quanti_heritability           0.9
quanti_selection_model        2

### OUTPUT ###
stat {adlt.nbInd_p
	  meanW_p
	  n.adlt.nbAll
	  q.adlt.nbAll
	  q.VpW}

ntrl_save_genotype            1
quanti_save_genotype          1
ntrl_genot_filename           ntrl
quanti_genot_filename         quanti
ntrl_genot_logtime            t2
quanti_genot_logtime          t2
```

Convert FSTAT to sync using `rust_utils/fstat2sync`