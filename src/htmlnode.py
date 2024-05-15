# html node renders as html
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return f"<{self.tag}>{self.value}</{self.tag}>" 

    def props_to_html(self):
        if self.props is not None:
            return " ".join(map(lambda prop: f"{prop}=\"{self.props[prop]}\"", self.props.keys()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes require a value")
        if self.tag is None:
            return f"{self.value}"
        # there is a tag and a value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag must be provided")
        if self.children is None:
            raise ValueError("children is none")
        html_str = []
        # iterate through children
        for child in self.children:
            if child.children is None:
                # add child to string list
                html_str.append(child.to_html())
            else:
                # the node might be a parent node, recursion
                html_str.append(child.to_html())

        # the html string should be populated as expected, hopefully
        return f"<{self.tag}>{"".join(html_str)}</{self.tag}>"
