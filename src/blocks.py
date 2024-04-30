import re
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
