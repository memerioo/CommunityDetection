def format_paper_id(paper_id):
    """
    Format the paper ID to match the proper format, which includes leading zeros.
    - IDs from 1991 to 1999 should be in the form 7 digits, so they need 6 zeros.
    - IDs from 2000 onwards should be in the form 7 digits, prefixed with zeros if necessary.
    
    Example:
    '1024' becomes '0001024'
    '111022' becomes '0111022'
    
    Args:
        paper_id (str or int): The raw paper ID.
    
    Returns:
        str: A formatted paper ID with leading zeros.
    """
    # Ensure paper_id is a string
    paper_id = str(paper_id)
    
    # If the ID is less than 7 digits, pad it with leading zeros
    return paper_id.zfill(7)


def save_community_analysis(community_stats, output_file='community_analysis.txt'):
    """
    Write a summary of community analysis including dominant subfields, their distributions, 
    and Fisher's Exact Test results to a file.
    
    Args:
        community_stats (dict): A dictionary containing statistics for each community.
        output_file (str): The filename where the summary will be saved.
    """
    with open(output_file, 'w') as file:
        for community_id, stats in community_stats.items():
            file.write(f"\nCommunity {community_id}:\n")
            file.write(f"  Dominant Subfield: {stats['dominant_subfield']} ({stats['dominant_percentage']:.2f}%)\n")
            file.write("  Subfield Distribution and Fisher's Exact Test Results:\n")
            for subfield, count in stats['subfields'].items():
                fisher_result = stats['fisher_results'].get(subfield, {'odds_ratio': 'N/A', 'p_value': 'N/A'})
                # Formatting numbers to two decimal places for odds ratio and four for p-value
                odds_ratio = f"{float(fisher_result['odds_ratio']):.2f}" if fisher_result['odds_ratio'] != 'N/A' else 'N/A'
                p_value = f"{float(fisher_result['p_value']):.4f}" if fisher_result['p_value'] != 'N/A' else 'N/A'
                file.write(f"    {subfield}: {count} - Odds Ratio: {odds_ratio}, P-value: {p_value}\n")
