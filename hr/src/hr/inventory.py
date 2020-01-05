import json
import sys

def parse(filename):
    with open(filename, 'r') as f:
        users = json.load(f)
    content_check(users)
    return users

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

