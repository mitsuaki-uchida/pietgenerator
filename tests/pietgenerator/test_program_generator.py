
from io import BytesIO

import pytest
from PIL import Image

from pietgenerator.piet_common import Codel
from pietgenerator.piet_common import Color
from pietgenerator.piet_common import Command
from pietgenerator.program_generator import GenerateProgramError
from pietgenerator.program_generator import ProgramGenerator
from pietgenerator.command_generator.command_generator import GenerateCommandError
from pietgenerator.command_layouter.command_layouter import LayoutCommandError


def test_generate_program_error_str():
    generate_program_error = GenerateProgramError()

    assert str(generate_program_error) == "GenerateProgramError: generate Piet program failed."


def test_generate(mocker):
    message = "Hello Piet World!"
    commands = [Command.NONE, Command.PUSH, Command.POP]
    start_color = Color.RED
    abort_program_color = Color.MAGENTA
    codel_size = 20
    grid = [[Command.NONE, Command.NONE], [Command.NONE, Command.NONE]]
    image = b"\x00\x01\x02"

    command_generator_mock = mocker.MagicMock()
    command_generator_generate_mock = mocker.patch.object(command_generator_mock, "generate", mocker.MagicMock(return_value=commands))

    command_layouter_mock = mocker.MagicMock()
    command_layouter_do_layout_mock = mocker.patch.object(command_layouter_mock, "do_layout", mocker.MagicMock(return_value=grid))

    gen = ProgramGenerator(command_generator_mock, command_layouter_mock)
    translate_mock = mocker.patch.object(gen, "_translate", mocker.MagicMock(return_value=image))

    actual = gen.generate(message, start_color=start_color, abort_program_color=abort_program_color, codel_size=codel_size)

    command_generator_generate_mock.assert_called_once_with(message)
    command_layouter_do_layout_mock.assert_called_once_with(commands, start_color, abort_program_color)
    translate_mock.assert_called_once_with(grid, codel_size)
    assert actual == image


def test_generate_call_default_values(mocker):
    message = "Hello Piet World!"
    commands = [Command.NONE, Command.PUSH, Command.POP]
    grid = [[Command.NONE, Command.NONE], [Command.NONE, Command.NONE]]
    image = b"\x00\x01\x02"

    command_generator_mock = mocker.MagicMock()
    command_generator_generate_mock = mocker.patch.object(command_generator_mock, "generate", mocker.MagicMock(return_value=commands))

    command_layouter_mock = mocker.MagicMock()
    command_layouter_do_layout_mock = mocker.patch.object(command_layouter_mock, "do_layout", mocker.MagicMock(return_value=grid))

    gen = ProgramGenerator(command_generator_mock, command_layouter_mock)
    translate_mock = mocker.patch.object(gen, "_translate", mocker.MagicMock(return_value=image))

    actual = gen.generate(message)

    command_generator_generate_mock.assert_called_once_with(message)
    command_layouter_do_layout_mock.assert_called_once_with(commands, Color.LIGHT_RED, Color.LIGHT_GREEN)
    translate_mock.assert_called_once_with(grid, 10)
    assert actual == image


@pytest.mark.parametrize('side_effect_commnad_generator, side_effect_commnad_layouter', [
    pytest.param(GenerateCommandError, [], id='command_generator: GenerateCommandError'),
    pytest.param(Exception, [], id='command_generator: Exception'),
    pytest.param([], LayoutCommandError, id='command_layouter: LayoutCommandError'),
    pytest.param([], Exception, id='command_layouter: Exception'),
    pytest.param(GenerateCommandError, LayoutCommandError, id='both'),
])
def test_generate_raise_exception(side_effect_commnad_generator, side_effect_commnad_layouter, mocker):
    command_generator_mock = mocker.MagicMock()
    mocker.patch.object(command_generator_mock, "generate", mocker.MagicMock(side_effect=side_effect_commnad_generator))

    command_layouter_mock = mocker.MagicMock()
    mocker.patch.object(command_layouter_mock, "do_layout", mocker.MagicMock(side_effect=side_effect_commnad_layouter))

    gen = ProgramGenerator(command_generator_mock, command_layouter_mock)
    mocker.patch.object(gen, "_translate", mocker.MagicMock())

    with pytest.raises(GenerateProgramError):
        _ = gen.generate("")


@pytest.mark.parametrize('grid, codel_size', [
    pytest.param([
            [Codel(Color.LIGHT_RED),     Codel(Color.RED),     Codel(Color.DARK_RED)],
            [Codel(Color.LIGHT_YELLOW),  Codel(Color.YELLOW),  Codel(Color.DARK_YELLOW)],
            [Codel(Color.LIGHT_GREEN),   Codel(Color.GREEN),   Codel(Color.DARK_GREEN)],
            [Codel(Color.LIGHT_CYAN),    Codel(Color.CYAN),    Codel(Color.DARK_CYAN)],
            [Codel(Color.LIGHT_BLUE),    Codel(Color.BLUE),    Codel(Color.DARK_BLUE)],
            [Codel(Color.LIGHT_MAGENTA), Codel(Color.MAGENTA), Codel(Color.DARK_MAGENTA)],
            [Codel(Color.BLACK),         Codel(Color.WHITE),   Codel(Color.BLACK)],
        ], 1, id='codel_size=1'),
    pytest.param([
            [Codel(Color.LIGHT_RED),     Codel(Color.RED),     Codel(Color.DARK_RED)],
            [Codel(Color.LIGHT_YELLOW),  Codel(Color.YELLOW),  Codel(Color.DARK_YELLOW)],
            [Codel(Color.LIGHT_GREEN),   Codel(Color.GREEN),   Codel(Color.DARK_GREEN)],
            [Codel(Color.LIGHT_CYAN),    Codel(Color.CYAN),    Codel(Color.DARK_CYAN)],
            [Codel(Color.LIGHT_BLUE),    Codel(Color.BLUE),    Codel(Color.DARK_BLUE)],
            [Codel(Color.LIGHT_MAGENTA), Codel(Color.MAGENTA), Codel(Color.DARK_MAGENTA)],
            [Codel(Color.BLACK),         Codel(Color.WHITE),   Codel(Color.BLACK)],
        ], 10, id='codel_size=10'),
    pytest.param([
            [Codel(Color.LIGHT_RED),     Codel(Color.RED),     Codel(Color.DARK_RED)],
            [Codel(Color.LIGHT_YELLOW),  Codel(Color.YELLOW),  Codel(Color.DARK_YELLOW)],
            [Codel(Color.LIGHT_GREEN),   Codel(Color.GREEN),   Codel(Color.DARK_GREEN)],
            [Codel(Color.LIGHT_CYAN),    Codel(Color.CYAN),    Codel(Color.DARK_CYAN)],
            [Codel(Color.LIGHT_BLUE),    Codel(Color.BLUE),    Codel(Color.DARK_BLUE)],
            [Codel(Color.LIGHT_MAGENTA), Codel(Color.MAGENTA), Codel(Color.DARK_MAGENTA)],
            [Codel(Color.BLACK),         Codel(Color.WHITE),   Codel(Color.BLACK)],
        ], 20, id='codel_size=20'),
])
def test_piet_generator__translate(grid, codel_size):
    w = len(grid[0])
    h = len(grid)
    gen = ProgramGenerator(None, None)
    image = Image.open(BytesIO(gen._translate(grid, codel_size)))

    assert image.mode == "RGBA"
    assert image.width == w * codel_size
    assert image.height == h * codel_size

    for y in range(h):
        for x in range(w):
            for j in range(codel_size):
                for i in range(codel_size):
                    r, g, b, a = image.getpixel(((x * codel_size) + i, (y * codel_size) + j))
                    assert r == grid[y][x].color.r
                    assert g == grid[y][x].color.g
                    assert b == grid[y][x].color.b
                    assert a == grid[y][x].color.a
