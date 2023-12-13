
import copy
import random

import pytest

from pietgenerator.command_generator.factorize_generator import FactorizeCommandGenerator
from pietgenerator.piet_common import Codel
from pietgenerator.piet_common import Color
from pietgenerator.piet_common import Command
from pietgenerator.piet_common import DirectionPointer
from pietgenerator.piet_common import get_command_from_color
from pietgenerator.command_layouter.command_layouter import LayoutCommand
from pietgenerator.command_layouter.command_layouter import LayoutCommandError
from pietgenerator.command_layouter.square_layouter import GridTooSmallError
from pietgenerator.command_layouter.square_layouter import SquareLayouter


def test_grid_too_small_error_init():
    w = 1
    h = 2
    x = 3
    y = 4

    grid_too_small_error = GridTooSmallError(w, h, x, y)

    assert grid_too_small_error._w == w
    assert grid_too_small_error._h == h
    assert grid_too_small_error._x == x
    assert grid_too_small_error._y == y


def test_grid_too_small_error_str():
    w = 1
    h = 2
    x = 3
    y = 4

    grid_too_small_error = GridTooSmallError(w, h, x, y)

    assert str(grid_too_small_error) == (f"GridTooSmallError: grid is too small. w={w} h={h} pos=({x}, {y})")


def test_square_layouter_init():
    layouter = SquareLayouter()

    assert layouter._debug is True
    assert layouter._trace is False


def _inspect_layout(layouter, grid, expect_commands, start_color, abort_program_color):
    stack = []
    actual_commands = []

    x = 0
    y = 0
    dp = DirectionPointer.RIGHT
    color = start_color

    abort_program_x = (len(grid[0]) - 1) // 2
    abort_program_y = len(grid) // 2

    while True:
        next_color = grid[y][x].color
        command = get_command_from_color(color, next_color)

        if (x == abort_program_x) and (y == abort_program_y):
            # 停止用プログラムに到達
            assert not command in [Command.IN_CHAR, Command.IN_NUMBER, Command.OUT_CHAR, Command.OUT_NUMBER]
            break

        try:
            if command is Command.NONE:
                assert ((x == 0) and (y == 0)) or (color is Color.WHITE)
            elif command is Command.PUSH:
                assert not next_color in [Color.WHITE, Color.BLACK]
                stack.append(1)
            elif command is Command.POP:
                assert not next_color in [Color.WHITE, Color.BLACK]
                stack.pop(-1)
            elif command is Command.ADD:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(value2 + value1)
            elif command is Command.SUBTRACT:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(value2 - value1)
            elif command is Command.MULTIPLY:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(value2 * value1)
            elif command is Command.DIVIDE:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(value2 // value1)
            elif command is Command.MOD:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(value2 % value1)
            elif command is Command.NOT:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value = stack.pop(-1)
                stack.append(0 if value != 0 else 1)
            elif command is Command.GREATER:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
                stack.append(1 if value2 > value1 else 0)
            elif command is Command.POINTER:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value = stack.pop(-1)
                dp = DirectionPointer.rotate(dp, value)
            elif command is Command.SWITCH:
                assert False
            elif command is Command.DUPLICATE:
                assert not next_color in [Color.WHITE, Color.BLACK]
                stack.append(stack[-1])
            elif command is Command.ROLL:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value1 = stack.pop(-1)
                value2 = stack.pop(-1)
            elif command is Command.IN_NUMBER:
                assert False
            elif command is Command.IN_CHAR:
                assert False
            elif command is Command.OUT_NUMBER:
                assert False
            elif command is Command.OUT_CHAR:
                assert not next_color in [Color.WHITE, Color.BLACK]
                value = stack.pop(-1)
            elif command is Command.FREE_ZONE:
                assert next_color is Color.WHITE
            elif command is Command.EDGE:
                assert False

        except IndexError:
            # stackが範囲外の操作となった場合はIndexErrorが送出されるが
            # Pietの以下の仕様により無視して良い
            # Any operations which cannot be performed
            # (such as popping values when not enough are on the stack)
            # are simply ignored,
            # and processing continues with the next command.
            pass
        except ZeroDivisionError:
            # DIVコマンドによりゼロ除算となった場合はZeroDivisionErrorが送出されるが
            # Pietの以下の仕様により無視して良い（と判断する）
            # it is handled as an implementation-dependent error,
            # though simply ignoring the command is recommended.
            pass

        if command is Command.NONE:
            if (x == 0) and (y == 0):
                actual_commands.append(command)
            else:
                # 先頭以外のNONEコマンドの直前は、FREE_ZONEコマンド
                before_none_command = actual_commands.pop(-1)
                assert before_none_command is Command.FREE_ZONE
        elif command is Command.POINTER:
            # POINTERコマンドの直前は、メッセージ用コマンド外のPUSHコマンド
            before_pointer_command = actual_commands.pop(-1)
            assert before_pointer_command is Command.PUSH
        else:
            # メッセージ用コマンド
            actual_commands.append(command)

        assert (0 <= x < len(grid[0])) and (0 <= y < len(grid))
        assert not layouter._is_conflict(grid[y][x].color, grid, x, y)

        x += dp.dx
        y += dp.dy
        color = next_color

    # メッセージ用コマンド部のみテスト
    assert expect_commands == actual_commands[:len(expect_commands)]


@pytest.mark.parametrize('message, start_color, abort_program_color', [
    pytest.param('A', Color.LIGHT_RED, Color.DARK_MAGENTA, id='message="A"'),
    pytest.param('Hello World!', Color.CYAN, Color.GREEN, id='message="Hello World!"'),
    pytest.param('Merry Christmas!!', Color.DARK_MAGENTA, Color.LIGHT_RED, id='message="Merry Christmas!!"'),
])
def test_do_layout(message, start_color, abort_program_color):
    gen = FactorizeCommandGenerator()

    commands = gen.generate(message)
    message_commands = copy.copy(commands)

    layouter = SquareLayouter()
    grid = layouter.do_layout(commands, start_color, abort_program_color)

    # プログラムが停止プログラムに到達しメッセージ用コマンドがcommandsの順に配置されているかテスト
    _inspect_layout(layouter, grid, message_commands, start_color, abort_program_color)

    # 先頭に配置されたCodelの色に問題がないかテスト
    assert grid[0][0].color is start_color

    # すべてのgridのcolorに問題がないかテスト
    initial_grid = layouter._create_grid(len(grid[0]), len(grid), abort_program_color)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not initial_grid[y][x]:
                color = grid[y][x].color

                assert color is not Color.BLACK
                assert not layouter._is_conflict(color, grid, x, y)
            else:
                initial_color = initial_grid[y][x].color
                color = grid[y][x].color

                if initial_color is Color.BLACK:
                    assert color is Color.BLACK
                elif initial_color is abort_program_color:
                    assert color is abort_program_color
                else:
                    assert False


def test_do_layout_too_long_message(mocker):
    message = "".join([chr(random.randrange(1, 256)) for _ in range(1000)])
    start_color = Color.LIGHT_RED
    abort_program_color = Color.DARK_MAGENTA

    gen = FactorizeCommandGenerator()

    commands = gen.generate(message)
    message_commands = copy.copy(commands)

    layouter = SquareLayouter()

    # 競合発生状況の確認用
    # is_conflict_spy = mocker.spy(layouter, "_is_conflict")

    grid = layouter.do_layout(commands, start_color, abort_program_color)

    # conflict_positions = {}
    # for call_args in is_conflict_spy.call_args_list:
    #    color, grid, x, y = call_args.args
    #
    #     if not (x, y) in conflict_positions:
    #         conflict_positions[(x, y)] = 0
    #
    #    conflict_positions[(x, y)] += 1

    # プログラムが停止プログラムに到達しメッセージ用コマンドがcommandsの順に配置されているかテスト
    _inspect_layout(layouter, grid, message_commands, start_color, abort_program_color)

    # 先頭に配置されたCodelの色に問題がないかテスト
    assert grid[0][0].color is start_color

    # すべてのgridのcolorに問題がないかテスト
    initial_grid = layouter._create_grid(len(grid[0]), len(grid), abort_program_color)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not initial_grid[y][x]:
                color = grid[y][x].color

                assert color is not Color.BLACK
                assert not layouter._is_conflict(color, grid, x, y)
            else:
                initial_color = initial_grid[y][x].color
                color = grid[y][x].color

                if initial_color is Color.BLACK:
                    assert color is Color.BLACK
                elif initial_color is abort_program_color:
                    assert color is abort_program_color
                else:
                    assert False


@pytest.mark.parametrize('side_effect__put_commands, side_effect__put_commands_to_abort_area, expect_w, expect_h', [
    pytest.param(
        [(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        [(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        7, 7, id='raises: no'),
    pytest.param(
        [GridTooSmallError(0, 0, 7, 7),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        [(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        8, 8, id='raises: _put_codels x 1'),
    pytest.param(
        [GridTooSmallError(0, 0, 7, 7),
         GridTooSmallError(0, 0, 7, 7),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        [(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        9, 9, id='raises: _put_codels x 2'),
    pytest.param(
        [(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        [GridTooSmallError(0, 0, 7, 7),
         GridTooSmallError(0, 0, 7, 7),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        9, 9, id='raises: _put_codels_to_abort_area x 2'),
    pytest.param(
        [GridTooSmallError(0, 0, 7, 7),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        [GridTooSmallError(0, 0, 7, 7),
         (0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)],
        9, 9, id='raises: _put_codels x 1, _put_codels_to_abort_area x 1'),
])
def test__do_layout_expand_grid(side_effect__put_commands, side_effect__put_commands_to_abort_area, expect_w, expect_h, mocker):
    layouter = SquareLayouter()

    mocker.patch.object(layouter, "_predict_grid_size", mocker.MagicMock(return_value=(7, 7)))
    mocker.patch.object(layouter, "_put_codels", mocker.MagicMock(side_effect=side_effect__put_commands))
    mocker.patch.object(layouter, "_put_codels_to_abort_area", mocker.MagicMock(side_effect=side_effect__put_commands_to_abort_area))
    mocker.patch.object(layouter, "_put_codels_to_abort_program", mocker.MagicMock(return_value=(0, 0, DirectionPointer.RIGHT, Color.LIGHT_RED)))
    mocker.patch.object(layouter, "_put_to_empty_cells", mocker.MagicMock())
    mocker.patch.object(layouter, "_is_fill_all", mocker.MagicMock(return_value=True))

    grid = layouter.do_layout([], Color.LIGHT_RED, Color.LIGHT_GREEN)

    assert expect_w == len(grid)
    assert expect_h == len(grid[0])


def test_generate_raises_generate_command_error(mocker):
    layouter = SquareLayouter()
    mocker.patch.object(layouter, "_do_layout_impl", mocker.MagicMock(side_effect=LayoutCommandError))

    with pytest.raises(LayoutCommandError):
        _ = layouter.do_layout([], Color.LIGHT_RED, Color.LIGHT_GREEN)


@pytest.mark.parametrize('command_num, expect_w, expect_h', [
    pytest.param(  4,  7,  7, id="(minimum): 4"),
    pytest.param( 13,  8,  8, id="' ': 13"),
    pytest.param( 23,  9,  9, id="'A': 23"),
    pytest.param( 93, 13, 13, id="'Xmas': 93"),
    pytest.param(233, 18, 18, id="'Hello World!': 233"),
    pytest.param(371, 22, 22, id="'Merry Christmas!!': 371"),
])
def test__predict_grid_size(command_num, expect_w, expect_h):
    layouter = SquareLayouter()
    actual_w, actual_h = layouter._predict_grid_size([Command.NONE] * command_num)

    assert expect_w == actual_w
    assert expect_h == actual_h


@pytest.mark.parametrize('w, h, expect', [
    pytest.param(1, 1, SquareLayouter._ABORT_PROGRAM_ODD,  id='odd'),
    pytest.param(2, 2, SquareLayouter._ABORT_PROGRAM_EVEN, id='even'),
])
def test__get_abort_program(w, h, expect):
    layouter = SquareLayouter()
    actual = layouter._get_abort_program(w, h)

    assert expect == actual


@pytest.mark.parametrize('w, h, expect', [
    pytest.param(7, 7, [
        *[[None] * (5 + (1 * 2))] * 1,
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_ODD[0], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_ODD[1], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_ODD[2], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_ODD[3], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_ODD[4], *[None] * 1],
        *[[None] * (5 + (1 * 2))] * 1,
    ],  id='7 x 7'),
    pytest.param(8, 8, [
        *[[None] * (6 + (1 * 2))] * 1,
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[0], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[1], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[2], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[3], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[4], *[None] * 1],
        [*[None] * 1, *SquareLayouter._ABORT_PROGRAM_EVEN[5], *[None] * 1],
        *[[None] * (6 + (1 * 2))] * 1,
    ], id='8 x 8'),
    pytest.param(9, 9, [
        *[[None] * (5 + (2 * 2))] * 2,
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_ODD[0], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_ODD[1], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_ODD[2], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_ODD[3], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_ODD[4], *[None] * 2],
        *[[None] * (5 + (2 * 2))] * 2,
    ],  id='9 x 9'),
    pytest.param(10, 10, [
        *[[None] * (6 + (2 * 2))] * 2,
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[0], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[1], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[2], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[3], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[4], *[None] * 2],
        [*[None] * 2, *SquareLayouter._ABORT_PROGRAM_EVEN[5], *[None] * 2],
        *[[None] * (6 + (2 * 2))] * 2,
    ], id='10 x 10'),
])
def test__create_grid(w, h, expect):
    layouter = SquareLayouter()
    grid = layouter._create_grid(w, h, Color.LIGHT_GREEN)

    for expect_row, actual_row in zip(expect, grid):
        for expect_command, actual in zip(expect_row, actual_row):
            if expect_command is LayoutCommand.ABORT:
                assert actual.color is Color.LIGHT_GREEN
            elif expect_command is Command.EDGE:
                assert actual.color is Color.BLACK
            elif expect_command is None:
                assert actual is None
            else:
                assert False


@pytest.mark.parametrize('w, h, expect', [
    pytest.param(7, 7, [
        [False, False, False, False, False, False, False],
        [True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  False],
        [False, False, False, False, False, False, False],
    ],  id='7 x 7'),
    pytest.param(8, 8, [
        [False, False, False, False, False, False, False, False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [True,  True,  True,  True,  True,  True,  True,  False],
        [False, False, False, False, False, False, False, False],
    ], id='8 x 8'),
    pytest.param(9, 9, [
        [False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False],
        [False, True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  False, False],
        [False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False],
    ],  id='9 x 9'),
    pytest.param(10, 10, [
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, True,  True,  True,  True,  True,  True,  True,  False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
    ], id='10 x 10'),
])
def test__is_in_abort_program_area(w, h, expect):
    layouter = SquareLayouter()
    grid = layouter._create_grid(w, h, Color.LIGHT_GREEN)

    for y, expect_row in enumerate(expect):
        for x, expect in enumerate(expect_row):
            assert expect is layouter._is_in_abort_program_area(grid, x, y)


@pytest.mark.parametrize('grid, random_colors', [
    pytest.param([
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
        [Color.LIGHT_BLUE, Color.BLUE],
        id='all empty'),
    pytest.param([
            [None,             Codel(Color.BLUE),    None],
            [Codel(Color.RED), None,                 Codel(Color.YELLOW)],
            [None,             Codel(Color.MAGENTA), None],
        ],
        [Color.LIGHT_BLUE],
        id='checkered'),
    pytest.param([
            [Codel(Color.LIGHT_BLUE), Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE)],
            [Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE), Codel(Color.BLUE)],
            [Codel(Color.LIGHT_BLUE), Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE)],
            [Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE), Codel(Color.BLUE)],
            [Codel(Color.LIGHT_BLUE), Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE)],
            [Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE), Codel(Color.BLUE)],
            [Codel(Color.LIGHT_BLUE), Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE)],
            [Codel(Color.BLUE),       Codel(Color.LIGHT_BLUE), Codel(Color.BLUE)],
        ],
        [],
        id='all command without empty'),
])
def test__put_to_empty_cells(grid, random_colors, mocker):
    expect = copy.deepcopy(grid)

    layouter = SquareLayouter()
    mocker.patch.object(
        layouter,
        '_get_random_color',
        side_effect=lambda exclude_colors: random.choice(
            [color for color in random_colors if color not in exclude_colors]))
    layouter._put_to_empty_cells(grid)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            assert not grid[y][x] is None
            assert not layouter._is_conflict(grid[y][x].color, grid, x, y)

            if expect[y][x] is not None:
                assert expect[y][x].color == grid[y][x].color 
