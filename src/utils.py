import os
import pandas as pd

def trim_df(df, trim):
    to_drop_col = [label for label in trim if label in df.columns]
    to_drop_row = [label for label in trim if label in df.index]
    df = df.drop(index=to_drop_row, columns=to_drop_col)
    return df


def flatten_df(df):
    flattened_list = []
    pool_pairs = []
    n = df.shape[1]
    for row in range(0,n-1):
        for col in range(row+1,n):
            flattened_list.append(df.iloc[row,col])
            pool_pairs.append((df.index[row], df.index[col]))
    
    flattened_df = pd.DataFrame({
        "data": flattened_list,
        "labels": pool_pairs,
    })

    return flattened_df


def create_df(distances_path, fst_path, trim):
    dirname = os.path.dirname(os.path.abspath(__file__))
    distances_path = os.path.join(dirname, distances_path)
    fst_path = os.path.join(dirname, fst_path)

    distances = pd.read_csv(distances_path, index_col=0)
    fst = pd.read_csv(fst_path, index_col=0)
    
    distances = trim_df(distances, trim)
    fst = trim_df(fst, trim)

    flattened_distances = flatten_df(distances)
    flattened_fst = flatten_df(fst)

    df = pd.DataFrame({
        "distances": flattened_distances["data"],
        "fst": flattened_fst["data"],
        "pool_pairs": flattened_fst["labels"],
    })
    return df
