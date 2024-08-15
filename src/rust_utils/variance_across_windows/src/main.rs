use clap::Parser;
use std::fs::OpenOptions;
use std::io::Write;
use std::error::Error;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    fname: String,

    #[clap(short, long)]
    output: String,

    #[clap(short, long)]
    window_size: u32,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let mut rdr = csv::Reader::from_path(&args.fname)?;
    let mut values: Vec<Vec<f64>> = Vec::new();
    let mut num_windows = 0;
    let num_pools = rdr.records().count();

    for result in rdr.records() {
        let record = result?;
        let mut row: Vec<f64> = Vec::new();
        for field in record.iter().skip(2) { // Skip the first two columns
            if let Ok(value) = field.parse::<f64>() {
                row.push(value);
                num_windows += 1;
            } else {
                // Handle NaN or other parsing errors
                // For now, we'll just skip this field
                continue;
            }        }
        values.push(row);
    }    

    num_windows = num_windows/num_pools;

    // find mean
    let means: Vec<f64> = (0..num_windows)
        .map(|window| {
            let sum: f64 = (0..num_pools)
                .map(|pool| values[window][pool])
                .sum();
            return sum / num_pools as f64
        })
        .collect();

    // find variances
    let variances: Vec<f64> = (0..num_windows)
        .map(|window| {
            let sum_of_squares: f64 = (0..num_pools)
                .map(|pool| (values[pool][window]-means[window]).powi(2))
                .sum();
            return sum_of_squares/(num_pools-1) as f64;
        })
        .collect();

    let mut output_file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&args.output)?;

    for var in variances {
        writeln!(output_file, "{},{}", &args.window_size, var)?;
    }

    Ok(())
}
