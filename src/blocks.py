import re
from htmlnode import HTMLNode
from textnode import text_to_textnodes, text_node_to_html_node, ParentNode
# Takes raw markdown and converts it into a list of clock strings

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered list"
block_type_ol = "ordered list"

def markdown_to_blocks(markdown):
    md_list = markdown.split("\n\n")
    upd_list = map(lambda x: x.strip(), md_list)
    new_list = []
    for item in upd_list:
        if item != "":
            new_list.append(item)
    return new_list

def block_to_block_type(block):
    heading_regex = r'^#{1,6} .*$'
    code_regex = r'^```.*|\n```$'
    quote_line_regex = r'^> .*$'
    ul_line_regex = r'^\*|- .*$'
    ol_line_regex = r'^\d+\. .*$'

    # Match headings
    if re.match(heading_regex, block):
        return block_type_heading

    if re.match(code_regex, block):
        return block_type_code

    # Need to split the block
    split_block = block.split("\n")

    if split_line_helper(split_block, quote_line_regex):
        return block_type_quote
    if split_line_helper(split_block, ul_line_regex):
        return block_type_ul
    if split_line_helper(split_block, ol_line_regex):
        return block_type_ol
    return block_type_paragraph

def split_line_helper(split_line_list, regex):
    for line in split_line_list:
        if not re.match(regex, line):
            return False
    return True


# convert block to its corresponding html node
def paragraph_to_html_node(block):
    return HTMLNode("p", block)

def code_to_html_node(block):
    code = HTMLNode("code", block)
    return HTMLNode("pre", None, code)

def quote_to_html_node(block):
    return HTMLNode("blockquote", block)

def ul_to_html_node(block):
    ul_elements = block.split("\n")
    ul_nodes = map(lambda x: HTMLNode("li", x), ul_elements)
    return HTMLNode("ul", None, ul_nodes)

def ol_to_html_node(block):
    ol_nodes = map(lambda x: HTMLNode("li", x), block.split("\n"))
    return ParentNode("ol", None, ol_nodes)

def headings_to_html_node(block):
    # Isolate the number of # with regex
    regex = r'^#{1,6}'
    hash_count = len(re.findall(regex, block)[0])
    return ParentNode(f"h{hash_count}", None, block)

def markdown_to_html_node(markdown):
    # The md is raw
    blocks = markdown_to_blocks(markdown)
    # define global html for blocks
    html_nodes = []
    for block in blocks:
        block_type =  block_to_block_type(block)
        if block_type == block_type_paragraph:
            # might use text_to_text_nodes function
            text_nodes = text_to_textnodes(block)
            leaf_nodes = []
            for node in text_nodes:
                leaf_nodes.append(text_node_to_html_node(node))
            # have to convert leaf nodes to html nodes
            leaf_nodes_combo = map(lambda x: x.to_html(), leaf_nodes)
            para_value = "".join(leaf_nodes_combo)
            html_nodes.append(HTMLNode("p", para_value))

        # Code
        if block_type == block_type_code:
            html_nodes.append(code_to_html_node(block))

        # heading
        if block_type == block_type_heading:
            html_nodes.append(headings_to_html_node(block))

        # ol
        if block_type == block_type_ol:
            html_nodes.append(ol_to_html_node(block))

        # ul
        if block_type == block_type_ul:
            html_nodes.append(ul_to_html_node(block))

        # quote
        if block_type == block_type_quote:
            html_nodes.append(quote_to_html_node(block))

    # The html node list contains the children of all
    mega_parent = ParentNode("div", None, html_nodes)
    return mega_parent
