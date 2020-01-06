import tempfile
import pytest
import json
from hr import inventory
import spwd

users_data = [{"name": "kevin", "groups": ["wheel", "dev"], "password": "$4H4/"},
              {"name": "lisa", "groups": ["wheel"], "password": "$j2ajcQbZ4H4/"},
              {"name": "jim","groups": [],"password": "$6$HjcQbZ4H4/"}]
invalid_data = '{["key1", "key2"]:"value"}'
malformed_data = [{"key": "value"}, 1]

user_mock_data = ['userA', 'userB', 'userC']
group_mock_data = [('root', 'x', 0, []),
                   ('groupAB', 'x', 1000, ['userA', 'userB']),
                   ('groupAC', 'x', 1001, ['userA', 'userC'])]
password_mock_data = ('nam', '1234', 'lstchg', 'min_d',' max_d',
                      'warn', 'inact', 'expire', 'flag')

desired_json_dump = '[{"name": "userA", "groups": ["groupAB", "groupAC"], "password": "1234"},' \
                    ' {"name": "userB", "groups": ["groupAB"], "password": "1234"},' \
                    ' {"name": "userC", "groups": ["groupAC"], "password": "1234"}]'

@pytest.fixture
def dumpfile():
    return tempfile.NamedTemporaryFile('r+', delete=False)

# A fixture that accepts arguments for testing inventory.parse
@pytest.fixture
def json_writer():
    def _writer(content):
        with tempfile.NamedTemporaryFile('r+', delete=False) as f:
            if isinstance(content, str): #we don't use dump for invalid data as json.dump may encode to proper json
                f.write(content)
            else:
                json.dump(content, f)
        return f
    return _writer

def test_dump_correctly_exports_users_to_file(dumpfile, mocker):
    """
    Asserts that inventory.dump correctly dumps the given user data and
    produces the expected json file
    """

    mocker.patch('grp.getgrall', return_value = group_mock_data)
    mocker.patch('spwd.getspnam', return_value = password_mock_data)
    inventory.dump(dumpfile.name, user_mock_data)

    #TODO: use the call helper object to assert calls with a list
    spwd.getspnam.assert_any_call('userA')
    spwd.getspnam.assert_any_call('userB')
    spwd.getspnam.assert_any_call('userC')

    with open(dumpfile.name,'r') as f:
        assert f.read() == desired_json_dump

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
