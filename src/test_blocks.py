from blocks import markdown_to_blocks, block_to_block_type
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

    def test_block_to_block_type(self):
        code = "``` \nprint(\"hello\")\n if something is nothing:\n    say(hi)\n```"
        paragraph = "this is a para, laskdjlsdkjf, \n lsakdjlsdkj\n thth"
        heading = "### hello"
        not_heading = "####### heh"
        quote = "> vim is great\n> line 2\n> line 3"
        ul = "* one\n- two\n* three"
        ol = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(code), "code")
        self.assertEqual(block_to_block_type(paragraph), "paragraph")
        self.assertEqual(block_to_block_type(heading), "heading")
        self.assertEqual(block_to_block_type(not_heading), "paragraph")
        self.assertEqual(block_to_block_type(quote), "quote")
        self.assertEqual(block_to_block_type(ul),"unordered list")
        self.assertEqual(block_to_block_type(ol),"ordered list")
