import unittest
from pcol import ModifierNode, TokenNode, pcol


class ModifierNodeTestCase(unittest.TestCase):
    def test_modifier_tree_is_not_leaf(self):
        t = ModifierNode('green', ['child1', 'child2'])
        assert not t.is_leaf, "Expected modifier tree not to be leaf"


class TokenNodeTestCase(unittest.TestCase):
    def test_token_is_leaf(self):
        t = TokenNode('leaf')
        assert t.is_leaf, "Expected token to be leaf"

    def test_token_render_renders_with_clear(self):
        t = TokenNode('hey')
        self.assertEqual('hey[clear]', t.render())

class RendererTestCase(unittest.TestCase):
    def test_render_nothing_should_be_empty_string(self):
        self.assertEqual('', str(pcol.green()))

    def test_render_with_one_token_should_render_with_color(self):
        output = pcol.green('hey')
        self.assertEqual('[green]hey[clear]', str(output))

    def test_render_with_multiple_tokens_should_render_all_independently(self):
        output = pcol.green('hey', 'there')
        self.assertEqual('[green]hey[clear][green]there[clear]', str(output))

    @unittest.skip("Not done yet")
    def test_render_with_two_modifiers(self):
        output = pcol.green('hey', pcol.bold('there'))
        self.assertEqual('[green]hey[clear][green][bold]there[clear]', str(output))