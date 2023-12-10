
import pytest

from pietgenerator.command_generator.command_generator import ICommandGenerator
from pietgenerator.command_generator.command_generator import GenerateCommandError


def test_generate_command_error_str():
    generate_command_error = GenerateCommandError()

    assert str(generate_command_error) == "GenerateCommandError: generate command failed."


class TestCommandGenerator(ICommandGenerator):
    def __init__(self, debug):
        super().__init__(debug)
    
    def _generate_impl(self, message):
        return super()._generate_impl(message)


def test_init():
    gen = TestCommandGenerator(True)
    assert gen._debug is True

    gen = TestCommandGenerator(False)
    assert gen._debug is False


def test__generate_impl_raise_not_implemented_error(mocker):
    gen = TestCommandGenerator(True)

    with pytest.raises(NotImplementedError):
        _ = gen._generate_impl("")