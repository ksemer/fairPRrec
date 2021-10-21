from subprocess import run
import subprocess
from time import time

path = "/mnt/sdb1/tsiou/wisdom2021/code/"
run(["cp", path + "python/getNetworksQualityFeatures.py", "."])
run(["cp", path + "python/getNodesQualityFeatures.py", "."])
run(["python3", "getNetworksQualityFeatures.py"])
run(["python3", "getNodesQualityFeatures.py"])

