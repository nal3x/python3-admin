import pytest

from hr import cli

path = 'path/to/inventory.json'

@pytest.fixture
def parser():
        return cli.create_parser()

def test_no_arguments_to_parser(parser):
    """
    The parser will exit if no arguments are passed to it
    """
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_argument_given_to_parser(parser):
    """
    path is correctly parsed by the parser
    """
    args = parser.parse_args([path])
    assert args.path == path

def test_export_value_if_flag_is_given(parser):
    """
    The export value is set to True if the --export flag is given.
    """
    args = parser.parse_args([path, '--export'])
    assert args.export == True

def test_export_value_if_no_flag_is_given(parser):
    """
    The export value is set to False if the --export flag is not given.
    """
    args = parser.parse_args([path])
    assert args.export == False


