import json, sys, pwd, spwd, grp

def parse(filename):
    with open(filename, 'r') as f:
        users = json.load(f)
    content_check(users)
    return users

def default_users():
    return [user.pw_name for user in pwd.getpwall() if user.pw_uid >= 1000]

def dump(path, users=default_users()): #default arguments are evaluated once when the function is defined, not each time the function is called
    """
    exports all users of the system in properly formatted json
    """
    user_dicts = []
    for username in users:
        user_dict = {}
        user_dict['name'] = username #assignment adds key in dictionary!
        groups = [] #in latest python, dictionaries remember insertion order
        for group in grp.getgrall():
            if username in group.gr_mem:
                groups.append(group.gr_name)
        user_dict['groups'] = groups
        user_dict['password'] = spwd.getspnam(username).sp_pwd
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
