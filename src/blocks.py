# Takes raw markdown and converts it into a list of clock strings
def markdown_to_blocks(markdown):
    md_list = markdown.split("\n\n")
    upd_list = map(lambda x: x.strip(), md_list)
    return upd_list

