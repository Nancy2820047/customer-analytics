# Cosmetics Store (Customer Behavior Analysis Pipeline) 

This project builds a full data pipeline to analyze customer behavior 
from a cosmetics eCommerce store. We use real event data from November 
and December 2019 to classify customers, spot shopping patterns, and 
group users by behavior using K-Means clustering.

---

## Team Members

Nancy Ahmed Mohamed 231000470
Habiba Bahbah   231001544 
Yasmin Ahmed   231000088  
Habiba Ayman   231000939

---

## Dataset

- **Source:** eCommerce Events History in Cosmetics Shop (Kaggle)
- **Period:** November and December 2019
- **Size:** 258,000 events after combining both months
- **Event types:** view, cart, remove_from_cart, purchase

---

## Project Structure

customer-analytics/
├── Dockerfile
├── ingest.py
├── preprocess.py
├── analytics.py
├── visualize.py
├── cluster.py
├── summary.sh
├── README.md
└── results/

---

## Pipeline Flow

ingest.py → preprocess.py → analytics.py → visualize.py → cluster.py

Each script calls the next one automatically and passes the latest CSV as an argument.

1. **ingest.py**: loads the raw dataset and saves it as `data_raw.csv`
2. **preprocess.py**: cleans, transforms, and prepares the data, saves as `data_preprocessed.csv`
3. **analytics.py**: generates 3 text files with insights about customer behavior
4. **visualize.py**: creates 3 plots and saves them as `summary_plot.png`
5. **cluster.py**: applies K-Means clustering on user profiles, saves results to `clusters.txt`

---

## How to Run

### 1. Build the Docker image
```bash
docker build -t cosmetics-pipeline .
```

### 2. Run the container
```bash
docker run -it --name cosmetics-container cosmetics-pipeline
```

### 3. Inside the container, start the pipeline
```bash
python ingest.py nov_dec_combined.csv
```

### 4. Open a new terminal on your machine and run summary.sh
```bash
bash summary.sh
```

This copies all output files into `results/` on your machine, 
then stops and removes the container.

---

## Outputs

`data_raw.csv` : Raw copy of the original dataset 
`data_preprocessed.csv` :Cleaned and transformed data ready for analysis 
`insight1.txt`: Customer conversion funnel views vs purchases 
`insight2.txt` : Customer behavior types and weekend vs weekday patterns 
`insight3.txt` : Peak shopping hours, top brands, and pricing analysis 
`summary_plot.png` : Price histogram, correlation heatmap, top brands chart 
`clusters.txt` : K-Means clustering results with user segments 

---

## Preprocessing Steps

 **Cleaning:** dropped 15,107 duplicate rows, removed negative prices, filled missing brand values with "unknown"
 **Transformation:** converted event_time to datetime and extracted hour and day, label encoded event_type, scaled price using MinMaxScaler
 **Dimensionality Reduction:** dropped category_code (98% missing), category_id, and user_session
 **Discretization:** binned price into four ranges budget (0–5), mid (5–20), premium (20–60), luxury (60+)

---

## Clustering Results

We built a profile for each user based on their activity then applied K-Means with 4 clusters:

| Cluster | Size | Type |
| 0 | 29,122 | Casual Browsers |
| 1 | 173 | Power Buyers |
| 2 | 2,021 | Regular Buyers |
| 3 | 1,732 | Luxury Browsers |

---

## Screenshots

### Pipeline Execution


### Visualization Output


### Results Folder
