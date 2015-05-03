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


def _render_with(modifier):
    def __construct_modifier_tree(self, *tokens):
        token_nodes = [token if isinstance(token, RenderTree) else TokenNode(token, clear=self.__clear__) for token in tokens]
        return ModifierNode(modifier, token_nodes)
    return __construct_modifier_tree


class Renderer(object):
    __clear__ = '[clear]'
    
    green = _render_with('[green]')
    bold = _render_with('[bold]')


pcol = Renderer()