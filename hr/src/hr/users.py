import pwd
import subprocess
import sys
from subprocess import CalledProcessError
import spwd

def create(user_info):
    """
    Accepts a dictionary containing user_info and creates the user
    if no user exists by that name
    """
    system_users = [user.pw_name for user in pwd.getpwall() if user.pw_uid >= 1000]
    username = user_info.get('name')
    if username not in system_users:
        groups = ','.join(user_info.get('groups'))
        try:
            proc = subprocess.run(
                    ['useradd', '-G', groups, '-p', user_info.get('password'), username],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True) #raises CalledProcessError for non-exit status
        except CalledProcessError as err:
            print(f"Error: {err}")
            sys.exit(1)


