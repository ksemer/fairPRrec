#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <cmath>
#include "graph.hpp"
#include "pagerank.hpp"
#include "edge_add.hpp"



static bool get_options(const int argc, char ** const argv, algorithm_mode &algo_mode, int &n_source, int &n_target) {
    if (argc != 6 && argc != 2) goto error;
    if (!std::strcmp(argv[1], "-gd") && !std::strcmp(argv[2], "-s") && !std::strcmp(argv[4], "-t")) {
        algo_mode = algorithm_mode::GREEDY;
        n_source = std::atoi(argv[3]);
        n_target = std::atoi(argv[5]);
    } else {
        goto error;
    }
    return true;

error:
	std::cerr << "Usage: " << argv[0] << " [options]\n"
		"Options:\n"
		"-gd -s <number of source nodes> -t <number of target nodes>\t\t\t Greedy \n"
		"-fgd -s <number of source nodes> -t <number of target nodes>\t\t\t Fast Greedy\n"
		"-apx -s <number of source nodes> -t <number of target nodes>\t\t\t  Approximation\n"
		"-fapx -s <number of source nodes> -t <number of target nodes>\t\t\t Fast Approximation\n"
		"-rsrc -s <number of source nodes> -t <number of target nodes>\t\t\t Random Source nodes\n"
		"-srcst -s <number of source nodes> -t <number of target nodes>\t\t\t Sources Statistics\n"
		"-tarst -s <number of source nodes> -t <number of target nodes>\t\t\t Target Statistics\n"
		"-ota \t\t\t One to All" << std::endl;
	return false;
}

int main(int argc, char **argv) {
    // Init arguments.
    algorithm_mode algo_mode;
    int n_source = 1;
    int n_target = 1;
    if (!get_options(argc, argv, algo_mode, n_source, n_target)) return 1;

    // Init graph and algorithms.
    graph g("out_graph.txt", "out_community.txt");
    pagerank_algorithms algs(g);
    Edge_addition link_rec(g, algs, n_source, n_target);

    // Precision testing.
    //check_precision_effect(link_rec);
    /*
    switch (algo_mode)
    {
    case algorithm_mode::GREEDY :
        link_rec.greedy_per_one();
        link_rec.greedy_all();
        break;
    case algorithm_mode::FAST_GREEDY :
        link_rec.fast_greedy_per_one();
        link_rec.fast_greedy_all();
        break;
    case algorithm_mode::RANDOM :
        for (int exp = 0; exp < 10; exp++) {
            link_rec.random_edges(exp);
        }
        break;
    case algorithm_mode::RAND_SRC :
        link_rec.random_sources_per_one();
        link_rec.random_sources_all();
        break;
    case algorithm_mode::ONE_TO_ALL_G :
        link_rec.one_to_all_greedy();
        break;
    case algorithm_mode::ONE_TO_ALL_FG :
        link_rec.one_to_all_fast_greedy();
        break;
    case algorithm_mode::ONE_TO_ALL_R :
        link_rec.one_to_all_random();
        break;
    case algorithm_mode::SRC_ST :
        link_rec.source_stats();
        link_rec.targets_stats();
        break;
    case algorithm_mode::TAR_ST :
        link_rec.targets_stats();
        break;
    default:
        std::cout << "Not supported yet\n";
        return 1;
    }
    */
   std::cout << "oal kala?? \n";
}