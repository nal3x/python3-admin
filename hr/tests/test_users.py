import pytest
from hr import users
import subprocess
from subprocess import CalledProcessError

kevin = {'name':'kevin', 'groups': ['wheel', 'fake'], 'password': 'abracatabra'}

def test_user_creation_called_with_correct_arguments(mocker):
    """
    useradd should be called with correct arguments
    """
    mocker.patch('subprocess.run')
    users.create(kevin)
    subprocess.run.assert_called_with(
            ['useradd', '-G', 'wheel,fake', '-p', 'abracatabra', 'kevin'],
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
            ['usermod', '-G', 'wheel,fake', '-p', 'abracatabra', 'kevin'],
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
