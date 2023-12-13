
import random

import pytest

from pietgenerator.piet_common import Command
from pietgenerator.command_generator.command_generator import GenerateCommandError
from pietgenerator.command_generator.factorize_generator import FactorizeCommandGenerator


def test_init():
    gen = FactorizeCommandGenerator()
    assert gen._debug is True

    gen = FactorizeCommandGenerator(debug=True)
    assert gen._debug is True

    gen = FactorizeCommandGenerator(debug=False)
    assert gen._debug is False


def _inspect_character_commands(commands, expect):
    stack = []

    for command in commands:
        if command is Command.PUSH:
            stack.append(1)
        elif command is Command.ADD:
            value1 = stack.pop(-1)
            value2 = stack.pop(-1)
            stack.append(value2 + value1)
        elif command is Command.SUBTRACT:
            value1 = stack.pop(-1)
            value2 = stack.pop(-1)
            stack.append(value2 - value1)
        elif command is Command.MULTIPLY:
            value1 = stack.pop(-1)
            value2 = stack.pop(-1)
            stack.append(value2 * value1)
        elif command is Command.DIVIDE:
            value1 = stack.pop(-1)
            value2 = stack.pop(-1)
            stack.append(value2 // value1)
        elif command is Command.MOD:
            value1 = stack.pop(-1)
            value2 = stack.pop(-1)
            stack.append(value2 % value1)
        elif command is Command.DUPLICATE:
            stack.append(stack[-1])
        else:
            assert False

    assert len(stack) == len(expect)
    assert expect == "".join([chr(ascii) for ascii in stack[::-1]])


@pytest.mark.parametrize('ch', [
    # ASCIIコード 1 ～ 255 をテスト
    pytest.param(ch, id=f"ch=0x{ch:02X}") for ch in range(1, 256)
])
def test__character_to_commands(ch):
    gen = FactorizeCommandGenerator()
    commands = gen._character_to_commands(chr(ch))

    _inspect_character_commands(commands, chr(ch))


@pytest.mark.parametrize('ch', [
    pytest.param(0x00, id=f"ch=0x00"),
])
def test__character_to_commands_raise_value_error(ch):
    gen = FactorizeCommandGenerator()

    with pytest.raises(ValueError):
        _ = gen._character_to_commands(chr(ch))


@pytest.mark.parametrize('message', [
    pytest.param(' ', id='message=" "'),
    pytest.param('A', id='message="A"'),
    pytest.param('Hello World!', id='message="Hello World!"')
])
def test_generate(message):
    gen = FactorizeCommandGenerator()
    commands = gen.generate(message)

    none_command = commands[:1]
    message_commands = commands[1:len(commands) - len(message)]
    output_commands = commands[len(commands) - len(message):]

    assert none_command == [Command.NONE]
    assert output_commands == [Command.OUT_CHAR] * len(message)

    _inspect_character_commands(message_commands, message)


def test_generate_too_long_message():
    message = "".join([chr(random.randrange(1, 256)) for _ in range(10000)])
    gen = FactorizeCommandGenerator()
    commands = gen.generate(message)

    none_command = commands[:1]
    message_commands = commands[1:len(commands) - len(message)]
    output_commands = commands[len(commands) - len(message):]

    assert none_command == [Command.NONE]
    assert output_commands == [Command.OUT_CHAR] * len(message)

    _inspect_character_commands(message_commands, message)


def test_generate_raises_generate_command_error(mocker):
    gen = FactorizeCommandGenerator()
    mocker.patch.object(gen, "_generate_impl", mocker.MagicMock(side_effect=GenerateCommandError))

    with pytest.raises(GenerateCommandError):
        _ = gen.generate("")
