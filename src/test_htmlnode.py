from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

class TesthtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "hello", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), f"HTMLNode(a, hello, None, {node.props})")

    def test_props(self):
        node = HTMLNode("a", "hello", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_with_props(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")


class TestParentNode(unittest.TestCase):
    def test_without_children(self):
        node = ParentNode("p",
                                 [
                                     LeafNode("b", "Bold text"),
                                     LeafNode(None, "Normal text"),
                                     LeafNode("i", "italic text"),
                                     LeafNode(None, "Normal text"),
                                     ],
                                 )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        

    def test_with_children(self):
        node1 = ParentNode("p",
                           [
                               LeafNode("b", "Bold text"),
                               LeafNode(None, "Normal text"),
                               LeafNode("i", "italic text"),
                               LeafNode(None, "Normal text"),
                               ],
                           )
        node2 = ParentNode("div", 
                           [
                               node1,
                               LeafNode(None, "Normal text"),
                               LeafNode("i", "italic text"),
                               LeafNode(None, "Normal text"),
                               ]
                           )
        self.assertEqual(node2.to_html(), "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</div>")

