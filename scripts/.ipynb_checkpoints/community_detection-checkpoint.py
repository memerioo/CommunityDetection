import networkx as nx
import infomap
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import random
import scipy.spatial as sp

def detect_communities_infomap(citation_graph):
    """
    Detect communities in the citation graph using the Infomap algorithm.

    Args:
        citation_graph (nx.Graph): The citation graph.

    Returns:
        dict: A dictionary where keys are nodes and values are community labels.
    """
    infomap_instance = infomap.Infomap()

    # Convert nodes to integers and add edges to the Infomap instance
    node_to_int = {node: idx for idx, node in enumerate(citation_graph.nodes())}
    int_to_node = {idx: node for node, idx in node_to_int.items()}

    for u, v in citation_graph.edges():
        infomap_instance.add_link(node_to_int[u], node_to_int[v])

    # Run the Infomap algorithm
    infomap_instance.run()

    # Retrieve the partition without calling nodes as a function
    partition = {int_to_node[node.node_id]: node.module_id for node in infomap_instance.nodes}
    return partition



def analyze_community_subfields(communities, metadata):
    """
    Analyzes the subfields of the papers in each community based on provided metadata.

    Args:
        communities (dict): Paper IDs mapped to community labels.
        metadata (dict): Paper IDs mapped to metadata that includes subfield labels.

    Returns:
        dict: Community labels mapped to lists of subfields for each paper in that community.
    """
    community_subfields = defaultdict(list)
    
    for paper_id, community in communities.items():
        subfield = metadata.get(paper_id, {}).get('subfield', 'Unknown')
        community_subfields[community].append(subfield)
    
    return community_subfields


def visualize_communities_advanced(graph, partition, community_stats, num_communities_to_label=10, degree_threshold=40):
    """
    Visualizes the network graph with nodes colored by community using distinct random colors.

    Args:
        graph (nx.Graph): The graph to visualize.
        partition (dict): Node-community mapping.
        community_stats (dict): Statistics about each community, including dominant subfield.
        num_communities_to_label (int): Number of communities to label in the legend.
        degree_threshold (int): Threshold of nodes degree for showing in the visualization.
    """
    # Apply a threshold to filter nodes
    filtered_nodes = [node for node in graph.nodes() if graph.degree(node) > degree_threshold]
    subgraph = graph.subgraph(filtered_nodes)
    pos = nx.kamada_kawai_layout(subgraph)  

    plt.figure(figsize=(12, 8))
    
    # Generate distinct random colors for communities
    communities = set(partition.values())
    color_map = {community: "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for community in communities}

    # Node colors and sizes for the filtered nodes
    node_colors = [color_map[partition[node]] for node in subgraph]
    node_sizes = [subgraph.degree(node) * 10 for node in subgraph]  # Scale node sizes by degree

    # Draw nodes and edges for the filtered graph
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_sizes, alpha=0.7)
    nx.draw_networkx_edges(subgraph, pos, alpha=0.5)

    # Create a legend for the largest communities
    largest_communities = sorted([(comm_id, stats) for comm_id, stats in community_stats.items() if comm_id in partition.values()], key=lambda x: x[1]['count'], reverse=True)[:num_communities_to_label]
    legend_handles = [plt.Line2D([0], [0], marker='o', color=color_map[comm_id], label=f"Community {comm_id}: {stats['dominant_subfield']} ({stats['dominant_percentage']:.2f}%)", markersize=10, linestyle='') for comm_id, stats in largest_communities]

    plt.legend(handles=legend_handles, title="Communities", loc='upper left')
    plt.title('Advanced Community Visualization')
    plt.axis('off')
    plt.savefig('/Users/maryamriazi/Documents/Uni Courses/imagekamadakawai_DT40.png')  
    plt.close()  



