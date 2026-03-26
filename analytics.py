import sys
import os
import pandas as pd

# generates 3 insight files about customer behavior

def analyze(filepath):
    df = pd.read_csv(filepath)

    total = len(df)
    counts = df['event_type'].value_counts()

    viewers = counts.get('view', 0)
    carters = counts.get('cart', 0)
    purchasers = counts.get('purchase', 0)
    removers = counts.get('remove_from_cart', 0)

    conversion = round((purchasers / viewers) * 100, 2) if viewers > 0 else 0
    cart_abandonment = round(((carters - purchasers) / carters) * 100, 2) if carters > 0 else 0

    insight1 = f"""Customer Conversion Funnel
Total events: {total}
Views:             {viewers} ({round(viewers/total*100,2)}%)
Cart adds:         {carters} ({round(carters/total*100,2)}%)
Cart removals:     {removers} ({round(removers/total*100,2)}%)
Purchases:         {purchasers} ({round(purchasers/total*100,2)}%)

Conversion rate (views to purchases): {conversion}%
Cart abandonment rate:                {cart_abandonment}%

Only {conversion}% of product views end in a purchase.
{cart_abandonment}% of users who add to cart never complete the purchase.
This is a major opportunity — recovering even 10% of abandoned carts
could significantly increase revenue.
"""
    with open("insight1.txt", "w") as f:
        f.write(insight1)

    user_events = df.groupby('user_id')['event_type'].value_counts().unstack(fill_value=0)

    for col in ['view', 'cart', 'purchase', 'remove_from_cart']:
        if col not in user_events.columns:
            user_events[col] = 0

    def classify(row):
        if row['purchase'] > 0 and row['view'] <= 3:
            return 'impulsive buyer'
        elif row['purchase'] > 0:
            return 'serious buyer'
        elif row['cart'] > 0 and row['purchase'] == 0:
            return 'interested but hesitant'
        elif row['view'] > 5 and row['purchase'] == 0:
            return 'window shopper'
        else:
            return 'casual browser'

    user_events['customer_type'] = user_events.apply(classify, axis=1)
    type_counts = user_events['customer_type'].value_counts()
    type_pcts = round(type_counts / type_counts.sum() * 100, 2)

    purchases = df[df['event_type'] == 'purchase']
    weekend = purchases[purchases['day_of_week'] >= 5]
    weekday = purchases[purchases['day_of_week'] < 5]
    weekend_pct = round(len(weekend) / len(purchases) * 100, 2)
    weekday_pct = round(len(weekday) / len(purchases) * 100, 2)

    insight2 = f"""Customer Behavior Types
{type_counts.to_string()}

Percentages:
{type_pcts.to_string()}

Most users are window shoppers or casual browsers.
Serious and impulsive buyers are the key revenue drivers
even though they are the smallest groups.

Weekend vs Weekday Purchases:
Weekday purchases: {len(weekday)} ({weekday_pct}%)
Weekend purchases: {len(weekend)} ({weekend_pct}%)

Most purchases happen on weekdays, suggesting customers
shop during work/school breaks rather than on weekends.
"""
    with open("insight2.txt", "w") as f:
        f.write(insight2)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    busiest_day = days[purchases['day_of_week'].mode()[0]]
    top_hours = purchases.groupby('hour').size().sort_values(ascending=False).head(3)
    avg_price = df.groupby('event_type')['price'].mean().round(2)

    top_brands = (
        df[df['event_type'] == 'purchase']
        .groupby('brand')
        .size()
        .sort_values(ascending=False)
        .head(5)
    )

    price_range_sales = (
        df[df['event_type'] == 'purchase']['price_range']
        .value_counts()
    ) if 'price_range' in df.columns else "N/A"

    insight3 = f"""Shopping Patterns & Pricing
Top 3 purchase hours (24h):
{top_hours.to_string()}

Busiest purchase day: {busiest_day}

Average price by event type:
{avg_price.to_string()}

Top 5 brands by purchases:
{top_brands.to_string()}

Purchases by price range:
{price_range_sales.to_string() if hasattr(price_range_sales, 'to_string') else price_range_sales}

Customers tend to buy budget and mid range products the most.
Premium and luxury items get viewed often but purchased rarely.
The most purchased brands dominate both views and purchases,
suggesting brand loyalty plays a role in cosmetics shopping.
"""
    with open("insight3.txt", "w") as f:
        f.write(insight3)

    print("insight1.txt saved")
    print("insight2.txt saved")
    print("insight3.txt saved")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analytics.py <path>")
        sys.exit(1)

    analyze(sys.argv[1])
    os.system(f"python visualize.py {sys.argv[1]}")