#!/bin/bash

# copies all output files from the container to the host
# then stops and removes the container

HOST_DIR="$(pwd)/results"
mkdir -p "$HOST_DIR"

echo "Copying output files"

docker cp cosmetics-container:/app/pipeline/data_raw.csv "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/data_preprocessed.csv "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/insight1.txt "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/insight2.txt "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/insight3.txt "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/clusters.txt "$HOST_DIR/"
docker cp cosmetics-container:/app/pipeline/summary_plot.png "$HOST_DIR/"

echo "All files copied to $HOST_DIR"

echo "Stopping and removing container"
docker stop cosmetics-container
docker rm cosmetics-container

echo "finished"
