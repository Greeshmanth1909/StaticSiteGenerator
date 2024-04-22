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
        text_btw_delimiter = []
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
