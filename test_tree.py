"""
test_tree.py - Unit test suite for CareerTree binary decision tree engine.
"""

import unittest
from tree import build_career_tree, trace_tree, find_path_to_career, get_all_careers, get_tree_metrics


class TestCareerTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = build_career_tree()

    def test_tree_metrics(self):
        metrics = get_tree_metrics(self.root)
        self.assertEqual(metrics["total_nodes"], 31, "Total nodes should be 31 for full 4-level binary tree")
        self.assertEqual(metrics["leaf_nodes"], 16, "Leaf count should be 2^4 = 16")
        self.assertEqual(metrics["internal_nodes"], 15, "Internal nodes should be 15")
        self.assertEqual(metrics["tree_height"], 4, "Tree height must be 4")
        self.assertTrue(metrics["is_balanced"], "Tree must be perfectly balanced")

    def test_all_16_paths(self):
        all_careers = set()
        # Test all 2^4 = 16 permutations of [bool, bool, bool, bool]
        for b0 in [False, True]:
            for b1 in [False, True]:
                for b2 in [False, True]:
                    for b3 in [False, True]:
                        path = [b0, b1, b2, b3]
                        leaf, history = trace_tree(self.root, path)
                        self.assertTrue(leaf.is_leaf, f"Path {path} did not reach a leaf")
                        self.assertIsNotNone(leaf.career, f"Path {path} leaf has no career profile")
                        self.assertEqual(len(history), 4, f"Path length must be 4, got {len(history)}")
                        all_careers.add(leaf.career.title)

        self.assertEqual(len(all_careers), 16, "All 16 paths must reach 16 distinct careers")

    def test_find_path_to_career(self):
        careers = get_all_careers(self.root)
        self.assertEqual(len(careers), 16)
        for c in careers:
            path = find_path_to_career(self.root, c.title)
            self.assertIsNotNone(path, f"Could not find path to {c.title}")
            self.assertEqual(len(path), 5, f"Path to {c.title} should have 5 entries (4 decisions + 1 leaf)")


if __name__ == "__main__":
    unittest.main()
