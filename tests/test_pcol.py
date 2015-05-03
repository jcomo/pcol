import unittest
from pcol import pcol, ModifierNode, TokenNode, render_with


class ModifierNodeTestCase(unittest.TestCase):
    def test_modifier_does_not_render_without_children(self):
        t = ModifierNode('red', [])
        self.assertEqual('', t.render())

    def test_modifier_renders_children(self):
        child = TokenNode('leaf')
        t = ModifierNode('[B]', [child])
        expected = '[B]%s' % child.render()
        self.assertEqual(expected, t.render())

    def test_modifier_renders_children_with_separator(self):
        left = TokenNode('left')
        right = TokenNode('right')
        t = ModifierNode('[B]', [left, right], separator=' ')
        expected = '[B]%s [B]%s' % (left.render(), right.render())
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


class MyRenderer(object):
    __clear__ = '[CL]'

    green = render_with('[G]')
    bold = render_with('[B]')


class RendererTestCase(unittest.TestCase):
    def setUp(self):
        self.renderer = MyRenderer()

    def test_render_nothing_should_be_empty_string(self):
        self.assertEqual('', str(self.renderer.green()))

    def test_no_clear_class_value_should_be_ok(self):

        class RendererWithoutClear(object):
            purple = render_with('[P]')

        renderer = RendererWithoutClear()
        renderer.purple('no clear')

    def test_render_with_one_token_should_render_with_color(self):
        output = self.renderer.green('hey')
        self.assertEqual('[G]hey[CL]', str(output))

    def test_render_with_multiple_tokens_should_render_all_independently(self):
        output = self.renderer.green('hey', 'there')
        self.assertEqual('[G]hey[CL][G]there[CL]', str(output))

    def test_render_with_two_modifiers(self):
        output = self.renderer.green('hey', self.renderer.bold('there'))
        self.assertEqual('[G]hey[CL][G][B]there[CL]', str(output))


class LibraryDefaultsTestCase(unittest.TestCase):
    """Test that the pcol object uses the proper defaults"""

    def test_has_appropriate_modifiers(self):
        self.assertEqual('\033[1mHI\033[0m', str(pcol.bold('HI')))
        self.assertEqual('\033[4mHI\033[0m', str(pcol.underline('HI')))

        self.assertEqual('\033[30mHI\033[0m', str(pcol.black('HI')))
        self.assertEqual('\033[31mHI\033[0m', str(pcol.red('HI')))
        self.assertEqual('\033[32mHI\033[0m', str(pcol.green('HI')))
        self.assertEqual('\033[33mHI\033[0m', str(pcol.yellow('HI')))
        self.assertEqual('\033[34mHI\033[0m', str(pcol.blue('HI')))
        self.assertEqual('\033[35mHI\033[0m', str(pcol.magenta('HI')))
        self.assertEqual('\033[36mHI\033[0m', str(pcol.cyan('HI')))
        self.assertEqual('\033[37mHI\033[0m', str(pcol.white('HI')))

    def test_it_separates_with_spaces(self):
        expected = str(pcol.green('Hello')) + ' ' + str(pcol.green('World!'))
        self.assertEqual(expected, str(pcol.green('Hello', 'World!')))