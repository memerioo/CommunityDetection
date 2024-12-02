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


def save_analysis(community_stats, global_stats, output_file):
    """
    Write a summary of community analysis including dominant subfields, their distributions, 
    and Fisher's Exact Test results to a file.
    
    Args:
        community_stats (dict): A dictionary containing statistics for each community.
        output_file (str): The filename where the summary will be saved.
    """
    with open(output_file, 'w') as file:
        # Write global stats
        file.write("Global Metrics:\n")
        for key, value in global_stats.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

        # Write community stats
        file.write("Community Specific Metrics:\n")
        for community_id, stats in community_stats.items():
            file.write(f"Community {community_id}:\n")
            for stat_key, stat_value in stats.items():
                file.write(f"  {stat_key}: {stat_value}\n")
            file.write("\n")