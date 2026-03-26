import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# creates 3 meaningful plots and saves as summary_plot.png

def visualize(filepath):
    df = pd.read_csv(filepath)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Cosmetics Store - Customer Behavior Analysis', fontsize=14)

    # histogram of price distribution
    axes[0].hist(df['price'], bins=50, color='steelblue', edgecolor='white')
    axes[0].set_title('Price Distribution')
    axes[0].set_xlabel('Price ($)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_xlim(0, 100)

    # correlation heatmap of numeric columns
    numeric_cols = df[['price', 'hour', 'day_of_week', 'event_type_encoded', 'price_scaled']]
    corr = numeric_cols.corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1])
    axes[1].set_title('Correlation Heatmap')

    # top 10 brands by purchases
    top_brands = (
        df[df['event_type'] == 'purchase']
        .groupby('brand')
        .size()
        .sort_values(ascending=False)
        .head(10)
    )
    sns.barplot(x=top_brands.values, y=top_brands.index, ax=axes[2], palette='muted')
    axes[2].set_title('Top 10 Brands by Purchases')
    axes[2].set_xlabel('Number of Purchases')
    axes[2].set_ylabel('Brand')

    plt.tight_layout()
    plt.savefig('summary_plot.png', dpi=150)
    print("summary_plot.png saved")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <path>")
        sys.exit(1)

    visualize(sys.argv[1])
    os.system(f"python cluster.py {sys.argv[1]}")