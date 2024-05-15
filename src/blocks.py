import re, os
from htmlnode import HTMLNode
from textnode import text_to_textnodes, text_node_to_html_node
from htmlnode import ParentNode
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
    quote_list = block.split("> ")
    html_node_list = []
    for quote in quote_list:
        if quote == "":
            continue
        html_node_list.append(HTMLNode("blockquote", quote))
    return html_node_list

def ul_to_html_node(block):
    ul_elements = block.split("\n")
    ul_nodes = map(lambda x: HTMLNode("li", x), ul_elements)
    return HTMLNode("ul", None, ul_nodes)

def ol_to_html_node(block):
    ol_nodes = map(lambda x: HTMLNode("li", re.sub(r'^\d+\. ', "", x)), block.split("\n"))
    return ParentNode("ol", ol_nodes)

def headings_to_html_node(block):
    # Isolate the number of # with regex
    regex = r'^#{1,6}'
    hash_count = len(re.findall(regex, block)[0])
    return HTMLNode(f"h{hash_count}", block.strip(f"{re.findall(regex, block)[0]}"))

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
            quote_list = quote_to_html_node(block)
            for quote in quote_list:
                print(quote)
                html_nodes.append(quote)

    # The html node list contains the children of all
    mega_parent = ParentNode("div", html_nodes)
    return mega_parent


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("#"):
            return line.strip("#")

    raise Exception("Document must contain a heading")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    from_path_md = f.read()
    f.close()

    # read template
    f = open(template_path)
    template_file = f.read()
    f.close()

    title = extract_title(from_path_md).strip("#")
    content = markdown_to_html_node(from_path_md).to_html()
    html = template_file.replace(" {{ Title }} ", title)
    html = html.replace("{{ Content }}", content)
    
    # Write template_file to html in specified path
    #if not os.path.exists(dest_path):
     #   os.makedirs(dest_path)
    
    try:
        f = open(dest_path, "w")
        f.write(html)
        f.close()
    except Exception as e:
        print(f"error: {e}")

