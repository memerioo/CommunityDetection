import networkx as nx
from scripts import utils as ut

def load_citation_network(filepath):
    """
    Loads the citation network from a file and returns it as a directed graph.
    
    Args:
        filepath (str): Path to the citation network file.
    
    Returns:
        nx.DiGraph: A directed graph where nodes are paper IDs and edges represent citations.
    """
    citation_graph = nx.DiGraph()
    with open(filepath, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    from_paper, to_paper = parts
                    from_paper = ut.format_paper_id(from_paper)
                    to_paper = ut.format_paper_id(to_paper)
                    citation_graph.add_edge(from_paper, to_paper)
    return citation_graph





