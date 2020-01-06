import json, sys, pwd, spwd, grp

def parse(filename):
    with open(filename, 'r') as f:
        users = json.load(f)
    content_check(users)
    return users

def default_users():
    return [user.pw_name for user in pwd.getpwall() if user.pw_uid >= 1000]

# Default arguments are evaluated once when the function is defined, not each
# time the function is called, so default_users must be declared before.

def dump(path, users=default_users()):
    """
    Accepts a list of system users (defaults to all normal ie non-system users)
    and exports them in a properly formatted json indicated by path
    """
    user_dicts = []
    for username in users:
        user_dict = {}
        user_dict['name'] = username #assignment adds key in dictionary!
        groups = [] #in latest python, dictionaries remember insertion order
        for group in grp.getgrall():
            (gr_name, gr_passwd, gr_id, gr_members) = group #unpacking to tuple for easier testing
            if username in gr_members:
                groups.append(gr_name)
        user_dict['groups'] = groups
        (nam, pwd, lstchg, min_d, max_d, warn, inact, expire, flag) = spwd.getspnam(username)
        user_dict['password'] = pwd
        user_dicts.append(user_dict)
    with open(path, 'w') as f:
        json.dump(user_dicts, f)

def content_check(content):
    """
    exits with status 1 if json is not a list of dictionaries
    """
    error = False
    if not isinstance(content, list):
        error = True
    else:
        for element in content:
            if not isinstance(element, dict):
                error = True
                break
    if error:
        print("Parsed JSON is not a list of users")
        sys.exit(1)
