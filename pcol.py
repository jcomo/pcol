class RenderTree(object):
    def __str__(self):
        return self.render()

    def render(self, prefix=''):
        raise NotImplemented("Implement in subclass")


class ModifierNode(RenderTree):
    def __init__(self, modifier, children, separator=''):
        self.modifier = modifier
        self.children = children
        self.separator = separator

    def render(self, prefix=''):
        if not self.children:
            return ''
        accumulated_modifiers = prefix + self.modifier
        rendered_children = [child.render(accumulated_modifiers) for child in self.children]
        return self.separator.join(rendered_children)


class TokenNode(RenderTree):
    def __init__(self, value='', clear=''):
        self.value = value
        self.clear = clear

    def render(self, prefix=''):
        return prefix + self.value + self.clear


def render_with(modifier):
    def __construct_modifier_tree(self, *tokens):
        clear = getattr(self, '__clear__', '')
        get_node = lambda t: t if isinstance(t, RenderTree) else TokenNode(t, clear)
        return ModifierNode(modifier, [get_node(token) for token in tokens])
    return __construct_modifier_tree


class _Pcol(object):
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