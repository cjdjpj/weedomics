use clap::Parser;
use std::error::Error;
use std::fs::File;
use std::io::{self, Write, BufRead, BufReader};

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    fname: String,

    #[clap(short, long)]
    output: String,
}

fn read_tsv_file(file_path: &str) -> io::Result<Vec<Vec<String>>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);

    let mut data = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let values: Vec<String> = line.split('\t').map(|s| s.to_string()).collect();
        data.push(values);
    }
    Ok(data)
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let sync = read_tsv_file(&args.fname)?;
    let mut output_file = File::create(&args.output)?;
    for (row_index, row) in sync.iter().enumerate() {
        if row_index == 0{
            continue;
        }
        let mut counts: Vec<u32> = vec![0,0,0,0,0,0];
        let mut new_row = String::new();
        for (col_index, value) in row.iter().enumerate() {
            if col_index < 3{
                new_row.push_str(value);
                new_row.push_str("\t");
                continue
            }
            let polymorphisms: Vec<u32> = value.split(':')
                              .map(|s| s.parse().unwrap()) 
                              .collect();
            for (index, &count) in polymorphisms.iter().enumerate(){
                counts[index] += count;
            }
        }
        for (index, &count) in counts.iter().enumerate(){
            new_row.push_str(&count.to_string());
            if index != 5{
                new_row.push_str(":");
            } 
        }
        writeln!(output_file, "{}", new_row)?;
    }



    Ok(())
}
