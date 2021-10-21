""" Pipeline for the computation of the fairwalk scores.

Run after pre_experiments_pipeline.py
"""
from subprocess import run
import subprocess
from time import time


# Path to the code.
path = "/mnt/sdb1/tsiou/wisdom2021/code/"
# Ratio for source nodes. 10 = 10%
source_nodes_ratio = 10
# Distance for embedings.
distance = "2"


# Get fairwalk node embeddings.
print("Get fairwalk node embeddings")
run(
    [
        "python3",
        "getNodeEmbeddings.py",
        "-g",
        "out_graph.txt",
        "-p",
        "fairwalk",
        "--l",
        distance,
        "--pp",
        "1.0",
        "--qp",
        "1.0",
        "-o",
        "fairwalk_node_embeddings.csv",
    ]
)

# Get candidate edges fairwalk embeddings.
print("Get fairwalk edge embeddings")
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "fairwalk_node_embeddings.csv",
        "-e",
        "candidate_edges.csv",
        "-p",
        "hadamart",
        "-o",
        "candidate_edges_fairwalk_embeddings.csv",
    ]
)

# Get positive edge sample fairwalk embeddings.
print("Get positive edge sample fairwalk embeddings")
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "fairwalk_node_embeddings.csv",
        "-e",
        "positive_edge_sample.csv",
        "-p",
        "hadamart",
        "-o",
        "positive_sample_edges_fairwalk_embeddings.csv",
    ]
)

# Get negative edge sample fairwalk embeddings.
print("Get negative edge sample fairwalk embeddings")
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "fairwalk_node_embeddings.csv",
        "-e",
        "negative_edge_sample.csv",
        "-p",
        "hadamart",
        "-o",
        "negative_sample_edges_fairwalk_embeddings.csv",
    ]
)

# Get fairwalk classifier.
print("Get fairwalk classifier")
run(
    [
        "python3",
        "getClassifier.py",
        "-p",
        "positive_sample_edges_fairwalk_embeddings.csv",
        "-n",
        "negative_sample_edges_fairwalk_embeddings.csv",
        "-o",
        "fairwalk_recommender.sav",
    ]
)

# Get fairwalk scores.
print("Get fairwalk scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges_fairwalk_embeddings.csv",
        "-p",
        "from-classifier",
        "-c",
        "fairwalk_recommender.sav",
        "-o",
        "fairwalk_scores.csv",
    ]
)
