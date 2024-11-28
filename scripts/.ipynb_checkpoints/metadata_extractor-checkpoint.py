import arxiv
import concurrent.futures as cf
import requests
from bs4 import BeautifulSoup
from scripts.data_access import save_json_cache, load_json_cache

def query_arxiv(paper_id):
    """ Query the ArXiv API for metadata using the paper's ID. """
    try:
        if paper_id.isdigit() and len(paper_id) == 7:
            paper_id = f"hep-ph/{paper_id}"
        search = arxiv.Search(id_list=[paper_id], max_results=1)
        result = next(search.results(), None)
        if result:
            return {
                "title": result.title,
                "abstract": result.summary,
                "published": result.published,
                "authors": [author.name for author in result.authors]
            }
        else:
            print(f"No metadata found for {paper_id}.")
            return None
    except Exception as e:
        print(f"Error querying Paper ID {paper_id}: {e}")
        return None

def fetch_metadata(paper_ids, cache_file='metadata_cache.json'):
    """Fetches metadata for a list of paper IDs using caching to avoid redundant API calls."""
    metadata_dict = load_json_cache(cache_file, "metadata") 

    missing_ids = [pid for pid in paper_ids if pid not in metadata_dict]
    if missing_ids:
        print(f"Fetching metadata for {len(missing_ids)} missing papers.")
        with cf.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(query_arxiv, paper_id): paper_id for paper_id in missing_ids}
            for future in cf.as_completed(futures):
                paper_id = futures[future]
                try:
                    metadata = future.result()
                    if metadata:
                        metadata_dict[paper_id] = metadata
                        save_json_cache(metadata_dict, cache_file, description="metadata") 
                    else:
                        # Store a default entry for papers where metadata could not be fetched
                        metadata_dict[paper_id] = {"title": "Unknown", "abstract": "Unknown", "subfield": "Unknown"}
                        save_json_cache(metadata_dict, cache_file, description="metadata")  
                except Exception as e:
                    print(f"Error fetching metadata for {paper_id}: {e}")
                    metadata_dict[paper_id] = {"title": "Unknown", "abstract": "Unknown", "subfield": "Unknown"}
                    save_json_cache(metadata_dict, cache_file, description="metadata")  # Ensuring error handling also caches the default data
    return metadata_dict
