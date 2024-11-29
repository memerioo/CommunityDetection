from . import test_setup
import unittest
from unittest.mock import mock_open, patch, call
from scripts.utils import save_community_analysis, format_paper_id

class TestSaveCommunityAnalysis(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_save_community_analysis(self, mock_file):
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
        output_file = 'test_community_analysis.txt'
        save_community_analysis(community_stats, output_file)

        # Prepare the expected content to be written to the file
        expected_calls = [
            call("\nCommunity 1:\n"),
            call("  Dominant Subfield: Electroweak Physics (38.81%)\n"),
            call("  Subfield Distribution and Fisher's Exact Test Results:\n"),
            call("    Gravitational Physics: 600 - Odds Ratio: 4.38, P-value: 0.0001\n"),
            call("    Electroweak Physics: 5586 - Odds Ratio: 2.58, P-value: 0.0000\n")
        ]

        # Check that open was called correctly
        mock_file.assert_called_once_with(output_file, 'w')
        # Check that write was called correctly
        handle = mock_file()
        handle.write.assert_has_calls(expected_calls, any_order=False)

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
