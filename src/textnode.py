from htmlnode import LeafNode
import re
# TextNode == a class that can take three arguments in its constructor: text, text_type and url
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



def text_node_to_html_node(text_node):
    # take a text node obj and convert it to a leafnode
    defined_text_types = set(["text", "bold", "italic", "code", "link", "image"])
    if text_node.text_type not in defined_text_types:
        raise Exception("text type not defined")
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # takes a textnode object a delimiter and a text type associated with the delimiter and separates the code within the delimiter
   defined_text_types = set(["text", "bold", "italic", "code", "link", "image"])
    # Check weather valid text_type is given
   if text_type not in defined_text_types:
        raise Exception("Invalid TextType")
   new_nodes = []
    # Filter text within specified delimiter
   for node in old_nodes:
        text = node.text
        split_text = text.split(delimiter)
        index_of_first_delimiter = text.find(delimiter)
        index_of_second_delimiter = text.find(delimiter, index_of_first_delimiter + 1, len(text))
        # if index of second delimiter is -1, only one occurance is present
        if index_of_first_delimiter == -1:
            new_nodes.append(TextNode(text, text_type_text))
            continue
        string_bw_delm = text[index_of_first_delimiter + len(delimiter): index_of_second_delimiter]
        for text in split_text:
            if text == string_bw_delm:
                new_nodes.append(TextNode(text, text_type))
                continue
            new_nodes.append(TextNode(text, text_type_text))

   return new_nodes

def extract_markdown_images(text):
    # take text with embedded links for images and split them
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    # extract links from markdown text
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

