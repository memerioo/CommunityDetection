from . import test_setup
import unittest
from unittest.mock import mock_open, patch, call
from scripts.utils import save_analysis, format_paper_id

class TestSaveCommunityAnalysis(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    def test_save_analysis(self, mock_file):
        """
        This test uses a mock for the file handling to verify if the write operations include specific
        content based on provided `community_stats` and `global_stats`.
        Attributes:
            mock_file (MagicMock): A mock of the built-in open function used to intercept file operations.
    
        The mock data simulates a typical set of community statistics
        """
        # Example setup
        community_stats = {
            1: {
                'dominant_subfield': 'Electroweak Physics',
                'dominant_percentage': 38.81,
                'subfields': {
                    'Gravitational Physics': 600,
                    'Electroweak Physics': 5586
                },
                'fisher_results': {
                    'Gravitational Physics': {'odds_ratio': 4.38, 'p_value': 0.0001},
                    'Electroweak Physics': {'odds_ratio': 2.58, 'p_value': 0.0000}
                }
            }
        }
        global_stats = {'total_papers': 10000, 'total_citations': 500000}
        output_file = 'test_analysis_output.txt'
        
        # Call the function under test
        save_analysis(community_stats, global_stats, output_file)
        
        # Access the file handle correctly
        handle = mock_file.return_value.__enter__.return_value
        
        
        handle.write.assert_any_call("Global Metrics:\n")
        handle.write.assert_any_call("total_papers: 10000\n")
        handle.write.assert_any_call("total_citations: 500000\n")
        handle.write.assert_any_call("Community Specific Metrics:\n")
        handle.write.assert_any_call("Community 1:\n")
        handle.write.assert_any_call("  dominant_subfield: Electroweak Physics\n")
        handle.write.assert_any_call("  subfields: {'Gravitational Physics': 600, 'Electroweak Physics': 5586}\n")


class TestFormatPaperId(unittest.TestCase):

    def test_format_paper_id(self):
        # Test normal IDs that should be padded with zeros
        self.assertEqual(format_paper_id('1024'), '0001024', "Should pad with leading zeros to make 7 digits")
        self.assertEqual(format_paper_id('111022'), '0111022', "Should pad with leading zeros to make 7 digits")

        # Test already complete ID not needing padding
        self.assertEqual(format_paper_id('1234567'), '1234567', "Should remain unchanged as it's already 7 digits")

        # Test IDs that are numeric values
        self.assertEqual(format_paper_id(1024), '0001024', "Should handle numeric input and pad correctly")
        self.assertEqual(format_paper_id(111022), '0111022', "Should handle numeric input and pad correctly")

        # Test edge case with empty string or zero
        self.assertEqual(format_paper_id(''), '0000000', "Empty string should return a string of seven zeros")
        self.assertEqual(format_paper_id(0), '0000000', "Zero should return a string of seven zeros")

if __name__ == '__main__':
    unittest.main()
