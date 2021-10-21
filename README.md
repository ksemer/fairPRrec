## fairPRrec

This repository has been created to distribute freely our implementations of the algorithms described in the "Link Recommendations for PageRank Fairness" paper. It also includes the datasets described and used in the forthmentioned paper plus some extra dataset from various resources.

### Dependencies:<br/>
- Python 3.
- C++ 11.
- Optional Compiler that supports openmmp.

    **Note:** make file is for gcc with openmp.

All the experiments were made in linux Ubuntu. To compile cpp we used gcc compiler.

### Repository Structure:<br/>
   - Code
       - Cpp_files
       - Python_files
   - Datasets
   - Experiments

### Experiments:<br/> 
The following refers to the steps needed to compute the results reported in the paper.
Note. Each cpp and python file is documented. Please open the files for more details.
1. Compute Nodes PageRank
   1. Copy "getPageRank.out" from the Cpp_files and execute: 
      1. >`./getPagerank.out`
2. Get random source nodes and save them into "random_source_nodes.csv"
   1. copy "getSourceNodes.py" from the Python_files and execute: 
      1. >`python3 getSourceNodes.py -p "random" -a "source_nodes_ratio" -o "random_source_nodes.csv"`  
3. Get Candidate Edges and save them into "candidate_edges.csv"
      1. >`python3 getCandidateEdges.py -i random_source_nodes.csv -d "distance" -o "candidate_edges.csv"`  
4. Converts the graph file to compatible form for positive sample. We specify the graph file, the output file and the number of the sample expressed as percentage of the number of the graph's edges.
      1. >`python3 getPositiveEdgeSample.py -g "out_graph.txt" "-p", "100", "-o", "positive_edge_sample.csv`  
5. Get negative edges sample.
      1. >`python3 getNegativeEdgeSample.py -g "out_graph.txt" "-p", "100", "-o", "negative_edge_sample.csv`  

We also included in the Experiments folder three python files that contain the execution pipeline for computing the results reported in the paper. 

* Pre experiments script.

    Computes the following:
    
    1. Initial pagerank.
    2. Red absorbing probabilities.
    3. Node2vec Classifier.
    4. Node2vec embeddings.
    5. Source nodes (10% random, 100 best red, 100 best blue).
    6. Edges' scores.
    7. Candidate edges distances.
    8. Network's quality features.
    9. Groups' quality features.
    10. Nodes' quality features.
    11. Time for each of the above.

* Experiments script.

    Execute the following:

    1. Experiment one:

        Compares the impact of the different policies of recommending edges in 10 rounds. 1 round is the addition of 1 edge to all source nodes.

    1. Experiment two:

        Computes Acceptance Probabilities

    1. Experiment three:

        Computes the red personalized pagerank for each round.
   



1. Experiment Zero: Compares  greedy with fast greedy algorithm for single source. It computes red pagerank ratio rise for both algorithms for 100 random source nodes and the 100 best by initial pagerank nodes. Then it takes the average red pagerank ratio for the two groups. For each source node it creates two files: "<node_id>_redPagerankGreedy.txt" and "<node_id>_redPagerankFastGreedy.txt".
    
    - Compile:
        >` g++ --std=c++11 -Wall -Wextra -O3 -fopenmp -o experimentZero.out graph.cpp pagerank.cpp experimentZero.cpp`

    - Execute: 
        >` ./experimentZero.out`

    **Note:** We then take the average red pagerank ratio for each group (random, best by pagerank).

2. Experiment Two: Compares the effect of adding edges based on recommendation score, on greatest red pagerank gain score (fast greedy algorithm) or on greatest expected red pagerank gain in average recommendation score, networks red pagerank ratio and expected red pagerank gain. It computes the forth mentioned scores for 100 random source nodes, for the 100 best by pagerank nodes and takes the average of them for each group (random, by pagerank).

    - Compile:
        >` g++ --std=c++11 -Wall -Wextra -O3 -fopenmp -o experimentTwo.out graph.cpp pagerank.cpp experimentTwo.cpp`

    - Execute: 
        >` ./experimentTwo.out`

3. Fast greedy single source (independent executable):
    
    - Compile:
        >` g++ --std=c++11 -Wall -Wextra -O3 -fopenmp -o singleSourceFastGreedy.out graph.cpp pagerank.cpp edgeAddition.cpp singleSourceFastGreedy.cpp`

    - Execute: 
        >` ./singleSourceFastGreedy.out -s <source node id\> -n <numberOfEdges\>`

    **Note:** You will also find the algorithm as a static method in EdgeAddition class



* Post experiment script.

    Computes the following:

    1. Selected edges distances.

* Analysis script.

    Produces the following:

    1. Pending.

Datasets Description.
---------
Datasets provided have been collected from various resources. They are graphs with a binary attribute for each node. Every dataset is consisted of two txt files. "out_graph.txt" and "out_community.txt".
    
"out_graph.txt" is the edge list of the graph. First line of the file is the number of the nodes. Every other line is a pair of node ids (pair of integers) separated by an empty space. line "32 46" denotes an edge from node with id 32 to node with id 46. Every edge is assumed to be directed. So if the graph is undirected for every edge "i j" there is also the edge "j i".

"out_community.txt" includes the group for every node. The first line of the file is the number of groups in the graph. Every other line is a pair of integers. First integer is a node id and the se cond integer is the group that the specific node belongs to. "34 1" denotes that node with id 43 belongs to group 1.

Nodes' ids should be from 0 to n without missing numbers. The same holds for groups' ids.

**All above conventions are important for the proper function of the algorithms.**

In the datasets provided we have done the forth mentioned preprocessing. In cases where nodes in the graph hadn't have group information we removed them from the graph. We have also kept only the largest weak component of each graph.

### Datasets:

1. Blogs

    A directed network of hyperlinks between weblogs on US politic. You can find more informations about this dataset here: L. A. Adamic and N. S. Glance. 2005. The political blogosphere and the 2004 U.S. election: divided they blog. In LinkKDD.

1. Books

    A network of books about US politics where edges 1 between books represented co-purchasing. You can find the original dataset here: http://www-personal.umich.edu/~mejn/netdata/.

1. DBLP-GENDER

    An author collaboration network constructed
from DBLP with a subset of data mining and database conferences
from 2011 to 2020 with gender as the protected
attribute the value of which is inferred using the python
gender guesser package.

1. DBLP-PUB

    The same network as dblp-gender but with the
protected group being the set of authors whose first publication
appears in 2016.
    
1. Twitter

    A political retweet graph from "Ryan A. Rossi and Nesreen K. Ahmed. 2015. The Network Data Repository with InteractiveGraphAnalyticsandVisualization.InAAAI.  You can find the original dataset here: http://networkrepository.com"
