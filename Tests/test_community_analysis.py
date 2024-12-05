from . import test_setup
import unittest
from scripts.community_analysis import prepare_community_stats, perform_fisher_analysis, calculate_overall_subfield_counts
import collections as col
import scipy.stats as st
import networkx as nx

class TestCommunityAnalysis(unittest.TestCase):

    def setUp(self):
        """
        Setup test environment for community analysis tests.
        This setup includes a partition dict mapping paper IDs to community IDs,
        a dict of labeled papers mapping paper IDs to lists of their subfields, and
        a mock graph object.
        """
        self.partition = {'p1': 1, 'p2': 1, 'p3': 2}
        self.labeled_papers = {'p1': ['Physics'], 'p2': ['Physics', 'Math'], 'p3': ['Math']}
        self.total_papers = 3
        self.mock_graph = nx.Graph()
        self.mock_graph.add_nodes_from(self.partition.keys())
        self.mock_graph.add_edges_from([('p1', 'p2'), ('p2', 'p3')])

    def test_prepare_community_stats(self):
        """
        Tests the generation of initial community statistics based on a partition, labeled papers, and a graph object.
        The test verifies that the statistics correctly calculate the dominant subfield and its percentage
        for each community.
        """
        expected_stats = {
            1: {'count': 2, 'subfields': {'Physics': 2, 'Math': 1}, 'dominant_subfield': 'Physics', 'dominant_percentage': 100.0},
            2: {'count': 1, 'subfields': {'Math': 1}, 'dominant_subfield': 'Math', 'dominant_percentage': 100.0}
        }
        result, _ = prepare_community_stats(self.partition, self.labeled_papers, self.mock_graph)
        self.assertEqual(result[1]['dominant_subfield'], expected_stats[1]['dominant_subfield'])
        self.assertEqual(result[1]['dominant_percentage'], expected_stats[1]['dominant_percentage'])
        self.assertEqual(result[2]['dominant_subfield'], expected_stats[2]['dominant_subfield'])
        self.assertEqual(result[2]['dominant_percentage'], expected_stats[2]['dominant_percentage'])

    def test_perform_fisher_analysis(self):
        """
        Tests the Fisher's Exact Test analysis performed on community statistics.
        This test verifies that the p-values are calculated correctly and are within
        the valid range of 0 to 1 for significance testing.
        """
        community_stats, _ = prepare_community_stats(self.partition, self.labeled_papers, self.mock_graph)
        updated_stats = perform_fisher_analysis(community_stats, self.labeled_papers, self.total_papers)
        for community_id, stats in updated_stats.items():
            for subfield, result in stats['fisher_results'].items():
                with self.subTest(community_id=community_id, subfield=subfield):
                    # Check if p-value is calculated and is a valid probability
                    self.assertGreaterEqual(result['p_value'], 0.0)
                    self.assertLessEqual(result['p_value'], 1.0)

    def test_calculate_overall_subfield_counts(self):
        """
        Tests the calculation of overall subfield counts across all labeled papers.
        The test checks whether the total counts for each subfield are accurately computed.
        """
        expected_counts = {'Physics': 2, 'Math': 2}
        result = calculate_overall_subfield_counts(self.labeled_papers)
        self.assertEqual(result, expected_counts)

if __name__ == '__main__':
    unittest.main()
