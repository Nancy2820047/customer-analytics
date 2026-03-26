import sys
import os
import pandas as pd

# first step in the pipeline
# loads the raw dataset and saves a copy

def load_data(filepath):
    
    df = pd.read_csv(filepath)
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    
    df.to_csv("data_raw.csv", index=False)
    print("\nRaw data saved as data_raw.csv")
    
    return "data_raw.csv"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("provide the dataset path: python ingest.py <path>")
        sys.exit(1)

    raw_path = load_data(sys.argv[1])
    os.system(f"python preprocess.py {raw_path}")