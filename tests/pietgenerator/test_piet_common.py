
import pytest

from pietgenerator.piet_common import Codel
from pietgenerator.piet_common import CodelChooser
from pietgenerator.piet_common import Color
from pietgenerator.piet_common import Command
from pietgenerator.piet_common import DirectionPointer
from pietgenerator.piet_common import get_command_from_color
from pietgenerator.piet_common import get_color_from_command


@pytest.mark.parametrize('dp, index, dx, dy', [
    pytest.param(DirectionPointer.RIGHT, 0,  1,  0, id='RIGHT'),
    pytest.param(DirectionPointer.DOWN,  1,  0,  1, id='DOWN'),
    pytest.param(DirectionPointer.LEFT,  2, -1,  0, id='LEFT'),
    pytest.param(DirectionPointer.UP,    3,  0, -1, id='UP'),
])
def test_direction_pointer_init(dp, index, dx, dy):
    assert dp._index == index
    assert dp._dx == dx
    assert dp._dy == dy


@pytest.mark.parametrize('dp, expect', [
    pytest.param(DirectionPointer.RIGHT, 'RIGHT', id='RIGHT'),
    pytest.param(DirectionPointer.DOWN,  'DOWN',  id='DOWN'),
    pytest.param(DirectionPointer.LEFT,  'LEFT',  id='LEFT'),
    pytest.param(DirectionPointer.UP,    'UP',    id='UP'),
])
def test_direction_pointer_str(dp, expect):
    assert str(dp) == expect


@pytest.mark.parametrize('dp, dx, dy', [
    pytest.param(DirectionPointer.RIGHT, 1,  0, id='RIGHT'),
    pytest.param(DirectionPointer.DOWN,  0,  1, id='DOWN'),
    pytest.param(DirectionPointer.LEFT, -1,  0, id='LEFT'),
    pytest.param(DirectionPointer.UP,    0, -1, id='UP'),
])
def test_direction_pointer_properties(dp, dx, dy):
    assert dp.dx == dx
    assert dp.dy == dy


@pytest.mark.parametrize('dp, rotate_num, expect', [
    pytest.param(DirectionPointer.RIGHT,  0, DirectionPointer.RIGHT, id='RIGHT:   0'),
    pytest.param(DirectionPointer.RIGHT,  1, DirectionPointer.DOWN,  id='RIGHT: + 1'),
    pytest.param(DirectionPointer.RIGHT,  2, DirectionPointer.LEFT,  id='RIGHT: + 2'),
    pytest.param(DirectionPointer.RIGHT,  3, DirectionPointer.UP,    id='RIGHT: + 3'),
    pytest.param(DirectionPointer.RIGHT,  4, DirectionPointer.RIGHT, id='RIGHT: + 4'),
    pytest.param(DirectionPointer.RIGHT, -1, DirectionPointer.UP,    id='RIGHT: - 1'),
    pytest.param(DirectionPointer.RIGHT, -2, DirectionPointer.LEFT,  id='RIGHT: - 2'),
    pytest.param(DirectionPointer.RIGHT, -3, DirectionPointer.DOWN,  id='RIGHT: - 3'),
    pytest.param(DirectionPointer.RIGHT, -4, DirectionPointer.RIGHT, id='RIGHT: - 4'),

    pytest.param(DirectionPointer.DOWN,   0, DirectionPointer.DOWN,  id='DOWN:   0'),
    pytest.param(DirectionPointer.DOWN,   1, DirectionPointer.LEFT,  id='DOWN: + 1'),
    pytest.param(DirectionPointer.DOWN,   2, DirectionPointer.UP,    id='DOWN: + 2'),
    pytest.param(DirectionPointer.DOWN,   3, DirectionPointer.RIGHT, id='DOWN: + 3'),
    pytest.param(DirectionPointer.DOWN,   4, DirectionPointer.DOWN,  id='DOWN: + 4'),
    pytest.param(DirectionPointer.DOWN,  -1, DirectionPointer.RIGHT, id='DOWN: - 1'),
    pytest.param(DirectionPointer.DOWN,  -2, DirectionPointer.UP,    id='DOWN: - 2'),
    pytest.param(DirectionPointer.DOWN,  -3, DirectionPointer.LEFT,  id='DOWN: - 3'),
    pytest.param(DirectionPointer.DOWN,  -4, DirectionPointer.DOWN,  id='DOWN: - 4'),

    pytest.param(DirectionPointer.LEFT,   0, DirectionPointer.LEFT,  id='LEFT:   0'),
    pytest.param(DirectionPointer.LEFT,   1, DirectionPointer.UP,    id='LEFT: + 1'),
    pytest.param(DirectionPointer.LEFT,   2, DirectionPointer.RIGHT, id='LEFT: + 2'),
    pytest.param(DirectionPointer.LEFT,   3, DirectionPointer.DOWN,  id='LEFT: + 3'),
    pytest.param(DirectionPointer.LEFT,   4, DirectionPointer.LEFT,  id='LEFT: + 4'),
    pytest.param(DirectionPointer.LEFT,  -1, DirectionPointer.DOWN,  id='LEFT: - 1'),
    pytest.param(DirectionPointer.LEFT,  -2, DirectionPointer.RIGHT, id='LEFT: - 2'),
    pytest.param(DirectionPointer.LEFT,  -3, DirectionPointer.UP,    id='LEFT: - 3'),
    pytest.param(DirectionPointer.LEFT,  -4, DirectionPointer.LEFT,  id='LEFT: - 4'),

    pytest.param(DirectionPointer.UP,     0, DirectionPointer.UP,    id='UP:   0'),
    pytest.param(DirectionPointer.UP,     1, DirectionPointer.RIGHT, id='UP: + 1'),
    pytest.param(DirectionPointer.UP,     2, DirectionPointer.DOWN,  id='UP: + 2'),
    pytest.param(DirectionPointer.UP,     3, DirectionPointer.LEFT,  id='UP: + 3'),
    pytest.param(DirectionPointer.UP,     4, DirectionPointer.UP,    id='UP: + 4'),
    pytest.param(DirectionPointer.UP,    -1, DirectionPointer.LEFT,  id='UP: - 1'),
    pytest.param(DirectionPointer.UP,    -2, DirectionPointer.DOWN,  id='UP: - 2'),
    pytest.param(DirectionPointer.UP,    -3, DirectionPointer.RIGHT, id='UP: - 3'),
    pytest.param(DirectionPointer.UP,    -4, DirectionPointer.UP,    id='UP: - 4'),
])
def test_direction_pointer_rotate(dp, rotate_num, expect):
    actual = DirectionPointer.rotate(dp, rotate_num)
    assert expect is actual


@pytest.mark.parametrize('index, expect', [
    pytest.param( 0, DirectionPointer.RIGHT, id='RIGHT'),
    pytest.param( 1, DirectionPointer.DOWN,  id='DOWN'),
    pytest.param( 2, DirectionPointer.LEFT,  id='LEFT'),
    pytest.param( 3, DirectionPointer.UP,    id='UP'),
])
def test_direction_pointer_index_of(index, expect):
    actual = DirectionPointer.index_of(index)
    assert expect is actual


@pytest.mark.parametrize('index', [
    pytest.param( 4, id='index=4'),
    pytest.param(-1, id='index=-1'),
])
def test_direction_pointer_index_of_raise_value_error(index):
    with pytest.raises(ValueError):
        _ = DirectionPointer.index_of(index)


@pytest.mark.parametrize('cc, index', [
    pytest.param(CodelChooser.RIGHT, 0, id='RIGHT'),
    pytest.param(CodelChooser.LEFT,  1, id='LEFT'),
])
def test_codel_chooser_init(cc, index):
    assert cc._index == index


@pytest.mark.parametrize('cc, expect', [
    pytest.param(CodelChooser.RIGHT, 'RIGHT', id='RIGHT'),
    pytest.param(CodelChooser.LEFT,  'LEFT',  id='LEFT'),
])
def test_codel_chooser_str(cc, expect):
    assert str(cc) == expect


@pytest.mark.parametrize('cc, switch_num, expect', [
    pytest.param(CodelChooser.RIGHT,  0, CodelChooser.RIGHT, id='RIGHT:   0'),
    pytest.param(CodelChooser.RIGHT,  1, CodelChooser.LEFT,  id='RIGHT: + 1'),
    pytest.param(CodelChooser.RIGHT,  2, CodelChooser.RIGHT, id='RIGHT: + 2'),
    pytest.param(CodelChooser.RIGHT, -1, CodelChooser.LEFT,  id='RIGHT: - 1'),
    pytest.param(CodelChooser.RIGHT, -2, CodelChooser.RIGHT, id='RIGHT: - 2'),

    pytest.param(CodelChooser.LEFT,   0, CodelChooser.LEFT,  id='LEFT:   0'),
    pytest.param(CodelChooser.LEFT,   1, CodelChooser.RIGHT, id='LEFT: + 1'),
    pytest.param(CodelChooser.LEFT,   2, CodelChooser.LEFT,  id='LEFT: + 2'),
    pytest.param(CodelChooser.LEFT,  -1, CodelChooser.RIGHT, id='LEFT: - 1'),
    pytest.param(CodelChooser.LEFT,  -2, CodelChooser.LEFT,  id='LEFT: - 2'),
])
def test_codel_chooser_switch(cc, switch_num, expect):
    actual = CodelChooser.switch(cc, switch_num)
    assert expect is actual


@pytest.mark.parametrize('index, expect', [
    pytest.param( 0, CodelChooser.RIGHT, id='RIGHT'),
    pytest.param( 1, CodelChooser.LEFT,  id='LEFT'),
])
def test_codel_chooser_index_of(index, expect):
    actual = CodelChooser.index_of(index)
    assert expect is actual


@pytest.mark.parametrize('index', [
    pytest.param( 2, id='index=2'),
    pytest.param(-1, id='index=-1'),
])
def test_codel_chooser_index_of_raise_valu_error(index):
    with pytest.raises(ValueError):
        _ = CodelChooser.index_of(index)


@pytest.mark.parametrize('command, command_id, hue_step, lightness_step', [
    pytest.param(Command.NONE,         0, 0, 0, id='NONE'),
    pytest.param(Command.PUSH,         1, 0, 1, id='PUSH'),
    pytest.param(Command.POP,          2, 0, 2, id='POP'),
    pytest.param(Command.ADD,          3, 1, 0, id='ADD'),
    pytest.param(Command.SUBTRACT,     4, 1, 1, id='SUBTRACT'),
    pytest.param(Command.MULTIPLY,     5, 1, 2, id='MULTIPLY'),
    pytest.param(Command.DIVIDE,       6, 2, 0, id='DIVIDE'),
    pytest.param(Command.MOD,          7, 2, 1, id='MOD'),
    pytest.param(Command.NOT,          8, 2, 2, id='NOT'),
    pytest.param(Command.GREATER,      9, 3, 0, id='GREATER'),
    pytest.param(Command.POINTER,     10, 3, 1, id='POINTER'),
    pytest.param(Command.SWITCH,      11, 3, 2, id='SWITCH'),
    pytest.param(Command.DUPLICATE,   12, 4, 0, id='DUPLICATE'),
    pytest.param(Command.ROLL,        13, 4, 1, id='ROLL'),
    pytest.param(Command.IN_NUMBER,   14, 4, 2, id='IN_NUMBER'),
    pytest.param(Command.IN_CHAR,     15, 5, 0, id='IN_CHAR'),
    pytest.param(Command.OUT_NUMBER,  16, 5, 1, id='OUT_NUMBER'),
    pytest.param(Command.OUT_CHAR,    17, 5, 2, id='OUT_CHAR'),
    pytest.param(Command.FREE_ZONE,  100, 0, 0, id='FREE_ZONE'),
    pytest.param(Command.EDGE,       101, 0, 0, id='EDGE'),
])
def test_command_init(command, command_id, hue_step, lightness_step):
    assert command._command_id == command_id
    assert command._hue_step == hue_step
    assert command._lightness_step == lightness_step


@pytest.mark.parametrize('command, expect', [
    pytest.param(Command.NONE,       'NONE',       id='NONE'),
    pytest.param(Command.PUSH,       'PUSH',       id='PUSH'),
    pytest.param(Command.POP,        'POP',        id='POP'),
    pytest.param(Command.ADD,        'ADD',        id='ADD'),
    pytest.param(Command.SUBTRACT,   'SUBTRACT',   id='SUBTRACT'),
    pytest.param(Command.MULTIPLY,   'MULTIPLY',   id='MULTIPLY'),
    pytest.param(Command.DIVIDE,     'DIVIDE',     id='DIVIDE'),
    pytest.param(Command.MOD,        'MOD',        id='MOD'),
    pytest.param(Command.NOT,        'NOT',        id='NOT'),
    pytest.param(Command.GREATER,    'GREATER',    id='GREATER'),
    pytest.param(Command.POINTER,    'POINTER',    id='POINTER'),
    pytest.param(Command.SWITCH,     'SWITCH',     id='SWITCH'),
    pytest.param(Command.DUPLICATE,  'DUPLICATE',  id='DUPLICATE'),
    pytest.param(Command.ROLL,       'ROLL',       id='ROLL'),
    pytest.param(Command.IN_NUMBER,  'IN_NUMBER',  id='IN_NUMBER'),
    pytest.param(Command.IN_CHAR,    'IN_CHAR',    id='IN_CHAR'),
    pytest.param(Command.OUT_NUMBER, 'OUT_NUMBER', id='OUT_NUMBER'),
    pytest.param(Command.OUT_CHAR,   'OUT_CHAR',   id='OUT_CHAR'),
    pytest.param(Command.FREE_ZONE,  'FREE_ZONE',  id='FREE_ZONE'),
    pytest.param(Command.EDGE,       'EDGE',       id='EDGE'),
])
def test_command_str(command, expect):
    assert str(command) == expect


@pytest.mark.parametrize('command, hue_step, lightness_step', [
    pytest.param(Command.NONE,       0, 0, id='NONE'),
    pytest.param(Command.PUSH,       0, 1, id='PUSH'),
    pytest.param(Command.POP,        0, 2, id='POP'),
    pytest.param(Command.ADD,        1, 0, id='ADD'),
    pytest.param(Command.SUBTRACT,   1, 1, id='SUBTRACT'),
    pytest.param(Command.MULTIPLY,   1, 2, id='MULTIPLY'),
    pytest.param(Command.DIVIDE,     2, 0, id='DIVIDE'),
    pytest.param(Command.MOD,        2, 1, id='MOD'),
    pytest.param(Command.NOT,        2, 2, id='NOT'),
    pytest.param(Command.GREATER,    3, 0, id='GREATER'),
    pytest.param(Command.POINTER,    3, 1, id='POINTER'),
    pytest.param(Command.SWITCH,     3, 2, id='SWITCH'),
    pytest.param(Command.DUPLICATE,  4, 0, id='DUPLICATE'),
    pytest.param(Command.ROLL,       4, 1, id='ROLL'),
    pytest.param(Command.IN_NUMBER,  4, 2, id='IN_NUMBER'),
    pytest.param(Command.IN_CHAR,    5, 0, id='IN_CHAR'),
    pytest.param(Command.OUT_NUMBER, 5, 1, id='OUT_NUMBER'),
    pytest.param(Command.OUT_CHAR,   5, 2, id='OUT_CHAR'),
    pytest.param(Command.FREE_ZONE,  0, 0, id='FREE_ZONE'),
    pytest.param(Command.EDGE,       0, 0, id='EDGE'),
])
def test_command_properties(command, hue_step, lightness_step):
    assert command.hue_step == hue_step
    assert command.lightness_step == lightness_step


@pytest.mark.parametrize('hue_step, lightness_step, expect', [
    pytest.param(0, 0, Command.NONE,       id='NONE'),
    pytest.param(0, 1, Command.PUSH,       id='PUSH'),
    pytest.param(0, 2, Command.POP,        id='POP'),
    pytest.param(1, 0, Command.ADD,        id='ADD'),
    pytest.param(1, 1, Command.SUBTRACT,   id='SUBTRACT'),
    pytest.param(1, 2, Command.MULTIPLY,   id='MULTIPLY'),
    pytest.param(2, 0, Command.DIVIDE,     id='DIVIDE'),
    pytest.param(2, 1, Command.MOD,        id='MOD'),
    pytest.param(2, 2, Command.NOT,        id='NOT'),
    pytest.param(3, 0, Command.GREATER,    id='GREATER'),
    pytest.param(3, 1, Command.POINTER,    id='POINTER'),
    pytest.param(3, 2, Command.SWITCH,     id='SWITCH'),
    pytest.param(4, 0, Command.DUPLICATE,  id='DUPLICATE'),
    pytest.param(4, 1, Command.ROLL,       id='ROLL'),
    pytest.param(4, 2, Command.IN_NUMBER,  id='IN_NUMBER'),
    pytest.param(5, 0, Command.IN_CHAR,    id='IN_CHAR'),
    pytest.param(5, 1, Command.OUT_NUMBER, id='OUT_NUMBER'),
    pytest.param(5, 2, Command.OUT_CHAR,   id='OUT_CHAR'),
])
def test_command_get_command(hue_step, lightness_step, expect):
    actual = Command.get_command(hue_step, lightness_step)
    assert expect is actual


@pytest.mark.parametrize('hue_step, lightness_step', [
    pytest.param(6, 0, id='hue_step=6 lightness_step=0'),
    pytest.param(0, 3, id='hue_step=0 lightness_step=3'),
    pytest.param(6, 3, id='hue_step=6 lightness_step=3'),
])
def test_command_get_command_raise_value_error(hue_step, lightness_step):
    with pytest.raises(ValueError):
        _ = Command.get_command(hue_step, lightness_step)


@pytest.mark.parametrize('color, rgb, hue, lightness', [
    pytest.param(Color.BLACK,         0x000000, None, None, id='BLACK'),
    pytest.param(Color.WHITE,         0xFFFFFF, None, None, id='WHITE'),
    pytest.param(Color.LIGHT_RED,     0xFFC0C0,    0,    0, id='LIGHT_RED'),
    pytest.param(Color.LIGHT_YELLOW,  0xFFFFC0,    1,    0, id='LIGHT_YELLOW'),
    pytest.param(Color.LIGHT_GREEN,   0xC0FFC0,    2,    0, id='LIGHT_GREEN'),
    pytest.param(Color.LIGHT_CYAN,    0xC0FFFF,    3,    0, id='LIGHT_CYAN'),
    pytest.param(Color.LIGHT_BLUE,    0xC0C0FF,    4,    0, id='LIGHT_BLUE'),
    pytest.param(Color.LIGHT_MAGENTA, 0xFFC0FF,    5,    0, id='LIGHT_MAGENTA'),
    pytest.param(Color.RED,           0xFF0000,    0,    1, id='RED'),
    pytest.param(Color.YELLOW,        0xFFFF00,    1,    1, id='YELLOW'),
    pytest.param(Color.GREEN,         0x00FF00,    2,    1, id='GREEN'),
    pytest.param(Color.CYAN,          0x00FFFF,    3,    1, id='CYAN'),
    pytest.param(Color.BLUE,          0x0000FF,    4,    1, id='BLUE'),
    pytest.param(Color.MAGENTA,       0xFF00FF,    5,    1, id='MAGENTA'),
    pytest.param(Color.DARK_RED,      0xC00000,    0,    2, id='DARK_RED'),
    pytest.param(Color.DARK_YELLOW,   0xC0C000,    1,    2, id='DARK_YELLOW'),
    pytest.param(Color.DARK_GREEN,    0x00C000,    2,    2, id='DARK_GREEN'),
    pytest.param(Color.DARK_CYAN,     0x00C0C0,    3,    2, id='DARK_CYAN'),
    pytest.param(Color.DARK_BLUE,     0x0000C0,    4,    2, id='DARK_BLUE'),
    pytest.param(Color.DARK_MAGENTA,  0xC000C0,    5,    2, id='DARK_MAGENTA'),
])
def test_color_init(color, rgb, hue, lightness):
    assert color._rgb == rgb
    assert color._hue == hue
    assert color._lightness == lightness


@pytest.mark.parametrize('color, expect', [
    pytest.param(Color.BLACK,         'BLACK',         id='BLACK'),
    pytest.param(Color.WHITE,         'WHITE',         id='WHITE'),
    pytest.param(Color.LIGHT_RED,     'LIGHT_RED',     id='LIGHT_RED'),
    pytest.param(Color.LIGHT_YELLOW,  'LIGHT_YELLOW',  id='LIGHT_YELLOW'),
    pytest.param(Color.LIGHT_GREEN,   'LIGHT_GREEN',   id='LIGHT_GREEN'),
    pytest.param(Color.LIGHT_CYAN,    'LIGHT_CYAN',    id='LIGHT_CYAN'),
    pytest.param(Color.LIGHT_BLUE,    'LIGHT_BLUE',    id='LIGHT_BLUE'),
    pytest.param(Color.LIGHT_MAGENTA, 'LIGHT_MAGENTA', id='LIGHT_MAGENTA'),
    pytest.param(Color.RED,           'RED',           id='RED'),
    pytest.param(Color.YELLOW,        'YELLOW',        id='YELLOW'),
    pytest.param(Color.GREEN,         'GREEN',         id='GREEN'),
    pytest.param(Color.CYAN,          'CYAN',          id='CYAN'),
    pytest.param(Color.BLUE,          'BLUE',          id='BLUE'),
    pytest.param(Color.MAGENTA,       'MAGENTA',       id='MAGENTA'),
    pytest.param(Color.DARK_RED,      'DARK_RED',      id='DARK_RED'),
    pytest.param(Color.DARK_YELLOW,   'DARK_YELLOW',   id='DARK_YELLOW'),
    pytest.param(Color.DARK_GREEN,    'DARK_GREEN',    id='DARK_GREEN'),
    pytest.param(Color.DARK_CYAN,     'DARK_CYAN',     id='DARK_CYAN'),
    pytest.param(Color.DARK_BLUE,     'DARK_BLUE',     id='DARK_BLUE'),
    pytest.param(Color.DARK_MAGENTA,  'DARK_MAGENTA',  id='DARK_MAGENTA'),
])
def test_color_str(color, expect):
    assert str(color) == expect


@pytest.mark.parametrize('color, r, g, b, hue, lightness', [
    pytest.param(Color.BLACK,         0x00, 0x00, 0x00, None, None, id='BLACK'),
    pytest.param(Color.WHITE,         0xFF, 0xFF, 0xFF, None, None, id='WHITE'),
    pytest.param(Color.LIGHT_RED,     0xFF, 0xC0, 0xC0,    0,    0, id='LIGHT_RED'),
    pytest.param(Color.LIGHT_YELLOW,  0xFF, 0xFF, 0xC0,    1,    0, id='LIGHT_YELLOW'),
    pytest.param(Color.LIGHT_GREEN,   0xC0, 0xFF, 0xC0,    2,    0, id='LIGHT_GREEN'),
    pytest.param(Color.LIGHT_CYAN,    0xC0, 0xFF, 0xFF,    3,    0, id='LIGHT_CYAN'),
    pytest.param(Color.LIGHT_BLUE,    0xC0, 0xC0, 0xFF,    4,    0, id='LIGHT_BLUE'),
    pytest.param(Color.LIGHT_MAGENTA, 0xFF, 0xC0, 0xFF,    5,    0, id='LIGHT_MAGENTA'),
    pytest.param(Color.RED,           0xFF, 0x00, 0x00,    0,    1, id='RED'),
    pytest.param(Color.YELLOW,        0xFF, 0xFF, 0x00,    1,    1, id='YELLOW'),
    pytest.param(Color.GREEN,         0x00, 0xFF, 0x00,    2,    1, id='GREEN'),
    pytest.param(Color.CYAN,          0x00, 0xFF, 0xFF,    3,    1, id='CYAN'),
    pytest.param(Color.BLUE,          0x00, 0x00, 0xFF,    4,    1, id='BLUE'),
    pytest.param(Color.MAGENTA,       0xFF, 0x00, 0xFF,    5,    1, id='MAGENTA'),
    pytest.param(Color.DARK_RED,      0xC0, 0x00, 0x00,    0,    2, id='DARK_RED'),
    pytest.param(Color.DARK_YELLOW,   0xC0, 0xC0, 0x00,    1,    2, id='DARK_YELLOW'),
    pytest.param(Color.DARK_GREEN,    0x00, 0xC0, 0x00,    2,    2, id='DARK_GREEN'),
    pytest.param(Color.DARK_CYAN,     0x00, 0xC0, 0xC0,    3,    2, id='DARK_CYAN'),
    pytest.param(Color.DARK_BLUE,     0x00, 0x00, 0xC0,    4,    2, id='DARK_BLUE'),
    pytest.param(Color.DARK_MAGENTA,  0xC0, 0x00, 0xC0,    5,    2, id='DARK_MAGENTA'),
])
def test_color_properties(color, r, g, b, hue, lightness):
    assert color.r == r
    assert color.g == g
    assert color.b == b
    assert color.a == 0xff
    assert color.hue == hue
    assert color.lightness == lightness


@pytest.mark.parametrize('hue, lightness, expect', [
    pytest.param(0, 0, Color.LIGHT_RED,     id='LIGHT_RED'),
    pytest.param(1, 0, Color.LIGHT_YELLOW,  id='LIGHT_YELLOW'),
    pytest.param(2, 0, Color.LIGHT_GREEN,   id='LIGHT_GREEN'),
    pytest.param(3, 0, Color.LIGHT_CYAN,    id='LIGHT_CYAN'),
    pytest.param(4, 0, Color.LIGHT_BLUE,    id='LIGHT_BLUE'),
    pytest.param(5, 0, Color.LIGHT_MAGENTA, id='LIGHT_MAGENTA'),
    pytest.param(0, 1, Color.RED,           id='RED'),
    pytest.param(1, 1, Color.YELLOW,        id='YELLOW'),
    pytest.param(2, 1, Color.GREEN,         id='GREEN'),
    pytest.param(3, 1, Color.CYAN,          id='CYAN'),
    pytest.param(4, 1, Color.BLUE,          id='BLUE'),
    pytest.param(5, 1, Color.MAGENTA,       id='MAGENTA'),
    pytest.param(0, 2, Color.DARK_RED,      id='DARK_RED'),
    pytest.param(1, 2, Color.DARK_YELLOW,   id='DARK_YELLOW'),
    pytest.param(2, 2, Color.DARK_GREEN,    id='DARK_GREEN'),
    pytest.param(3, 2, Color.DARK_CYAN,     id='DARK_CYAN'),
    pytest.param(4, 2, Color.DARK_BLUE,     id='DARK_BLUE'),
    pytest.param(5, 2, Color.DARK_MAGENTA,  id='DARK_MAGENTA'),
])
def test_color_get_color(hue, lightness, expect):
    actual = Color.get_color(hue, lightness)
    assert expect is actual


@pytest.mark.parametrize('hue, lightness', [
    pytest.param(6, 0, id='hue=6 lightness=0'),
    pytest.param(0, 3, id='hue=0 lightness=3'),
    pytest.param(6, 3, id='hue=6 lightness=3'),
])
def test_color_get_color_raise_value_error(hue, lightness):
    with pytest.raises(ValueError):
        _ = Color.get_color(hue, lightness)


@pytest.mark.parametrize('name, expect', [
    pytest.param('LIGHT_RED',     Color.LIGHT_RED,     id='LIGHT_RED'),
    pytest.param('LIGHT_YELLOW',  Color.LIGHT_YELLOW,  id='LIGHT_YELLOW'),
    pytest.param('LIGHT_GREEN',   Color.LIGHT_GREEN,   id='LIGHT_GREEN'),
    pytest.param('LIGHT_CYAN',    Color.LIGHT_CYAN,    id='LIGHT_CYAN'),
    pytest.param('LIGHT_BLUE',    Color.LIGHT_BLUE,    id='LIGHT_BLUE'),
    pytest.param('LIGHT_MAGENTA', Color.LIGHT_MAGENTA, id='LIGHT_MAGENTA'),
    pytest.param('RED',           Color.RED,           id='RED'),
    pytest.param('YELLOW',        Color.YELLOW,        id='YELLOW'),
    pytest.param('GREEN',         Color.GREEN,         id='GREEN'),
    pytest.param('CYAN',          Color.CYAN,          id='CYAN'),
    pytest.param('BLUE',          Color.BLUE,          id='BLUE'),
    pytest.param('MAGENTA',       Color.MAGENTA,       id='MAGENTA'),
    pytest.param('DARK_RED',      Color.DARK_RED,      id='DARK_RED'),
    pytest.param('DARK_YELLOW',   Color.DARK_YELLOW,   id='DARK_YELLOW'),
    pytest.param('DARK_GREEN',    Color.DARK_GREEN,    id='DARK_GREEN'),
    pytest.param('DARK_CYAN',     Color.DARK_CYAN,     id='DARK_CYAN'),
    pytest.param('DARK_BLUE',     Color.DARK_BLUE,     id='DARK_BLUE'),
    pytest.param('DARK_MAGENTA',  Color.DARK_MAGENTA,  id='DARK_MAGENTA'),
])
def test_color_name_of(name, expect):
    actual = Color.name_of(name)
    assert expect is actual


@pytest.mark.parametrize('color', [
    pytest.param(Color.BLACK, id='NONE'),
])
def test_codel_init(color):
    codel = Codel(color)

    assert codel._color is color


@pytest.mark.parametrize('color, expect', [
    pytest.param(Color.BLACK, '(BLACK)', id='NONE'),
])
def test_codel_str(color, expect):
    codel = Codel(color)

    assert str(codel) == expect


@pytest.mark.parametrize('color', [
    pytest.param(Color.BLACK, id='NONE'),
])
def test_codel_properties(color):
    codel = Codel(color)

    assert codel.color is color


@pytest.mark.parametrize('command, color, expect', [
    pytest.param(Command.NONE,       Color.LIGHT_RED, Color.LIGHT_RED,     id='NONE: LIGHT_RED'),
    pytest.param(Command.PUSH,       Color.LIGHT_RED, Color.RED,           id='PUSH: LIGHT_RED'),
    pytest.param(Command.POP,        Color.LIGHT_RED, Color.DARK_RED,      id='POP: LIGHT_RED'),
    pytest.param(Command.ADD,        Color.LIGHT_RED, Color.LIGHT_YELLOW,  id='ADD: LIGHT_RED'),
    pytest.param(Command.SUBTRACT,   Color.LIGHT_RED, Color.YELLOW,        id='SUBTRACT: LIGHT_RED'),
    pytest.param(Command.MULTIPLY,   Color.LIGHT_RED, Color.DARK_YELLOW,   id='MULTIPLY: LIGHT_RED'),
    pytest.param(Command.DIVIDE,     Color.LIGHT_RED, Color.LIGHT_GREEN,   id='DIVIDE: LIGHT_RED'),
    pytest.param(Command.MOD,        Color.LIGHT_RED, Color.GREEN,         id='MOD: LIGHT_RED'),
    pytest.param(Command.NOT,        Color.LIGHT_RED, Color.DARK_GREEN,    id='NOT: LIGHT_RED'),
    pytest.param(Command.GREATER,    Color.LIGHT_RED, Color.LIGHT_CYAN,    id='GREATER: LIGHT_RED'),
    pytest.param(Command.POINTER,    Color.LIGHT_RED, Color.CYAN,          id='POINTER: LIGHT_RED'),
    pytest.param(Command.SWITCH,     Color.LIGHT_RED, Color.DARK_CYAN,     id='SWITCH: LIGHT_RED'),
    pytest.param(Command.DUPLICATE,  Color.LIGHT_RED, Color.LIGHT_BLUE,    id='DUPLICATE: LIGHT_RED'),
    pytest.param(Command.ROLL,       Color.LIGHT_RED, Color.BLUE,          id='ROLL: LIGHT_RED'),
    pytest.param(Command.IN_NUMBER,  Color.LIGHT_RED, Color.DARK_BLUE,     id='IN_NUMBER: LIGHT_RED'),
    pytest.param(Command.IN_CHAR,    Color.LIGHT_RED, Color.LIGHT_MAGENTA, id='IN_CHAR: LIGHT_RED'),
    pytest.param(Command.OUT_NUMBER, Color.LIGHT_RED, Color.MAGENTA,       id='OUT_NUMBER: LIGHT_RED'),
    pytest.param(Command.OUT_CHAR,   Color.LIGHT_RED, Color.DARK_MAGENTA,  id='OUT_CHAR: LIGHT_RED'),

    pytest.param(Command.NONE,       Color.DARK_MAGENTA, Color.DARK_MAGENTA,  id='NONE: DARK_MAGENTA'),
    pytest.param(Command.PUSH,       Color.DARK_MAGENTA, Color.LIGHT_MAGENTA, id='PUSH: DARK_MAGENTA'),
    pytest.param(Command.POP,        Color.DARK_MAGENTA, Color.MAGENTA,       id='POP: DARK_MAGENTA'),
    pytest.param(Command.ADD,        Color.DARK_MAGENTA, Color.DARK_RED,      id='ADD: DARK_MAGENTA'),
    pytest.param(Command.SUBTRACT,   Color.DARK_MAGENTA, Color.LIGHT_RED,     id='SUBTRACT: DARK_MAGENTA'),
    pytest.param(Command.MULTIPLY,   Color.DARK_MAGENTA, Color.RED,           id='MULTIPLY: DARK_MAGENTA'),
    pytest.param(Command.DIVIDE,     Color.DARK_MAGENTA, Color.DARK_YELLOW,   id='DIVIDE: DARK_MAGENTA'),
    pytest.param(Command.MOD,        Color.DARK_MAGENTA, Color.LIGHT_YELLOW,  id='MOD: DARK_MAGENTA'),
    pytest.param(Command.NOT,        Color.DARK_MAGENTA, Color.YELLOW,        id='NOT: DARK_MAGENTA'),
    pytest.param(Command.GREATER,    Color.DARK_MAGENTA, Color.DARK_GREEN,    id='GREATER: DARK_MAGENTA'),
    pytest.param(Command.POINTER,    Color.DARK_MAGENTA, Color.LIGHT_GREEN,   id='POINTER: DARK_MAGENTA'),
    pytest.param(Command.SWITCH,     Color.DARK_MAGENTA, Color.GREEN,         id='SWITCH: DARK_MAGENTA'),
    pytest.param(Command.DUPLICATE,  Color.DARK_MAGENTA, Color.DARK_CYAN,     id='DUPLICATE: DARK_MAGENTA'),
    pytest.param(Command.ROLL,       Color.DARK_MAGENTA, Color.LIGHT_CYAN,    id='ROLL: DARK_MAGENTA'),
    pytest.param(Command.IN_NUMBER,  Color.DARK_MAGENTA, Color.CYAN,          id='IN_NUMBER: DARK_MAGENTA'),
    pytest.param(Command.IN_CHAR,    Color.DARK_MAGENTA, Color.DARK_BLUE,     id='IN_CHAR: DARK_MAGENTA'),
    pytest.param(Command.OUT_NUMBER, Color.DARK_MAGENTA, Color.LIGHT_BLUE,    id='OUT_NUMBER: DARK_MAGENTA'),
    pytest.param(Command.OUT_CHAR,   Color.DARK_MAGENTA, Color.BLUE,          id='OUT_CHAR: DARK_MAGENTA'),
])
def test_get_color_from_command(command, color, expect):
    actual = get_color_from_command(command, color)
    assert actual is expect


@pytest.mark.parametrize('current_color, next_color, expect', [
    pytest.param(Color.LIGHT_RED, Color.LIGHT_RED,     Command.NONE,       id='NONE: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.RED,           Command.PUSH,       id='PUSH: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_RED,      Command.POP,        id='POP: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.LIGHT_YELLOW,  Command.ADD,        id='ADD: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.YELLOW,        Command.SUBTRACT,   id='SUBTRACT: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_YELLOW,   Command.MULTIPLY,   id='MULTIPLY: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.LIGHT_GREEN,   Command.DIVIDE,     id='DIVIDE: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.GREEN,         Command.MOD,        id='MOD: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_GREEN,    Command.NOT,        id='NOT: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.LIGHT_CYAN,    Command.GREATER,    id='GREATER: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.CYAN,          Command.POINTER,    id='POINTER: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_CYAN,     Command.SWITCH,     id='SWITCH: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.LIGHT_BLUE,    Command.DUPLICATE,  id='DUPLICATE: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.BLUE,          Command.ROLL,       id='ROLL: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_BLUE,     Command.IN_NUMBER,  id='IN_NUMBER: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.LIGHT_MAGENTA, Command.IN_CHAR,    id='IN_CHAR: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.MAGENTA,       Command.OUT_NUMBER, id='OUT_NUMBER: LIGHT_RED'),
    pytest.param(Color.LIGHT_RED, Color.DARK_MAGENTA,  Command.OUT_CHAR,   id='OUT_CHAR: LIGHT_RED'),

    pytest.param(Color.DARK_MAGENTA, Color.DARK_MAGENTA,  Command.NONE,       id='NONE: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_MAGENTA, Command.PUSH,       id='PUSH: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.MAGENTA,       Command.POP,        id='POP: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.DARK_RED,      Command.ADD,        id='ADD: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_RED,     Command.SUBTRACT,   id='SUBTRACT: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.RED,           Command.MULTIPLY,   id='MULTIPLY: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.DARK_YELLOW,   Command.DIVIDE,     id='DIVIDE: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_YELLOW,  Command.MOD,        id='MOD: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.YELLOW,        Command.NOT,        id='NOT: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.DARK_GREEN,    Command.GREATER,    id='GREATER: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_GREEN,   Command.POINTER,    id='POINTER: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.GREEN,         Command.SWITCH,     id='SWITCH: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.DARK_CYAN,     Command.DUPLICATE,  id='DUPLICATE: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_CYAN,    Command.ROLL,       id='ROLL: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.CYAN,          Command.IN_NUMBER,  id='IN_NUMBER: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.DARK_BLUE,     Command.IN_CHAR,    id='IN_CHAR: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.LIGHT_BLUE,    Command.OUT_NUMBER, id='OUT_NUMBER: DARK_MAGENTA'),
    pytest.param(Color.DARK_MAGENTA, Color.BLUE,          Command.OUT_CHAR,   id='OUT_CHAR: DARK_MAGENTA'),
])
def test_get_command_from_color(current_color, next_color, expect):
    actual = get_command_from_color(current_color, next_color)
    assert actual is expect
