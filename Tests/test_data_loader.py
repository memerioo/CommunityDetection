import unittest
import networkx as nx
from scripts import data_loader
import tempfile
import os

class TestLoadCitationNetwork(unittest.TestCase):

    def setUp(self):
        # Initialize a clean temporary file each time
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+t')
        # Base test data
        self.test_data = [
            "# Comment line should be ignored\n",
            "1001\t2001\n",
            "1002\t2002\n",
            "2001\t1001\n"
        ]
        # Write base test data
        self.temp_file.writelines(self.test_data)
        self.temp_file.seek(0)

    def tearDown(self):
        # Close and remove the temporary file
        self.temp_file.close()
        os.remove(self.temp_file.name)

    def test_ignore_comments_and_malformed_lines(self):
        """Ensure that comments and malformed lines do not affect edge creation."""
        # Reopen the file in append mode to add more lines
        with open(self.temp_file.name, 'a') as f:
            f.write("# This is a new comment line\nnot_a_node_id\n")
        # Reload the graph to include new lines
        graph = data_loader.load_citation_network(self.temp_file.name)
        self.assertEqual(len(graph.edges()), 3, "Should only have 3 valid edges")

    def test_empty_and_comment_only_file(self):
        """Test loading an empty or comment-only file."""
        # Clear and rewrite the file with only a comment
        with open(self.temp_file.name, 'w') as f:
            f.write("# Only a comment\n")
        graph = data_loader.load_citation_network(self.temp_file.name)
        self.assertEqual(len(graph), 0)
        self.assertEqual(len(graph.edges()), 0)

if __name__ == '__main__':
    unittest.main()
