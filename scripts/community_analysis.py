import collections as col
import scipy.stats as st
import networkx as nx

def prepare_community_stats(partition, labeled_papers, graph):
    community_stats = col.defaultdict(lambda: {
        'count': 0,
        'subfields': col.defaultdict(int), 
        'edge_density': 0,
        'avg_clustering': 0,
        'avg_degree_centrality': 0,
        'avg_betweenness_centrality': 0
    })


    # Global metrics
    global_edge_density = nx.density(graph)
    global_clustering_coefficient = nx.average_clustering(graph)
    global_degree_centrality = nx.degree_centrality(graph)
    global_betweenness_centrality = nx.betweenness_centrality(graph)

    for paper_id, community_id in partition.items():
        community_stats[community_id]['count'] += 1
        subfields = labeled_papers.get(paper_id, ["Unknown"])
        for subfield in subfields:
            community_stats[community_id]['subfields'][subfield] += 1

    for community_id, stats in community_stats.items():
        subgraph = graph.subgraph([node for node, comm in partition.items() if comm == community_id])
        stats['edge_density'] = nx.density(subgraph)
        stats['avg_clustering'] = nx.average_clustering(subgraph)
        stats['avg_degree_centrality'] = sum(global_degree_centrality[node] for node in subgraph.nodes()) / len(subgraph.nodes())
        stats['avg_betweenness_centrality'] = sum(global_betweenness_centrality[node] for node in subgraph.nodes()) / len(subgraph.nodes())

    global_stats = {
        'global_edge_density': global_edge_density,
        'global_clustering_coefficient': global_clustering_coefficient,
        'global_avg_degree_centrality': sum(global_degree_centrality.values()) / len(graph.nodes()),
        'global_avg_betweenness_centrality': sum(global_betweenness_centrality.values()) / len(graph.nodes())
    }


    return community_stats, global_stats



def perform_fisher_analysis(community_stats, labeled_papers, total_papers):
    """
    Calculates Fisher's Exact Test for each community and subfield.
    
    Args:
        community_stats (dict): Community statistics with subfield counts.
        labeled_papers (dict): Mapping from paper IDs to their assigned subfields.
        total_papers (int): Total number of papers.
    
    Returns:
        dict: Updated community statistics with Fisher's test results.
    """
    overall_counts = calculate_overall_subfield_counts(labeled_papers)
    for community_id, stats in community_stats.items():
        fisher_results = {}
        community_size = stats['count']
        for subfield, count_in_community in stats['subfields'].items():
            count_outside_community = overall_counts[subfield] - count_in_community
            non_subfield_community = community_size - count_in_community
            non_subfield_outside = total_papers - community_size - count_outside_community
            table = [[count_in_community, count_outside_community], [non_subfield_community, non_subfield_outside]]
            odds_ratio, p_value = st.fisher_exact(table)  # corrected use of scipy.stats
            fisher_results[subfield] = {'odds_ratio': odds_ratio, 'p_value': p_value}
        stats['fisher_results'] = fisher_results
    return community_stats

def calculate_overall_subfield_counts(labeled_papers):
    """
    Calculates the total counts of each subfield across all papers.
    
    Args:
        labeled_papers (dict): Mapping from paper IDs to their assigned subfields.
    
    Returns:
        dict: Total counts of each subfield.
    """
    total_counts = col.defaultdict(int)
    for subfields in labeled_papers.values():
        for subfield in subfields:
            total_counts[subfield] += 1
    return total_counts
