import sys
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# groups users into behavior clusters using K-Means

def cluster(filepath):
    df = pd.read_csv(filepath)
    user_profile = df.groupby('user_id').agg(
        total_events  = ('event_type', 'count'),
        views         = ('event_type', lambda x: (x == 'view').sum()),
        cart_adds     = ('event_type', lambda x: (x == 'cart').sum()),
        purchases     = ('event_type', lambda x: (x == 'purchase').sum()),
        avg_price     = ('price', 'mean'),
        unique_products = ('product_id', 'nunique')
    ).reset_index()

    print(f"User profiles built: {user_profile.shape[0]} users")

    features = ['total_events', 'views', 'cart_adds', 'purchases', 'avg_price', 'unique_products']
    scaler = StandardScaler()
    scaled = scaler.fit_transform(user_profile[features])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    user_profile['cluster'] = kmeans.fit_predict(scaled)

    cluster_counts = user_profile['cluster'].value_counts().sort_index()

    cluster_summary = user_profile.groupby('cluster')[features].mean().round(2)

    output = f"""K-Means Clustering Results (k=4)
Users per cluster:
{cluster_counts.to_string()}

Cluster profiles (average behavior):
{cluster_summary.to_string()}

Cluster interpretation:
  Cluster with highest purchases = Serious Buyers
  Cluster with high views but low purchases = Window Shoppers
  Cluster with high cart_adds but low purchases = Hesitant Buyers
  Cluster with low activity overall = Casual Browsers
"""

    with open("clusters.txt", "w") as f:
        f.write(output)

    print("clusters.txt saved")
    print(f"\nUsers per cluster:\n{cluster_counts}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cluster.py <path>")
        sys.exit(1)

    cluster(sys.argv[1])