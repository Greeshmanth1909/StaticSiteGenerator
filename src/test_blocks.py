from blocks import markdown_to_blocks
import unittest

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        block_text = markdown_to_blocks(text)
        expected_block = ["This is **bolded** paragraph", 
                          "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                          "* This is a list\n* with items",
                          ]
        self.assertEqual(block_text, expected_block)
