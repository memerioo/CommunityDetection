from . import test_setup
import unittest
from scripts.label_assigner import assign_labels, create_subfield_dictionary, label_paper, label_papers
from unittest.mock import patch, MagicMock

class TestLabelAssigner(unittest.TestCase):
    
    def setUp(self):
        self.subfield_dict = create_subfield_dictionary()

    def test_assign_labels_single_match(self):
        """Test label assignment for a paper with a title and abstract that match multiple subfields."""
        title = "Exploring the anomaly in gravity"
        abstract = "This paper discusses gravitational physics extensively."
        expected_labels = sorted(["General Theoretical Physics", "Gravitational Physics"])  
        labels = sorted(assign_labels(title, abstract, self.subfield_dict, max_labels=3))  
        self.assertEqual(labels, expected_labels)

    def test_assign_labels_multiple_matches(self):
        """Test label assignment for a paper with a title and abstract that match multiple subfields."""
        title = "A study on SUSY particles and their implications on cosmology"
        abstract = "Supersymmetry (SUSY) and dark matter are discussed."
        expected_labels = ["Supersymmetry", "Cosmology"]
        labels = assign_labels(title, abstract, self.subfield_dict, max_labels=3)
        self.assertListEqual(labels, expected_labels)

    def test_assign_labels_no_matches(self):
        """Test label assignment for a paper with a title and abstract that match no known subfields."""
        title = "Unknown phenomena in physics"
        abstract = "This paper does not match any subfield."
        expected_labels = ["Unknown"]
        labels = assign_labels(title, abstract, self.subfield_dict, max_labels=3)
        self.assertEqual(labels, expected_labels)

    def test_assign_labels_limit_exceeded(self):
        """Test label assignment for a paper where the number of potential labels exceeds the maximum allowed."""
        title = "Quantum gravity, strings, and cosmological implications"
        abstract = "This paper discusses quantum gravity, string theory, and cosmology in depth."
        expected_labels = ["Gravitational Physics", "String Theory", "Cosmology"]
        labels = assign_labels(title, abstract, self.subfield_dict, max_labels=3)
        self.assertListEqual(labels, expected_labels)

    @patch('scripts.label_assigner.assign_labels')
    def test_label_paper(self, mock_assign_labels):
        """Test the labeling of a single paper using mocked label assignments to ensure the function handles inputs correctly."""
        mock_assign_labels.return_value = ["Quantum Chromodynamics", "Perturbative QCD"]
        metadata = {"title": "High-energy particle collisions", "abstract": "Discussing QCD and collider impacts."}
        expected = ("1234567", ["Quantum Chromodynamics", "Perturbative QCD"])
        result = label_paper("1234567", metadata, self.subfield_dict)
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
