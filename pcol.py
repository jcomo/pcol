class RenderTree(object):
    def __str__(self):
        return self.render()

    def render(self, prefix=''):
        raise NotImplemented("Implement in subclass")


class ModifierNode(RenderTree):
    def __init__(self, modifier, children):
        self.modifier = modifier
        self.children = children

    def render(self, prefix=''):
        if not self.children:
            return ''
        accumulated_modifiers = prefix + self.modifier
        rendered_children = [child.render(accumulated_modifiers) for child in self.children]
        return ''.join(rendered_children)


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


class Renderer(object):
    __clear__ = '[clear]'

    green = render_with('[green]')
    bold = render_with('[bold]')


pcol = Renderer()