import tempfile
import pytest
import json
from hr import inventory


users_data = [{"name": "kevin", "groups": ["wheel", "dev"], "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"}, {"name": "lisa", "groups": ["wheel"], "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"}, {"name": "jim","groups": [],"password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"}]

invalid_data = '{["key1", "key2"]:"value"}'

malformed_data = [{"key": "value"}, 1]

# this is the way to write a fixture that accepts arguments!
@pytest.fixture
def json_writer():
    def _writer(content):
        with tempfile.NamedTemporaryFile('r+', delete=False) as f:
            if isinstance(content, str):
                f.write(content)
            else:
                json.dump(content, f)
        return f
    return _writer


def test_parsing_nonexistent_file():
    """
    inventory.parse exits normally when it is given a non existing path
    """
    with pytest.raises(FileNotFoundError):
        inventory.parse('fake_filename')

def test_parsing_invalid_json(json_writer):
    """
    inventory.parse raises ValueError when improper json is loaded
    """
    with pytest.raises(ValueError):
        invalid_file = json_writer(invalid_data)
        inventory.parse(invalid_file.name)

def test_parsing_malformed_json(json_writer):
    """
    inventory.parse raises an error and exits when malformed json is given!
    """
    with pytest.raises(SystemExit):
        malformed_file = json_writer(malformed_data)
        inventory.parse(malformed_file.name)

def test_parsing_works_correctly(json_writer):
    """
    When vaild json data is given, parser correctly returns list of user dictionariesi
    """
    valid_json_file = json_writer(users_data)
    users = inventory.parse(valid_json_file.name)
    assert users == users_data
