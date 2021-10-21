""" Basic pipeline for the computation of the recommendation scores.
"""
from subprocess import run
import subprocess
from time import time


# Path to the code.
path = "/mnt/sdb1/tsiou/wisdom2021/code/"
# Ratio for source nodes. 10 = 10%
source_nodes_ratio = 10
# Distance for embedings.
distance = "4"

# Get PageRank.
print("Get PageRank")
run(["cp", path + "cpp/getPagerank.out", "."])
cp = run(["./getPagerank.out"])

# Get source nodes.
print("Get source nodes")
run(["cp", path + "python/getSourceNodes.py", "."])
run(
    [
        "python3",
        "getSourceNodes.py",
        "-p",
        "random",
        "-a",
        str(source_nodes_ratio),
        "-o",
        "random_source_nodes.csv",
    ]
)
# cp = run(["python3", "getSourceNodes.py", "-p", "best-pagerank", "-a", rounds, "-o", "best_by_pagerank_nodes.csv"])
# cp = run(["python3", "getSourceNodes.py", "-p", "worst-pagerank", "-a", rounds, "-o", "worst_by_pagerank_nodes.csv"])

# Get candidate edges.
print("Get candidate edges")
run(["cp", path + "python/getCandidateEdges.py", "."])
run(
    [
        "python3",
        "getCandidateEdges.py",
        "-i",
        "random_source_nodes.csv",
        "-d",
        distance,
        "-o",
        "candidate_edges.csv",
    ]
)

# Get positive edge sample.
print("Get positive edge sample")
run(["cp", path + "python/getPositiveEdgeSample.py", "."])
run(
    [
        "python3",
        "getPositiveEdgeSample.py",
        "-g",
        "out_graph.txt",
        "-p",
        "100",
        "-o",
        "positive_edge_sample.csv",
    ],
    universal_newlines=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Get negative edges sample.
print("Get negative edge sample")
run(["cp", path + "python/getNegativeEdgeSample.py", "."])
run(
    [
        "python3",
        "getNegativeEdgeSample.py",
        "-g",
        "out_graph.txt",
        "-p",
        "100",
        "-o",
        "negative_edge_sample.csv",
    ]
)

# Get node2vec node embeddings.
print("Get node2vec node embeddings")
run(["cp", path + "python/getNodeEmbeddings.py", "."])
run(
    [
        "python3",
        "getNodeEmbeddings.py",
        "-g",
        "out_graph.txt",
        "-p",
        "node2vec",
        "--l",
        distance,
        "--pp",
        "1.0",
        "--qp",
        "1.0",
        "-o",
        "node2vec_node_embeddings.csv",
    ]
)

# Get fairwalk node embeddings.
"""
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
"""

# Get candidates edges node2vec embeddings.
print("Get node2vec edge embeddings")
run(["cp", path + "python/getEdgeEmbeddings.py", "."])
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "node2vec_node_embeddings.csv",
        "-e",
        "candidate_edges.csv",
        "-p",
        "hadamart",
        "-o",
        "candidate_edges_node2vec_embeddings.csv",
    ]
)

# Get candidate edges fairwalk embeddings.
"""
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
"""

# 9. Get positive edge sample node2vec embeddings.
print("Get positive edge sample node2vec embeddings")
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "node2vec_node_embeddings.csv",
        "-e",
        "positive_edge_sample.csv",
        "-p",
        "hadamart",
        "-o",
        "positive_sample_edges_node2vec_embeddings.csv",
    ]
)

# Get positive edge sample fairwalk embeddings.
"""
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
"""

# Get negative edge sample node2vec embeddings.
print("Get negative edge sample node2vec embeddings")
run(
    [
        "python3",
        "getEdgeEmbeddings.py",
        "-i",
        "node2vec_node_embeddings.csv",
        "-e",
        "negative_edge_sample.csv",
        "-p",
        "hadamart",
        "-o",
        "negative_sample_edges_node2vec_embeddings.csv",
    ]
)

# Get negative edge sample fairwalk embeddings.
"""
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
"""

# Get node2vec classifier.
print("Get node2vec classifier")
run(["cp", path + "python/getClassifier.py", "."])
run(
    [
        "python3",
        "getClassifier.py",
        "-p",
        "positive_sample_edges_node2vec_embeddings.csv",
        "-n",
        "negative_sample_edges_node2vec_embeddings.csv",
        "-o",
        "node2vec_recommender.sav",
    ]
)

# Get fairwalk classifier.
"""
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
"""

# Get red absorbing probabilities.
print("Get red absorbing probabilites.")
run(["cp", path + "python/getRedAbsorbingProbs.py", "."])
run(
    [
        "python3",
        "getRedAbsorbingProbs.py",
        "-g",
        "out_graph.txt",
        "-o",
        "red_absorbing_probabilities.csv",
    ]
)

# Get Adamic Adar scores.
print("Get adamic adar scores")
run(["cp", path + "python/getRecommendationScores.py", "."])
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "adamic-adar",
        "-o",
        "adamic_adar_scores.csv",
    ]
)

# Get Jaccard coefficient scores.
print("Get jaccard coefficient scores")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "jaccard-coefficient",
        "-o",
        "jaccard_coefficient_scores.csv",
    ]
)

# Get resource allocation scores.
print("Get resource allocation scores")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "resource-allocation",
        "-o",
        "resource_allocation_scores.csv",
    ]
)

# Get preferencial attachment scores.
print("Get prerferential attachment scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "preferential-attachment",
        "-o",
        "preferential_attachment_scores.csv",
    ]
)

# Get node2vec scores.
print("Get node2vec scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges_node2vec_embeddings.csv",
        "-p",
        "from-classifier",
        "-c",
        "node2vec_recommender.sav",
        "-o",
        "node2vec_scores.csv",
    ]
)

# Get fairwalk scores.
"""
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
"""

# Get fair scores.
print("Get fair scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "fair",
        "-o",
        "fair_scores.csv",
    ]
)

# Get sum fair scores.
print("Get sum fair scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "sum-fair",
        "-o",
        "sum_fair_scores.csv",
    ]
)

# Get dyadic fair scores.
print("Get dyadic fair scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "dyadic-fair",
        "-o",
        "dyadic_fair_scores.csv",
    ]
)

# Get multiplicative hybrid node2vec scores.
print("Get hybrid scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "multiplicative-hybrid",
        "-f",
        "fair_scores.csv",
        "-c",
        "node2vec_scores.csv",
        "-o",
        "hybrid_node2vec_scores.csv",
    ]
)

# Get multiplicative hybrid node2vec scores.
print("Get balanced hybrid scores.")
run(
    [
        "python3",
        "getRecommendationScores.py",
        "-i",
        "candidate_edges.csv",
        "-p",
        "multiplicative-hybrid",
        "-f",
        "dyadic_fair_scores.csv",
        "-c",
        "node2vec_scores.csv",
        "-o",
        "hybrid_balanced_node2vec_scores.csv",
    ]
)