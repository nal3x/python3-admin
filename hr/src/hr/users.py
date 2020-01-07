import pwd
import subprocess
import sys
from subprocess import CalledProcessError
import spwd
import pwd

def sync_system(input_users):
    """
    Receive a list of user dictionaries and ensure that the system’s users match.
    """
    for user in input_users:
        if user.get('name') not in system_usernames():
            create(user)
        else:
            modify(user)
    input_usernames = [user.get('name') for user in input_users]
    for username in system_usernames():
        if username not in input_usernames:
            delete(username)

def system_usernames():
    return [user.pw_name for user in pwd.getpwall() if user.pw_uid >= 1000]

def create(user_info):
    """
    Accepts a dictionary containing user_info and creates the user
    if no user exists by that name
    """
    system_users = system_usernames()
    username = user_info.get('name')
    if username not in system_users:
        groups = ','.join(user_info.get('groups'))
        try:
            print(f"Adding user {username}")
            proc = subprocess.run(
                    ['useradd', '-G', groups, '-p', user_info.get('password'), username],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True) #raises CalledProcessError for non-exit status
        except CalledProcessError as err:
            print(f"Error: {err}")
            sys.exit(1)
        else:
            print(f"Added user {username}")

def modify(user_info):
    """
    Updates a user based on the provided user dictionary
    """
    try:
        username = user_info.get('name')
        print(f"Updating user {username}")
        proc = subprocess.run(
                ['usermod',
                '-G', ','.join(user_info.get('groups')),
                '-p', user_info.get('password'),
                username],
                check = True
                )
    except CalledProcessError as err:
        print(f"Error: {err}")
        sys.exit(1)
    else:
        print(f"Updated user {username}")

def delete(username):
    """
    Removes a user with a given username
    """
    try:
        print(f"Deleting user {username}")
        proc = subprocess.run(
                ['userdel', '-r', username],
                check=True)
    except CalledProcessError as err:
        print(f"Error: {err}")
        sys.exit(1)
    else:
        print(f"Deleted user {username}")

