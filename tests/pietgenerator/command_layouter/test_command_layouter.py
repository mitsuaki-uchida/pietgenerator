
import pytest

from pietgenerator.command_layouter.command_layouter import ICommandLayouter
from pietgenerator.command_layouter.command_layouter import LayoutCommand
from pietgenerator.command_layouter.command_layouter import LayoutCommandError
from pietgenerator.piet_common import Codel
from pietgenerator.piet_common import Color
from pietgenerator.piet_common import Command


def test_layout_command_error_str():
    layout_command_error = LayoutCommandError()

    assert str(layout_command_error) == "LayoutCommandError: layout command failed."


@pytest.mark.parametrize('command, command_id', [
    pytest.param(LayoutCommand.ABORT,   200, id='ABORT'),
    pytest.param(LayoutCommand.NOT_USE, 201, id='NOT_USE'),
])
def test_layout_command_init(command, command_id):
    assert command._command_id == command_id


@pytest.mark.parametrize('command, expect', [
    pytest.param(LayoutCommand.ABORT,   'ABORT',   id='ABORT'),
    pytest.param(LayoutCommand.NOT_USE, 'NOT_USE', id='NOT_USE'),
])
def test_layout_command_str(command, expect):
    assert str(command) == expect


class TestCommandLayouter(ICommandLayouter):
    def __init__(self, debug, trace):
        super().__init__(debug, trace)
    
    def _do_layout_impl(self, commands, start_color, abort_program_color):
        return super()._do_layout_impl(commands, start_color, abort_program_color)


def test_i_command_Layouter_init():
    gen = TestCommandLayouter(True, False)
    assert gen._debug is True
    assert gen._trace is False

    gen = TestCommandLayouter(False, True)
    assert gen._debug is False
    assert gen._trace is True


def test_i_command_Layouter_do_layout_raise_not_implemented_error():
    gen = TestCommandLayouter(True, True)

    with pytest.raises(NotImplementedError):
        _ = gen._do_layout_impl([], Color.RED, Color.RED)
        

@pytest.mark.parametrize('x, y, color, codels, expect', [
    #
    # color
    #
    pytest.param(1, 1, Color.WHITE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.WHITE)},
    ], False, id='color=WHITE'),
    pytest.param(1, 1, Color.BLACK, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLACK)},
    ], False, id='color=BLACK'),
    pytest.param(1, 1, Color.LIGHT_RED, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_RED)},
    ], True, id='color=LIGHT_RED'),
    pytest.param(1, 1, Color.LIGHT_YELLOW, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_YELLOW)},
    ], True, id='color=LIGHT_YELLOW'),
    pytest.param(1, 1, Color.LIGHT_GREEN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_GREEN)},
    ], True, id='color=LIGHT_GREEN'),
    pytest.param(1, 1, Color.LIGHT_CYAN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_CYAN)},
    ], True, id='color=LIGHT_CYAN'),
    pytest.param(1, 1, Color.LIGHT_BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_BLUE)},
    ], True, id='color=LIGHT_BLUE'),
    pytest.param(1, 1, Color.LIGHT_MAGENTA, [
        {'x': 2, 'y': 1, 'value': Codel(Color.LIGHT_MAGENTA)},
    ], True, id='color=LIGHT_MAGENTA'),
    pytest.param(1, 1, Color.RED, [
        {'x': 2, 'y': 1, 'value': Codel(Color.RED)},
    ], True, id='color=RED'),
    pytest.param(1, 1, Color.YELLOW, [
        {'x': 2, 'y': 1, 'value': Codel(Color.YELLOW)},
    ], True, id='color=YELLOW'),
    pytest.param(1, 1, Color.GREEN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.GREEN)},
    ], True, id='color=GREEN'),
    pytest.param(1, 1, Color.CYAN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.CYAN)},
    ], True, id='color=CYAN'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='color=BLUE'),
    pytest.param(1, 1, Color.MAGENTA, [
        {'x': 2, 'y': 1, 'value': Codel(Color.MAGENTA)},
    ], True, id='color=MAGENTA'),
    pytest.param(1, 1, Color.DARK_RED, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_RED)},
    ], True, id='color=DARK_RED'),
    pytest.param(1, 1, Color.DARK_YELLOW, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_YELLOW)},
    ], True, id='color=DARK_YELLOW'),
    pytest.param(1, 1, Color.DARK_GREEN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_GREEN)},
    ], True, id='color=DARK_GREEN'),
    pytest.param(1, 1, Color.DARK_CYAN, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_CYAN)},
    ], True, id='color=DARK_CYAN'),
    pytest.param(1, 1, Color.DARK_BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_BLUE)},
    ], True, id='color=DARK_BLUE'),
    pytest.param(1, 1, Color.DARK_MAGENTA, [
        {'x': 2, 'y': 1, 'value': Codel(Color.DARK_MAGENTA)},
    ], True, id='color=DARK_MAGENTA'),

    #
    # position
    #

    # center
    pytest.param(1, 1, Color.BLUE, [
        {'x': 0, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 2, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(1, 1) conflict=no'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 1) conflict=right'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 1) conflict=bottom'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 1) conflict=left'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 1) conflict=top'),
    pytest.param(1, 1, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 1) conflict=all'),

    # right-center
    pytest.param(2, 1, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(2, 1) conflict=no'),
    pytest.param(2, 1, Color.BLUE, [
        {'x': 2, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 1) conflict=bottom'),
    pytest.param(2, 1, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 1) conflict=left'),
    pytest.param(2, 1, Color.BLUE, [
        {'x': 2, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 1) conflict=top'),
    pytest.param(2, 1, Color.BLUE, [
        {'x': 2, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 1) conflict=all'),

    # center-bottom
    pytest.param(1, 2, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(1, 2) conflict=no'),
    pytest.param(1, 2, Color.BLUE, [
        {'x': 2, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 2) conflict=right'),
    pytest.param(1, 2, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 2) conflict=top'),
    pytest.param(1, 2, Color.BLUE, [
        {'x': 0, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 2) conflict=left'),
    pytest.param(1, 2, Color.BLUE, [
        {'x': 2, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 2) conflict=all'),

    # left-center
    pytest.param(0, 1, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(0, 1) conflict=no'),
    pytest.param(0, 1, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 1) conflict=right'),
    pytest.param(0, 1, Color.BLUE, [
        {'x': 0, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 1) conflict=bottom'),
    pytest.param(0, 1, Color.BLUE, [
        {'x': 0, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 1) conflict=top'),
    pytest.param(0, 1, Color.BLUE, [
        {'x': 0, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 1) conflict=all'),

    # center-top
    pytest.param(1, 0, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(1, 0) conflict=no'),
    pytest.param(1, 0, Color.BLUE, [
        {'x': 2, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 0) conflict=right'),
    pytest.param(1, 0, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 0) conflict=bottom'),
    pytest.param(1, 0, Color.BLUE, [
        {'x': 0, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 0) conflict=left'),
    pytest.param(1, 0, Color.BLUE, [
        {'x': 2, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(1, 0) conflict=all'),

    # right-bottom
    pytest.param(2, 2, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(2, 2) conflict=no'),
    pytest.param(2, 2, Color.BLUE, [
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 2) conflict=left'),
    pytest.param(2, 2, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 2) conflict=top'),
    pytest.param(2, 2, Color.BLUE, [
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 2) conflict=all'),

    # left-bottom
    pytest.param(0, 2, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(0, 2) conflict=no'),
    pytest.param(0, 2, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 2) conflict=top'),
    pytest.param(0, 2, Color.BLUE, [
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 2) conflict=right'),
    pytest.param(0, 2, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 2, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 2) conflict=all'),

    # left-top
    pytest.param(0, 0, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(0, 0) conflict=no'),
    pytest.param(0, 0, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 0) conflict=right'),
    pytest.param(0, 0, Color.BLUE, [
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 0) conflict=bottom'),
    pytest.param(0, 0, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
        {'x': 0, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(0, 0) conflict=all'),

    # right-top
    pytest.param(2, 0, Color.BLUE, [
        {'x': 1, 'y': 1, 'value': Codel(Color.BLUE)},
    ], False, id='pos=(2, 0) conflict=no'),
    pytest.param(2, 0, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 0) conflict=bottom'),
    pytest.param(2, 0, Color.BLUE, [
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 0) conflict=left'),
    pytest.param(2, 0, Color.BLUE, [
        {'x': 2, 'y': 1, 'value': Codel(Color.BLUE)},
        {'x': 1, 'y': 0, 'value': Codel(Color.BLUE)},
    ], True, id='pos=(2, 0) conflict=all'),
])
def test_i_command_Layouter__is_conflict(x, y, color, codels, expect):
    base_codels = [None, Codel(Color.BLACK), Codel(Color.WHITE)]

    for base_codel in base_codels:
        grid = [[base_codel] * 3 for _ in range(3)]

        for codel in codels:
            grid[codel['y']][codel['x']] = codel['value']

        actual = ICommandLayouter._is_conflict(color, grid, x, y)

        assert expect == actual



@pytest.mark.parametrize('grid, expect', [
    pytest.param([[Codel(Color.RED), Codel(Color.RED), Codel(Color.RED)]], True, id='all codel'),
    pytest.param([[None, Codel(Color.RED), Codel(Color.RED)]], False, id='has 1 None'),
    pytest.param([[None, None, Codel(Color.RED)]], False, id='has 2 Nones'),
    pytest.param([[None, None, None]], False, id='all None'),
])
def test_i_command_Layouter__is_fill_all(grid, expect):
    actual = ICommandLayouter._is_fill_all(grid)

    assert expect == actual


@pytest.mark.parametrize('exclueds, expects', [
    pytest.param(
        None,
        [
            Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
            Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
            Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA
        ],
        id='exclude=None'),
    pytest.param(
        [],
        [
            Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
            Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
            Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA
        ],
        id='exclude=empty'),
    pytest.param(
        [Color.LIGHT_RED],
        [
            Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
            Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
            Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA
        ],
        id='exclude=LIGHT_RED'),
    pytest.param(
        [
            Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
            Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
            Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE
        ],
        [Color.DARK_MAGENTA],
        id='exclude=other than DARK_MAGENTA'),
    # raises RuntimeError
    # pytest.param(
    #     [
    #         Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
    #         Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
    #         Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA
    #     ],
    #     [None],
    #     id='exclude=all color'),
])
def test_i_command_Layouter__get_random_color(exclueds, expects):
    for _ in range(10000):
        actual = ICommandLayouter._get_random_color(exclueds)
        assert actual in expects


@pytest.mark.parametrize('exclueds', [
    pytest.param(
        [
            Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN, Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA,
            Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA,
            Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN, Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA
        ],
        id='exclude=all color'),
])
def test_i_command_Layouter__get_random_color_raises_runtime_error(exclueds):
    for _ in range(10000):
        with pytest.raises(RuntimeError):
            _ = ICommandLayouter._get_random_color(exclueds)


@pytest.mark.parametrize('exclueds, expects', [
    pytest.param(
        None,
        [
            Command.PUSH, Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
            Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER, Command.DUPLICATE
        ],
        id='exclude=None'),
    pytest.param(
        [],
        [
            Command.PUSH, Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
            Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER, Command.DUPLICATE
        ],
        id='exclude=empty'),
    pytest.param(
        [Command.PUSH],
        [
            Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
            Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER, Command.DUPLICATE
        ],
        id='exclude=PUSH'),
    pytest.param(
        [
            Command.PUSH, Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
            Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER
        ],
        [Command.DUPLICATE],
        id='exclude=other than DUPLICATE'),
    # raises RuntimeError
    # pytest.param(
    #     [
    #         Command.PUSH, Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
    #         Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER, Command.DUPLICATE
    #     ],
    #     [None],
    #     id='exclude=all command'),
])
def test_i_command_Layouter__get_random_command(exclueds, expects):
    for _ in range(10000):
        actual = ICommandLayouter._get_random_command(exclueds)
        assert actual in expects


@pytest.mark.parametrize('exclueds', [
    pytest.param(
        [
            Command.PUSH, Command.POP, Command.ADD, Command.SUBTRACT, Command.MULTIPLY,
            Command.DIVIDE, Command.MOD, Command.NOT, Command.GREATER, Command.DUPLICATE
        ],
        id='exclude=all command'),
])
def test_i_command_Layouter__get_random_command_raise_runtime_error(exclueds):
    for _ in range(10000):
        with pytest.raises(RuntimeError):
            _ = ICommandLayouter._get_random_command(exclueds)
