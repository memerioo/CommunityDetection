import collections as col
import scipy.stats as st

def prepare_community_stats(partition, labeled_papers):
    """
    Prepares initial community statistics based on partition and labeled papers, calculating dominant subfields.
    
    Args:
        partition (dict): Mapping from paper IDs to community IDs.
        labeled_papers (dict): Mapping from paper IDs to lists of subfields.
    
    Returns:
        dict: A dictionary with initial community statistics including dominant subfields.
    """
    community_stats = col.defaultdict(lambda: {'count': 0, 'subfields': col.defaultdict(int)})
    for paper_id, community_id in partition.items():
        community_stats[community_id]['count'] += 1
        subfields = labeled_papers.get(paper_id, ["Unknown"])
        for subfield in subfields:
            community_stats[community_id]['subfields'][subfield] += 1
    
    # Calculate the dominant subfield for each community
    for community_id, stats in community_stats.items():
        dominant_subfield = max(stats['subfields'], key=stats['subfields'].get)
        dominant_count = stats['subfields'][dominant_subfield]
        total_count = stats['count']
        stats['dominant_subfield'] = dominant_subfield
        stats['dominant_percentage'] = (dominant_count / total_count) * 100 if total_count > 0 else 0

    return community_stats


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
