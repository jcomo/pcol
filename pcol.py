class RenderTree(object):
    """A tree interface where the only responsibility of subclasses is to define
    what it means to render. Calling str on a RenderTree will implictly call render."""

    def __str__(self):
        return self.render()

    def render(self, prefix=''):
        raise NotImplemented("Implement in subclass")


class ModifierNode(RenderTree):
    """A node that has a modifier attached to it. The modifier will be rendered in
    front of each child."""

    def __init__(self, modifier, children, separator=None):
        """
        Initialize a modifier node.

        :param modifier: (string) modifier to prepend to each child
        :param children: list of children where each child is a RenderTree
        :param separator: the separator to use between nodes when rendering to a string
        """
        self.modifier = modifier
        self.children = children
        self.separator = separator or ''

    def render(self, prefix=''):
        """
        Renders the modifier node by pre-pending the modifier to each child. When rendering
        itself, it will append its own modifier to the prefix and pass that down to its children.

        :param prefix: accumulated modifiers up until this point
        :return: string representation of the render tree
        """
        if not self.children:
            return ''
        accumulated_modifiers = prefix + self.modifier
        rendered_children = [child.render(accumulated_modifiers) for child in self.children]
        return self.separator.join(rendered_children)


class TokenNode(RenderTree):
    """A leaf node of a RenderTree. Each TokenNode will have a value and an optional
    clear value. The clear value will be appended to the end when rendered."""

    def __init__(self, value=None, clear=None):
        """
        Initialize a token node.
        :param value: (string) value held by the node
        :param clear: (string) optional value to use as a reset
        """
        self.value = value or ''
        self.clear = clear or ''

    def render(self, prefix=''):
        """
        Renders the token node with its prefix, value, and clear value.

        :param prefix: (string) prefix at this point. Will be passed from a modifier node
        :return: string representation of this node
        """
        return prefix + self.value + self.clear


def render_with(modifier):
    """
    Creates a function that will use the modifier to create a render tree. This is
     meant to be attached to a class via a property as the function that it returns
     will be called on an instance of that class.

     The class can define the following parameters:
        __clear__     -> the clear value for each token node
        __separator__ -> the separator to use when rendering the constructed tree

    :param modifier: the modifier to use
    :return: a function that, when called, will create a render tree
    """
    def __make_render_tree(self, *tokens):
        clear = getattr(self, '__clear__', None)
        separator = getattr(self, '__separator__', None)
        get_node = lambda t: t if isinstance(t, RenderTree) else TokenNode(t, clear)
        return ModifierNode(modifier, [get_node(token) for token in tokens], separator)
    return __make_render_tree


class _Pcol(object):
    """A renderer that uses ANSI escape codes. The expected output device
    with this renderer is stdout on a terminal."""

    __separator__ = ' '
    __clear__ = '\033[0m'

    bold = render_with('\033[1m')
    underline = render_with('\033[4m')

    black = render_with('\033[30m')
    red = render_with('\033[31m')
    green = render_with('\033[32m')
    yellow = render_with('\033[33m')
    blue = render_with('\033[34m')
    magenta = render_with('\033[35m')
    cyan = render_with('\033[36m')
    white = render_with('\033[37m')


pcol = _Pcol()