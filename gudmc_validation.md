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

Burn in quantinemo.ini
```
### GENERAL ###
folder "burnin"
filename "burnin"

set t1 300

### DEMOGRAPHY ###
generations               t1
patch_capacity            5000
patch_ini_size            50
mating_nb_offspring_model 8
growth_rate               0.1

### DISPERSAL ###

### GENOTYPE ###
ntrl_loci                 7000
quanti_loci               100
ntrl_all                  4
quanti_all                4
ntrl_ini_allele_model     1
quanti_ini_allele_model   1
ntrl_mutation_rate        10e-7
quanti_mutation_rate      10e-7
quanti_mutation_model     2
ntrl_genome               $../ntrl_genome
quanti_genome             $../qtl_genome
ntrl_locus_index          $../ntrl_index
quanti_locus_index        $../qtl_index

### SELECTION ###

### OUTPUT ###
stat {adlt.nbInd
	  n.adlt.nbAll
	  q.adlt.nbAll
	  q.VgW}

ntrl_save_genotype        2
quanti_save_genotype      2
ntrl_genot_filename       ntrl
quanti_genot_filename     quanti
ntrl_genot_logtime        t1
quanti_genot_logtime      t1
```