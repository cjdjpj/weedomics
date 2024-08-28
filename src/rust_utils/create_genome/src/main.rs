use clap::Parser;
use std::error::Error;
use std::io::Write;
use std::fs::File;

///Creates a genome with a certain number of chromosomes, neutral loci, and QTLs.
///Neutral loci and QTLs are evenly distributed across chromosomes and evenly spaced within a
///chromosome.
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    ///Number of chromosomes
    #[clap(short, long)]
    chromosomes: u32,

    ///Number of total neutral loci
    #[clap(long)]
    num_ntrl: u32,

    ///Number of total quantitative loci
    #[clap(long)]
    num_qtl: u32
}

fn divide_into_chromosomes(total: u32, num_chr: u32) -> Vec<u32>{
    let base = total/num_chr;
    let remaining = total%num_chr;
    let mut chromosomes = vec![base; num_chr as usize];

    for i in 0..remaining{
        chromosomes[i as usize] += 1;
    }
    chromosomes
}

fn main() -> Result<(), Box<dyn Error>>{
    let args = Args::parse();
    let genome_output = File::create("genome")?;
    let ntrl_index_output = File::create("ntrl_index")?;
    let qtl_index_output = File::create("qtl_index")?;

    let ntrl_per_chr = divide_into_chromosomes(args.num_ntrl, args.chromosomes);
    let qtl_per_chr = divide_into_chromosomes(args.num_qtl, args.chromosomes);

    let mut ntrl_index: Vec<u32> = Vec::new();
    let mut qtl_index: Vec<u32> = Vec::new();

    write!(&genome_output, "{{\n")?;

    let mut global_l = 0;
    for chr in 0..args.chromosomes{
        let mut chr_str = format!("\t{{{}:", chr+1);
        let ntrl_diff = 100.0/ntrl_per_chr[chr as usize] as f64;
        let ntrl_positions: Vec<f64> = (0..ntrl_per_chr[chr as usize]).map(|i| i as f64 * ntrl_diff).collect();
        let qtl_diff = 100.0/qtl_per_chr[chr as usize] as f64;
        let qtl_positions: Vec<f64> = (0..qtl_per_chr[chr as usize]).map(|i| i as f64 * qtl_diff).collect();
        let mut genome_positions = [ntrl_positions.clone(), qtl_positions.clone()].concat();
        genome_positions.sort_by(|a, b| a.partial_cmp(b).unwrap());

        let mut ntrl_i: u32 = 0;
        let mut qtl_i: u32 = 0;
        for locus in &genome_positions{
            if *locus == ntrl_positions[ntrl_i as usize]{
                ntrl_index.push(global_l+1);
                ntrl_i += 1;
            }
            else if *locus == qtl_positions[qtl_i as usize]{
                qtl_index.push(global_l+1);
                qtl_i += 1;
            }
            else {
                panic!("you messed up");
            }
            global_l += 1;
        }

        for locus in genome_positions{
            chr_str = format!("{chr_str} {locus}");
        }
        writeln!(&genome_output, "{chr_str}}}")?;
    }
    writeln!(&genome_output, "}}")?;

    let mut ntrl_str = "{".to_string();
    for (i, n) in ntrl_index.iter().enumerate(){
        if i==0{
            ntrl_str = format!("{ntrl_str}{n}");
        } else {
            ntrl_str = format!("{ntrl_str} {n}");
        }
    }
    writeln!(&ntrl_index_output, "{ntrl_str}}}")?;
    let mut qtl_str = "{".to_string();
    for (i, n) in qtl_index.iter().enumerate(){
        if i==0{
            qtl_str = format!("{qtl_str}{n}");
        } else {
            qtl_str = format!("{qtl_str} {n}");
        }
    }
    writeln!(&qtl_index_output, "{qtl_str}}}")?;

    Ok(())
}
