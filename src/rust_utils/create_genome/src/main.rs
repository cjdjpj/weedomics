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
    let ntrl_output = File::create("ntrl_genome")?;
    let qtl_output = File::create("qtl_genome")?;
    let mut ntrl_index_output = File::create("ntrl_index")?;
    let mut qtl_index_output = File::create("qtl_index")?;

    let ntrl_per_chr = divide_into_chromosomes(args.num_ntrl, args.chromosomes);
    let qtl_per_chr = divide_into_chromosomes(args.num_qtl, args.chromosomes);

    write!(&ntrl_output, "{{\n")?;
    write!(&qtl_output, "{{\n")?;

    for chr in 0..args.chromosomes{
        let mut ntrl_chr_str = format!(" {{{}: ", chr+1);
        let mut qtl_chr_str = format!(" {{{}: ", chr+1);
        let ntrl_diff = 100.0/ntrl_per_chr[chr as usize] as f64;
        let ntrl_positions: Vec<f64> = (0..ntrl_per_chr[chr as usize]).map(|i| i as f64 * ntrl_diff).collect();
        let qtl_diff = 100.0/qtl_per_chr[chr as usize] as f64;
        let qtl_positions: Vec<f64> = (0..qtl_per_chr[chr as usize]).map(|i| i as f64 * qtl_diff).collect();

        for qtl in qtl_positions{
            qtl_chr_str = format!("{} {}", qtl_chr_str, qtl);
        }
        for ntrl in ntrl_positions{
            ntrl_chr_str = format!("{} {}", ntrl_chr_str, ntrl);
        }
        writeln!(&ntrl_output, "{}}}", ntrl_chr_str)?;
        writeln!(&qtl_output, "{}}}", qtl_chr_str)?;
    }

    write!(&ntrl_output, "}}")?;
    write!(&qtl_output, "}}")?;

    let ntrl_index: Vec<u32> = (1..args.num_ntrl+1).collect();
    let qtl_index: Vec<u32> = (1..args.num_qtl+1).collect();

    let ntrl_str = format!("{{{}}}", ntrl_index.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(" "));
    let qtl_str = format!("{{{}}}", qtl_index.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(" "));
    ntrl_index_output.write_all(ntrl_str.as_bytes())?;
    qtl_index_output.write_all(qtl_str.as_bytes())?;

    Ok(())
}
