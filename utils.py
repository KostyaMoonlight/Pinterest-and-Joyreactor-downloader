import json


def load_cred(path_to_cred):
    with open(path_to_cred, "r") as f:
        cred = json.load(f)
    email = cred["email"]
    password = cred["password"]
    return email, password

    

    