import json
import tempfile
import shutil
import os
from datetime import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def save_json_cache(data_dict, cache_file, description="data"):
    """ Save data to a JSON cache file safely. """
    temp_file = tempfile.NamedTemporaryFile('w', delete=False)
    try:
        json.dump(data_dict, temp_file, ensure_ascii=False, indent=4, cls=JSONEncoder)
        temp_file.close()
        shutil.move(temp_file.name, cache_file)
        print(f"{description.capitalize()} cache saved successfully for {len(data_dict)} items.")
    except Exception as e:
        print(f"Failed to save {description} cache: {e}")
        os.unlink(temp_file.name)
    finally:
        if not temp_file.closed:
            temp_file.close()

def load_json_cache(cache_file, description="data"):
    """ Load data from a JSON cache file. """
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded {description} for {len(data)} items from cache.")
                return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {description} cache file: {e}")
            return {}
    return {}
