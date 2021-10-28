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
       - Experiment Scripts
       - Python_files
   - Datasets
   - Notebooks

### Experiments:<br/> 
The following refers to the steps needed to compute the results reported in the paper.
Note. Each cpp and python file is documented. Please open the files for more details.
1. Compute Nodes PageRank
   1. Copy "getPageRank.out" from the Cpp_files and execute: 
      1. >`./getPagerank.out`
2. Get random source nodes and save them into "random_source_nodes.csv"
   1. copy "getSourceNodes.py" from the Python_files and execute: 
    >`python3 getSourceNodes.py -p "random" -a "source_nodes_ratio" -o "random_source_nodes.csv"`  
3. Get Candidate Edges and save them into "candidate_edges.csv"
    >`python3 getCandidateEdges.py -i random_source_nodes.csv -d "distance" -o "candidate_edges.csv"`  
4. Converts the graph file to compatible form for positive sample. We specify the graph file, the output file and the number of the sample expressed as percentage of the number of the graph's edges.
    >`python3 getPositiveEdgeSample.py -g "out_graph.txt" -p, "100", -o, "positive_edge_sample.csv`  
5. Get negative edges sample.
    >`python3 getNegativeEdgeSample.py -g "out_graph.txt" -p "100" -o "negative_edge_sample.csv`  
6. Get Node embeddings
   1. node2vec
     >`python3 getNodeEmbeddings.py -g "out_graph.txt" -p, "node2vec" --l "distance" -pp "1.0", --qp "1.0" -o, "node2vec_node_embeddings.csv`  
   2. FairWalk
      >`python3 getNodeEmbeddings.py -g "out_graph.txt" -p, "fairwalk" --l "distance" -pp "1.0", --qp "1.0" -o, "fairwalk_node_embeddings.csv`  
7. Get Edge embeddings
   1. node2vec
     * >`python3 getEdgeEmbeddings.py -l "node2vec_node_embeddings.csv" -e, "candidate_edges.csv" -p "hadamrt" -o "candidate_edges_node2vec_embeddings.csv`  
     * >`python3 getEdgeEmbeddings.py -l "node2vec_node_embeddings.csv" -e, "positive_edge_sample.csv" -p "hadamrt" -o "positive_sample_edges_node2vec_embeddings.csv` 
     * >`python3 getEdgeEmbeddings.py -l "node2vec_node_embeddings.csv" -e, "negative_edge_sample.csv" -p "hadamrt" -o "negative_sample_edges_node2vec_embeddings.csv`   
   2. FairWalk
      * >`python3 getEdgeEmbeddings.py l "fairwalk_node_embeddings.csv" -e, "candidate_edges.csv" -p "hadamrt" -o, "candidate_edges_fairwalk_embeddings.csv`  
      * >`python3 getEdgeEmbeddings.py -l "fairwalk_node_embeddings.csv" -e, "positive_edge_sample.csv" -p "hadamrt" -o "positive_sample_edges_fairwalk_embeddings.csv`  
      * >`python3 getEdgeEmbeddings.py -l "fairwalk_node_embeddings.csv" -e, "negative_edge_sample.csv" -p "hadamrt" -o "negative_sample_edges_node2vec_embeddings.csv`
8. Get node2vec and fairwalk classifier
     * >`python3 getClassifier.py -p "positive_sample_edges_node2vec_embeddings.csv" -n "negative_sample_edges_node2vec_embeddings.csv" -o "node2vec_recommender.sav"`
     * >`python3 getClassifier.py -p "positive_sample_edges_fairwalk_embeddings.csv" -n "negative_sample_edges_fairwalk_embeddings.csv" -o "fairwalk_recommender.sav"`
9. Get red absorbing probabilities
    * >`python3 getRedAbsorbingProbs.py" -g "out_graph.txt" -o "red_absorbing_probabilities.csv"`

10. Get link recommendation algorithms fairness scores
    * Adamic Adar: >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "adamic_adar" -o "adamic_adar_scores.csv"`
    * Jaccard Coefficient: >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "jaccard-coefficient" -o "jaccard_coefficient_scores.csv"`
    * Preferential Attachment: >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "preferential-attachment" -o "preferential_attachment_scores.csv"`
    * Node2vec:  >`python3 getRecommendationScores.py -i "candidate_edges_node2vec_embeddings.csv" -p "from-classifier" -o "node2vec_scores.csv"`
    * Fairwalk:  >`python3 getRecommendationScores.py -i "candidate_edges_fairwalk_embeddings.csv" -p "from-classifier" -c "fairwalk_recommender.sav" -o "node2vec_scores.csv"`
11. Get FREC, E-FREC, PREC, and E-PREC red pageranks
    * >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "fair" -o "frec.csv"`
    * >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "dyadic-fair" -o "e-frec.csv"`
    * >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "multiplicative-hybrid" -f "frec.csv" -c "node2vec_scores.csv" -o "prec.csv"`
    * >`python3 getRecommendationScores.py -i "candidate_edges.csv" -p "multiplicative-hybrid" -f "e-frec.csv" -c "node2vec_scores.csv" -o "e-prec.csv"`
12. Compute the PageRank Fairness per round
    * rounds: 10, algo_scores: the file computed in steps 10 and 11.Also have a look at `experiments_pipeline.py`
    * >`python3 experiment_one_fairness.py -r "rounds" -s "algo_scores" -o "sc_output`
13. Compute Acceptance Probability per round
    * rounds: 10, algo_scores: the file computed in steps 10 and 11.Also have a look at `experiments_pipeline.py`
    * >`python3 experiment_two_acceptance.py -r "rounds" -s "algo_scores" -n "node2vec_scores" -o "accept_prob.csv"`
14. Compute the personalized PageRank Fairness per round
    * rounds: 10, algo_scores: the file computed in steps 10 and 11.Also have a look at `experiments_pipeline.py`
    * >`python3 experiment_three_acceptance.py -r "rounds" -s "algo_scores" -o "sc_personalized_output`

 - We also included in the ExperimentScripts folder three python files that contain the execution pipeline for computing the results reported in the paper. 

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
Datasets Description.
---------
Datasets provided have been collected from various resources. They are graphs with a binary attribute for each node. Every dataset is consisted of two txt files. "out_graph.txt" and "out_community.txt".
    
"out_graph.txt" is the edge list of the graph. First line of the file is the number of the nodes. Every other line is a pair of node ids (pair of integers) separated by an empty space. line "32 46" denotes an edge from node with id 32 to node with id 46. Every edge is assumed to be directed. So if the graph is undirected for every edge "i j" there is also the edge "j i".

"out_community.txt" includes the group for every node. The first line of the file is the number of groups in the graph. Every other line is a pair of integers. First integer is a node id and the se cond integer is the group that the specific node belongs to. "34 1" denotes that node with id 43 belongs to group 1.

Nodes' ids should be from 0 to n without missing numbers. The same holds for groups' ids.

**All above conventions are important for the proper function of the algorithms.**

In the datasets provided we have done the forth mentioned preprocessing. In cases where nodes in the graph hadn't have group information we removed them from the graph. We have also kept only the largest weak component of each graph.

#### Notebooks contain the code for exporting the plots and constructing the latex tables.
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
