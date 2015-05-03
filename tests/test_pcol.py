import unittest
from pcol import ModifierNode, TokenNode, pcol


class ModifierNodeTestCase(unittest.TestCase):
    def test_modifier_node_is_not_leaf(self):
        t = ModifierNode('green', [TokenNode('child1'), TokenNode('child2')])
        assert not t.is_leaf, "Expected modifier tree not to be leaf"

    def test_modifier_does_not_render_without_children(self):
        t = ModifierNode('red', [])
        self.assertEqual('', t.render())

    def test_modifier_renders_children(self):
        child = TokenNode('leaf')
        t = ModifierNode('[blue]', [child])
        expected = '[blue]%s' % child.render()
        self.assertEqual(expected, t.render())

    def test_modifier_renders_all_children(self):
        child1 = TokenNode('child1')
        child2 = TokenNode('child2')
        t = ModifierNode('[yellow]', [child1, child2])
        expected = '[yellow]%s[yellow]%s' % (child1.render(), child2.render())
        self.assertEqual(expected, t.render())

    def test_modifier_renders_with_complex_children(self):
        left = TokenNode('Why')
        middle = ModifierNode('[bold]', [TokenNode('hello')])
        right = TokenNode('there')
        t = ModifierNode('[green]', [left, middle, right])
        expected = '[green]%s[green]%s[green]%s' % (left.render(), middle.render(), right.render())
        self.assertEqual(expected, t.render())

    def test_complex_render_tree(self):
        clear = '[CL]'

        some = TokenNode('Some', clear=clear)

        really = TokenNode('really', clear=clear)
        important = ModifierNode('[underline]', [TokenNode('important', clear=clear)])
        info = TokenNode('information', clear=clear)
        callout = ModifierNode('[bold]', [really, important])

        t = ModifierNode('[red]', [some, callout, info])
        expected = '[red]Some[CL][red][bold]really[CL][red][bold][underline]important[CL][red]information[CL]'
        self.assertEqual(expected, t.render())


class TokenNodeTestCase(unittest.TestCase):
    def test_token_node_is_leaf(self):
        t = TokenNode('leaf')
        assert t.is_leaf, "Expected token to be leaf"

    def test_clear_is_nothing_by_default(self):
        t = TokenNode('hey')
        self.assertEqual('hey', t.render())

    def test_empty_token_just_renders_clear(self):
        t = TokenNode(clear='[clear]')
        self.assertEqual('[clear]', t.render())

    def test_token_render_renders_with_clear(self):
        t = TokenNode('hey', clear='[clear]')
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