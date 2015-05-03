class RenderTree(object):
    @property
    def is_leaf(self):
        raise NotImplemented("Implement in subclass")

    def render(self):
        raise NotImplemented("Implement in subclass")


class ModifierNode(RenderTree):
    def __init__(self, modifier, children):
        self.modifier = modifier
        self.children = children

    @property
    def is_leaf(self):
        return False

    def render(self):
        if not self.children:
            return ''
        rendered_children = [child.render() for child in self.children]
        return self.modifier + ''.join(rendered_children)


class TokenNode(RenderTree):
    def __init__(self, value=None):
        self.value = value or ''

    @property
    def is_leaf(self):
        return True

    def render(self):
        return self.value + '[clear]'


class Renderer(object):
    def _render(self, color, tokens):
        if not tokens:
            return ''
        rendered_color = '[%s]' % color
        return ''.join(rendered_color + token + '[clear]' for token in tokens)

    def green(self, *tokens):
        return self._render('green', tokens)

    def bold(self, *tokens):
        return self._render('bold', tokens)

pcol = Renderer()