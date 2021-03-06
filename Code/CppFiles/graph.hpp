#ifndef _GRAPH_HPP
#define _GRAPH_HPP

#include <string>
#include <vector>

using namespace std;

struct edge {
    int source;
    int target;
    int sourceOutDegree;
    double recScore, fairScore, expectedFair;

    bool operator == (const edge &other) {
        return (source == other.source && target == other.target);
    }
};

struct recEdge {
    int source;
    int target;
    int sourceOutDegree;
    double node2vecScore, resAllocScore, jaccCoefScore, prefAttScore, adamicAdarScore, gain, expGain;

    bool operator == (const edge &other) {
        return (source == other.source && target == other.target);
    }
};

typedef struct {
	vector<int> out_neighbors;
	vector<int> in_neighbors;
	vector<int> in_neighbors_per_community; // we need this just for printing
	vector<int> out_neighbors_per_community;
	int out_degree;
	int community;
} node_t;

// For topk algorithms. For binary categories.
typedef struct {
	double pagerank_for_topk; // Ratio for every single node. We multiply it by node's pagerank.
	bool is_at_topk = false;
	bool is_in_topk = false;
	double excess; // Total ratio of excess. We multiply it by node's pagerank.
	int favour_community;
	int out_topk_neighbors_per_community[2] = { 0 }; // Only for two communitites. Fix me.
	double importance_in_topk_community;
} node_topk;

typedef struct {
	vector<int> nodes;
	int community_id;
} community_t;

typedef struct {
	vector<int> nodes;
	int attribute_id;
} attribute_t;

typedef struct pagerank_s {	
	int node_id;
	double pagerank;

	bool operator < (const struct pagerank_s &other) {return (pagerank > other.pagerank);} /* to sort in descending order */
} pagerank_t;

typedef vector<pagerank_t> pagerank_v;

class graph
{
public:
	graph(const string &graph_filename, const string &com_filename);
	/* ~graph(); */

	void load_attributes(const string &attribute_filename);

	void load_community_percentage(const string &percentage_filename);
	double get_community_percentage(const int community) const;

	void add_edge(const int src_node, const int dest_node);
	void add_edges(vector<recEdge> &edges);
	void remove_edge(const int src_node, const int dest_node);
	void remove_edges(vector<recEdge> &edges);

	int get_num_nodes() const {return nnodes;}
	int get_num_edges() const {return nedges;}
	int get_num_communities() const {return ncommunities;}
	int get_in_degree(const int node_id) const;
	int get_out_degree(const int node_id) const;

	int get_community(const int node) const ;
	int count_in_neighbors_with_community(const int node_id, const int target_community);
	int count_out_neighbors_with_community(const int node_id, const int target_community);
	const vector<int> &get_out_neighbors(int node_id) const;
	const vector<int> &get_in_neighbors(int node_id) const;
	vector<double> get_pagerank_per_community(pagerank_v pagerankv) const;
	community_t *get_communities();
	int get_community_size(const int community_id);

	vector<int> &get_nodes_with_attribute(const int attribute_id);

private:

	void load_graph(const string &graph_filename);
	void load_num_nodes(const string &graph_filename);
	void load_communities(const string &com_filename);

	int nnodes;
	int nedges;
	node_t *nodes;

	int ncommunities;
	community_t *communities;
	vector<double> comm_percentage; // pagerank percentage each community should get

	int nattributes; // for personalization
	attribute_t *attributes;
};

#endif /* _GRAPH_HPP */
