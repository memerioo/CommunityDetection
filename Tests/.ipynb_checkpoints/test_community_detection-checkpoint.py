import unittest
from unittest.mock import patch, MagicMock
from scripts.community_detection import detect_communities_infomap, analyze_community_subfields
import networkx as nx

class TestDetectCommunitiesInfomap(unittest.TestCase):
    @patch('scripts.community_detection.infomap.Infomap')
    def test_detect_communities_infomap(self, mock_infomap):
        """
        Tests the community detection using the Infomap algorithm on a simple graph.
        The test ensures that the mock Infomap instance is configured to simulate
        the Infomap community detection correctly and checks that the resulting
        community assignments are as expected based on the mocked output.
        """
        # Setup the graph
        graph = nx.Graph()
        graph.add_edge(0, 1)

        # Setup the mock Infomap instance
        mock_instance = mock_infomap.return_value
        mock_instance.run = MagicMock()

        # Setup the nodes property to yield mock nodes directly
        mock_node_0 = MagicMock(node_id=0, module_id=1)
        mock_node_1 = MagicMock(node_id=1, module_id=1)
        mock_instance.nodes = [mock_node_0, mock_node_1]

        # Mock add_link to simulate the Infomap internal behavior
        mock_instance.add_link = MagicMock()

        result = detect_communities_infomap(graph)

        expected = {0: 1, 1: 1}
        self.assertEqual(result, expected)

class TestAnalyzeCommunitySubfields(unittest.TestCase):
    def test_analyze_community_subfields(self):
        """
        Tests the analysis of paper subfields within identified communities.
        This test verifies that the function can correctly map and aggregate
        subfields for papers within the same community based on provided metadata.
        """
        # Setup
        communities = {'paper1': 1, 'paper2': 1, 'paper3': 2}
        metadata = {'paper1': {'subfield': 'Physics'}, 'paper2': {'subfield': 'Mathematics'}, 'paper3': {'subfield': 'Chemistry'}}

        expected = {1: ['Physics', 'Mathematics'], 2: ['Chemistry']}

        result = analyze_community_subfields(communities, metadata)

        self.assertEqual(result, expected)

    def test_analyze_community_subfields_with_unknown_subfields(self):
        """
        Tests the behavior of the subfield analysis when metadata is missing.
        The function should default to 'Unknown' for any papers where subfield metadata is not available.
        """
        # If metadata is missing, 'Unknown' should be used as the subfield
        communities = {'paper1': 1}
        metadata = {}  # No metadata available

        # Expected results
        expected = {1: ['Unknown']}

        result = analyze_community_subfields(communities, metadata)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
