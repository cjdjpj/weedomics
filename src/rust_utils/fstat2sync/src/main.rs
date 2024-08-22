#![allow(warnings)]
use clap::Parser;
use std::error::Error;
use std::io::{Write, BufRead, BufReader};
use std::fs::File;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args{
    ///Input FSTAT (Goudet 1995) file
    #[clap(short, long)]
    fname: String,

    ///Output synchronized pileup file
    #[clap(short, long)]
    output: String,
}

fn divide_into_chromosomes(total: u32, num_chr: u32) -> Vec<u32>{
    let base = total/num_chr;
    let remaining = total%num_chr;
    let mut chromosomes = vec![base; num_chr as usize];

    for i in 0..remaining{
        chromosomes[i as usize] += 1;
    }
    for i in 1..num_chr{
        chromosomes[i as usize] += chromosomes[i as usize-1];
    }
    chromosomes
}

#[derive(Debug)]
struct Fstat{
    patches: u32,
    num_loci: u32,
    num_alleles: u32,
    allele_digits: u32,
    allele_counts: Vec<Vec<(u32, u32, u32, u32)>>
}

impl Fstat{
    fn read_fstat(fname: &String) -> Result<Self, Box<dyn Error>>{
        let fstat_file = File::open(fname)?;
        let mut fstat_reader = BufReader::new(fstat_file);

        let mut metadata = String::new();
        fstat_reader.read_line(&mut metadata)?;

        let metadata: [&str; 4] = metadata.split_whitespace()
            .collect::<Vec<&str>>()
            .try_into()
            .unwrap();

        let patches: u32 = metadata[0].parse().unwrap();
        let num_loci: u32 = metadata[1].parse().unwrap();
        let num_alleles: u32 = metadata[2].parse().unwrap();
        let allele_digits: u32 = metadata[3].parse().unwrap();

        assert!(num_alleles == 4, "Number of alleles must be 4 (A/T/G/C)");

        // skip locus names
        for _ in 0..num_loci{
            let _ = fstat_reader.read_line(&mut String::new())?;
        }

        let mut allele_counts: Vec<Vec<(u32, u32, u32, u32)>> = vec![vec![(0,0,0,0); patches as usize]; num_loci as usize];

        // read genotypes
        let mut genotype = String::new();
        while fstat_reader.read_line(&mut genotype)? > 0 {
            let mut reads: Vec<&str> = genotype.split_whitespace().collect();
            let patch = reads.remove(0).parse::<usize>()? - 1;
            for (l, read) in reads.iter().enumerate(){
                let allele1 = read[0..allele_digits as usize].parse::<u32>().unwrap();
                let allele2 = read[allele_digits as usize..read.len()].parse::<u32>().unwrap();
                match allele1{
                    1 => allele_counts[l][patch].0 += 1,
                    2 => allele_counts[l][patch].1 += 1,
                    3 => allele_counts[l][patch].2 += 1,
                    4 => allele_counts[l][patch].3 += 1,
                    _ => panic!("Invalid allelic value"),
                }
                match allele2{
                    1 => allele_counts[l][patch].0 += 1,
                    2 => allele_counts[l][patch].1 += 1,
                    3 => allele_counts[l][patch].2 += 1,
                    4 => allele_counts[l][patch].3 += 1,
                    _ => panic!("Invalid allelic value"),
                }
            }
            genotype.clear(); 
        }

        Ok(Fstat{
            patches,
            num_loci,
            num_alleles,
            allele_digits,
            allele_counts,
        })
    }

    fn write2sync(&self, output: &String) -> Result<(), Box<dyn Error>>{
        let mut sync_file = File::create(output)?;
        let mut header = "chr\tpos\tref".to_owned();
        for i in 0..self.patches{
            header = format!("{header}\tpatch{i}")
        }
        writeln!(sync_file, "#{header}")?;
        let chromosomes_breakpoints = divide_into_chromosomes(self.num_loci, 7);
        let mut chromosome = 1;
        for (locus_index, locus) in self.allele_counts.iter().enumerate(){
            if locus_index as u32 > chromosomes_breakpoints[chromosome as usize-1]{
                chromosome += 1;
            }
            let mut locus_string = format!("{chromosome}\t{locus_index}\tNA");
            let mut pool_seq = String::new();
            for pool in locus{
                let (a, t, g, c) = pool;
                pool_seq = format!("{a}:{t}:{g}:{c}:0:0");
                let ref_base = if a >= t && a >= g && a >= c {
                    "A"
                } else if t >= g && t >= c {
                    "T"
                } else if g >= c {
                    "G"
                } else {
                    "C"
                };
                locus_string = format!("{locus_string}\t{pool_seq}");
            }
            writeln!(sync_file, "{}", locus_string)?;
        }
        Ok(())
    }
}

fn main() -> Result<(), Box<dyn Error>>{
    let args = Args::parse();
    let fstat = Fstat::read_fstat(&args.fname)?;
    fstat.write2sync(&args.output)?;
    Ok(())
}
