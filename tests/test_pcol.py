import unittest
from pcol import ModifierNode, TokenNode, pcol


class ModifierNodeTestCase(unittest.TestCase):
    def test_modifier_does_not_render_without_children(self):
        t = ModifierNode('red', [])
        self.assertEqual('', t.render())

    def test_modifier_renders_children(self):
        child = TokenNode('leaf')
        t = ModifierNode('[B]', [child])
        expected = '[B]%s' % child.render()
        self.assertEqual(expected, t.render())

    def test_modifier_renders_all_children(self):
        child1 = TokenNode('child1')
        child2 = TokenNode('child2')
        t = ModifierNode('[Y]', [child1, child2])
        expected = '[Y]%s[Y]%s' % (child1.render(), child2.render())
        self.assertEqual(expected, t.render())

    def test_modifier_renders_with_complex_children(self):
        left = TokenNode('Why')
        middle = ModifierNode('[B]', [TokenNode('hello')])
        right = TokenNode('there')
        t = ModifierNode('[G]', [left, middle, right])
        expected = '[G]%s[G]%s[G]%s' % (left.render(), middle.render(), right.render())
        self.assertEqual(expected, t.render())

    def test_complex_render_tree(self):
        clear = '[CL]'

        some = TokenNode('Some', clear=clear)

        really = TokenNode('really', clear=clear)
        important = ModifierNode('[U]', [TokenNode('important', clear=clear)])
        info = TokenNode('information', clear=clear)
        callout = ModifierNode('[B]', [really, important])

        t = ModifierNode('[R]', [some, callout, info])
        expected = '[R]Some[CL][R][B]really[CL][R][B][U]important[CL][R]information[CL]'
        self.assertEqual(expected, t.render())


class TokenNodeTestCase(unittest.TestCase):
    def test_clear_is_nothing_by_default(self):
        t = TokenNode('hey')
        self.assertEqual('hey', t.render())

    def test_empty_token_just_renders_clear(self):
        t = TokenNode(clear='[clear]')
        self.assertEqual('[clear]', t.render())

    def test_token_renders_with_clear(self):
        t = TokenNode('hey', clear='[clear]')
        self.assertEqual('hey[clear]', t.render())

    def test_token_renders_with_supplied_prefix(self):
        t = TokenNode('hey')
        self.assertEqual('[A]hey', t.render('[A]'))


class RendererTestCase(unittest.TestCase):
    def test_render_nothing_should_be_empty_string(self):
        self.assertEqual('', str(pcol.green()))

    def test_render_with_one_token_should_render_with_color(self):
        output = pcol.green('hey')
        self.assertEqual('[green]hey[clear]', str(output))

    def test_render_with_multiple_tokens_should_render_all_independently(self):
        output = pcol.green('hey', 'there')
        self.assertEqual('[green]hey[clear][green]there[clear]', str(output))

    def test_render_with_two_modifiers(self):
        output = pcol.green('hey', pcol.bold('there'))
        self.assertEqual('[green]hey[clear][green][bold]there[clear]', str(output))