import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import scripts.data_loader as dl
import scripts.label_assigner as la
import scripts.metadata_extractor as me
import scripts.community_detection as cd
import scripts.community_analysis as ca
import scripts.utils as ut

def main():
    base_path = os.path.join(os.path.dirname(__file__), '..', 'Data')
    citation_file = os.path.join(base_path, 'cit-HepPh.txt')
    metadata_cache_path = os.path.join(base_path, 'metadata_cache.json')
    labels_cache_path = os.path.join(base_path, 'labels_cache.json')

    # Load data
    citation_network = dl.load_citation_network(citation_file)
    paper_ids = list(citation_network.nodes())

    # Fetch metadata and labels
    subfield_dict = la.create_subfield_dictionary()
    metadata = me.fetch_metadata(paper_ids, metadata_cache_path)
    labeled_papers = la.label_papers(metadata, subfield_dict, labels_cache_path)

    # Detect communities and analyze them
    partition = cd.detect_communities_infomap(citation_network)
    community_stats, global_stats = ca.prepare_community_stats(partition, labeled_papers, citation_network)

    # Calculate and display Fisher's Exact Test results
    community_stats = ca.perform_fisher_analysis(community_stats, labeled_papers, len(paper_ids))
    if not os.path.exists('Results'):
        os.makedirs('Results')
    ut.save_analysis(community_stats, global_stats, output_file='Results/community_analysis.txt')
    cd.visualize_communities(citation_network, partition, community_stats)


if __name__ == "__main__":
    main()
