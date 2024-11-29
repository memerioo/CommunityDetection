from . import test_setup
import unittest
from unittest.mock import patch, MagicMock
from scripts.metadata_extractor import query_arxiv, fetch_metadata

class TestMetadataExtractor(unittest.TestCase):

    @patch('scripts.metadata_extractor.arxiv.Search')
    def test_query_arxiv_valid_id(self, mock_search):
        # Setup mock results from the arXiv search
        mock_result = MagicMock()
        mock_result.title = "Sample Title"
        mock_result.summary = "Sample Abstract"
        mock_result.published = "2021-01-01"
        mock_result.authors = [MagicMock(name="Author One"), MagicMock(name="Author Two")]
        mock_search.return_value.results.return_value = iter([mock_result])

        # Call the function under test
        result = query_arxiv('1234567')

        # Assert expected results
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Sample Title")
        self.assertEqual(result['abstract'], "Sample Abstract")
    
    def test_query_arxiv_invalid_id(self):
        # Call the function with an invalid paper ID
        result = query_arxiv('invalid123')
        # Assert that the result is None
        self.assertIsNone(result)

    @patch('scripts.metadata_extractor.load_json_cache', return_value={})
    @patch('scripts.metadata_extractor.save_json_cache')
    @patch('scripts.metadata_extractor.query_arxiv', side_effect=lambda x: {"title": "Dynamic Testing", "abstract": "Testing in progress", "published": "2022-01-01", "authors": ["Tester"]})
    def test_fetch_metadata(self, mock_query_arxiv, mock_save_json_cache, mock_load_json_cache):
        # Prepare a list of paper IDs and the expected results
        paper_ids = ['1234567', '2345678']
        # Call the function
        metadata = fetch_metadata(paper_ids)

        # Check that metadata is fetched and cached correctly
        self.assertEqual(metadata['1234567']['title'], "Dynamic Testing")
        self.assertTrue(mock_save_json_cache.called)

    @patch('scripts.metadata_extractor.load_json_cache', return_value={"1234567": {"title": "Cached Title"}})
    def test_fetch_metadata_with_cache_hit(self, mock_load_json_cache):
        # Test that cached data is used and no further API call is made
        paper_ids = ['1234567']  # This ID should be found in cache
        metadata = fetch_metadata(paper_ids)

        # Assert that the cached data is returned
        self.assertEqual(metadata['1234567']['title'], "Cached Title")

    @patch('scripts.metadata_extractor.save_json_cache')
    @patch('scripts.metadata_extractor.query_arxiv', return_value=None)
    def test_fetch_metadata_api_failure(self, mock_query_arxiv, mock_save_json_cache):
        # Simulate API failure
        paper_ids = ['unknown_id']
        metadata = fetch_metadata(paper_ids)
        # Check if fallback data is used
        self.assertEqual(metadata['unknown_id']['title'], "Unknown")
        self.assertTrue(mock_save_json_cache.called)

if __name__ == '__main__':
    unittest.main()
