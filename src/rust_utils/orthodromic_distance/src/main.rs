use clap::Parser;
use csv::Writer;
use std::error::Error;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    fname: String,

    #[clap(short, long)]
    output: String,
}

const RADIUS_OF_EARTH: f64 = 6371.0;

// population with name and coordinates
struct Population {
    name: String,
    x: f64,
    y: f64,
}

fn main() -> Result<(), Box<dyn Error>> {
    // read in arguments
    let args = Args::parse();

    let mut rdr = csv::Reader::from_path(&args.fname)?;
    let mut populations: Vec<Population> = Vec::new();
    let n = rdr.records().count();

    // read in populations
    for result in rdr.records() {
        let record = result?;
        let name = record.get(0).unwrap().to_string();
        let x: f64 = (record.get(1).unwrap().parse::<f64>()?) * std::f64::consts::PI / 180.0;
        let y: f64 = (record.get(2).unwrap().parse::<f64>()?) * std::f64::consts::PI / 180.0;

        populations.push(Population {
            name,
            x,
            y,
        });
    }

    // calculate orthodromic distance
    let mut distances = vec![vec![0.0; n]; n];
    for (i, point1) in populations.iter().enumerate() {
        for (j, point2) in populations.iter().enumerate() {
            distances[i][j] = 2.0
                * RADIUS_OF_EARTH
                * (((1.0 - (point2.x - point1.x).cos()
                    + point2.x.cos() * point1.x.cos() * (1.0 - (point2.y - point1.y).cos()))
                    / 2.0)
                    .sqrt())
                .asin();
        }
    }

    // write orthodromic distances
    let mut wtr = Writer::from_path(&args.output)?;

    let mut header = vec![""];
    for population in &populations {
        header.push(&population.name);
    }
    wtr.write_record(&header)?;

    for (i, row) in distances.iter().enumerate() {
        let mut record = vec![populations[i].name.clone()];
        for distance in row {
            record.push(distance.to_string());
        }
        wtr.write_record(&record)?;
    }
    wtr.flush()?;

    Ok(())
}
