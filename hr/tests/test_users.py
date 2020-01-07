import pytest
from hr import users
import subprocess
from subprocess import CalledProcessError
from unittest.mock import call

kevin = {'name':'kevin', 'groups': ['wheel', 'fake'], 'password': '12345'}
sorcerer ={'name':'sorcerer', 'groups': [], 'password': 'abracatabra'}

def test_sync_system_correctly_calls(mocker):
    """
    users.sync_system should add kevin, modify sorcerer, delete max
    """
    mocker.patch.object(users, 'system_usernames', return_value = ['max'])
    mocker.patch('subprocess.run')
    input_users = [kevin, sorcerer]
    users.sync_system(input_users)

    expected_calls = [
            call(['useradd', '-G', 'wheel,fake', '-p', '12345', 'kevin'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True),
            call(['usermod', '-G', '', '-p', 'abracatabra', 'sorcerer'], check=True),
            call(['userdel', '-r', 'max'],check=True)]
    subprocess.run.mock_calls == expected_calls

def test_user_creation_called_with_correct_arguments(mocker):
    """
    useradd should be called with correct arguments
    """
    mocker.patch('subprocess.run')
    users.create(kevin)
    subprocess.run.assert_any_call(
            ['useradd', '-G', 'wheel,fake', '-p', '12345', 'kevin'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True)

def test_user_creation_handles_thrown_exception():
    """
    users.create should exit normally when non existent group is given
    as exception is handle. Test passes only when there is no kevin as
    user!!!
    """
    with pytest.raises(SystemExit) as e:
        users.create(kevin)
        assert e.type is CalledProcessError

def test_user_modify_called_with_correct_arguments(mocker):
        """
        useradd should be called with correct arguments
        """
        mocker.patch('subprocess.run')
        users.modify(kevin)
        subprocess.run.assert_called_with(
            ['usermod', '-G', 'wheel,fake', '-p', '12345', 'kevin'],
            check=True)

def test_user_delete_calls_userdel_correctly(mocker):
    """
    users.delete should call userdel with correct arguments
    """
    mocker.patch('subprocess.run')
    users.delete("kidA")
    subprocess.run.assert_called_with(
                ['userdel', '-r', "kidA"],
                check=True)

def test_user_delete_handles_error(mocker):
    """
    users.delete should handle exception when user does not exist
    """
    with pytest.raises(SystemExit) as e:
        users.delete("kidA")
        assert e.type is CalledProcessError
