from . import test_setup
import unittest
import os
import tempfile
import json
from datetime import datetime
from scripts.data_access import save_json_cache, load_json_cache, JSONEncoder

class TestJSONCache(unittest.TestCase):

    def setUp(self):
        # Setup a temporary directory to use for cache files
        self.test_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.test_dir, 'test_cache.json')

    def tearDown(self):
        # First, remove all files in the directory
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            os.unlink(file_path)  
        os.rmdir(self.test_dir)  


    def test_save_json_cache(self):
        """ Test saving data to a JSON file """
        data = {'test': 'data', 'timestamp': datetime.now()}
        save_json_cache(data, self.cache_file)
        self.assertTrue(os.path.exists(self.cache_file))
        with open(self.cache_file, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data['test'], 'data')
        self.assertIsInstance(loaded_data['timestamp'], str)  

    def test_load_json_cache_exists(self):
        """ Test loading data from an existing JSON file """
        data = {'items': 123}
        with open(self.cache_file, 'w') as f:
            json.dump(data, f)
        loaded_data = load_json_cache(self.cache_file)
        self.assertEqual(loaded_data['items'], 123)

    def test_load_json_cache_not_exists(self):
        """ Test behavior when JSON file does not exist """
        loaded_data = load_json_cache('nonexistent.json')
        self.assertEqual(loaded_data, {})

    def test_load_json_cache_corrupted(self):
        """ Test behavior with a corrupted JSON file """
        with open(self.cache_file, 'w') as f:
            f.write('{"incomplete": "data"')
        loaded_data = load_json_cache(self.cache_file)
        self.assertEqual(loaded_data, {})

if __name__ == '__main__':
    unittest.main()
