import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# second step in the pipeline
# cleans and transforms the raw data to get it ready for analysis

def clean(df):
    print("Cleaning")

    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows")

    df = df[df['price'] > 0]
    print(f"Removed rows with invalid prices, {len(df)} rows remaining")

    df['brand'] = df['brand'].fillna('unknown')

    df = df.dropna(subset=['event_type', 'product_id', 'user_id'])

    print(f"Missing values after cleaning:\n{df.isnull().sum()}")
    return df


def transform(df):
    print("\nTransformation")

    df['event_time'] = pd.to_datetime(df['event_time'], utc=True)
    df['hour'] = df['event_time'].dt.hour
    df['day_of_week'] = df['event_time'].dt.dayofweek

    event_mapping = {
        'view': 0,
        'cart': 1,
        'remove_from_cart': 2,
        'purchase': 3
    }
    df['event_type_encoded'] = df['event_type'].map(event_mapping)
    scaler = MinMaxScaler()
    df['price_scaled'] = scaler.fit_transform(df[['price']])

    print("Encoded event_type and scaled price")
    print(f"Hour range: {df['hour'].min()} - {df['hour'].max()}")
    return df


def reduce(df):
    print("\nDimensionality Reduction")
    cols_to_drop = ['category_code', 'category_id', 'user_session', 'event_time']
    df = df.drop(columns=cols_to_drop)

    print(f"Remaining columns: {list(df.columns)}")
    return df


def discretize(df):
    print("\nDiscretization")

    bins = [0, 5, 20, 60, float('inf')]
    labels = ['budget', 'mid', 'premium', 'luxury']
    df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels)

    print(f"Price range distribution:\n{df['price_range'].value_counts()}")
    return df


def preprocess(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded data: {df.shape}")

    df = clean(df)
    df = transform(df)
    df = reduce(df)
    df = discretize(df)

    df.to_csv("data_preprocessed.csv", index=False)
    print(f"\nPreprocessed data saved as data_preprocessed.csv")
    print(f"Final shape: {df.shape}")

    return "data_preprocessed.csv"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("provide the data path: python preprocess.py <path>")
        sys.exit(1)

    preprocessed_path = preprocess(sys.argv[1])
    os.system(f"python analytics.py {preprocessed_path}")