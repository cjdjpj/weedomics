use clap::Parser;
use std::error::Error;
use std::fs::File;
use std::io::Write;
use csv::ReaderBuilder;
use kodama::{Method, linkage};

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    fname: String,

    #[clap(short, long)]
    output: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    // read in arguments
    let args = Args::parse();

    let file = File::open(&args.fname)?;
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_reader(file);


    let n = rdr.records().count();
    let mut distances = Vec::new();

    for result in rdr.records() {
        let record = result?;
        let mut row = Vec::new();
        for field in record.iter().skip(1) {
            let value = field.parse::<f64>()?;
            row.push(value);
        }
        distances.push(row);
    }

    // format dissimilarity matrix
    let mut condensed_matrix = vec![];

    for row in 0..n-1 {
        for col in row+1..n {
            condensed_matrix.push(distances[row][col]);
        }
    }

    assert_eq!(condensed_matrix.len(), (n * (n - 1)) / 2);

    // get heirarchical clustering
    let dendrogram = linkage(&mut condensed_matrix, n, Method::Average);

    // write to file
    let mut output_file = File::create(&args.output)?;
    for step in dendrogram.steps() {
        writeln!(output_file, "{}, {}, {}, {}", step.cluster1, step.cluster2, step.dissimilarity, step.size)?;
    }

    Ok(())
}
