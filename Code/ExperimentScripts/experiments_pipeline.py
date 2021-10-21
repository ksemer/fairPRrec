from subprocess import run
import subprocess
from time import time


rounds = "10"
distance = "4"
path = "/mnt/sdb1/tsiou/wisdom2021/code/"

# 23. Run Experiment Score and Acceptance probabilities
# run(["cp", path + "ExperimentScripts/experiment_one_fairness.py", "."])
# run(["cp", path + "ExperimentScripts/experiment_two_acceptance.py", "."])
# run(["cp", path + "ExperimentScripts/experiment_three_personalized.py", "."])
scores_files = [
    "fair",
    "adamic_adar",
    "jaccard_coefficient",
    "resource_allocation",
    "preferential_attachment",
    "node2vec",
    "fairwalk",
    "hybrid_node2vec",
    "dyadic_fair",
    "hybrid_balanced_node2vec",
    "random",
]

print("Run experiment one.")
for sf in scores_files:
    cp = run(
        [
            "python3",
            "experiment_one_fairness.py",
            "-r",
            rounds,
            "-s",
            f"{sf}_scores.csv",
            "-o",
            f"sc_{sf}.csv",
        ]
    )

print("Run experiment two.")
for sf in scores_files:
    cp = run(
        [
            "python3",
            "experiment_two_acceptance.py",
            "-r",
            rounds,
            "-s",
            f"{sf}_scores.csv",
            "-n",
            "node2vec_scores.csv",
            "-o",
            f"accept_prob_{sf}.csv",
        ]
    )

print("Run experiment three.")
for sf in scores_files:
    cp = run(
        [
            "python3",
            "experiment_three_personalized.py",
            "-r",
            rounds,
            "-s",
            f"{sf}_scores.csv",
            "-o",
            f"sc_personalized_{sf}.csv",
        ]
    )

# 24 deletion edges.
print("Get deletion scores.")
run(["cp", path + "cpp/get_deletion_scores.out", "."])
run(["./get_deletion_scores.out", "."])
