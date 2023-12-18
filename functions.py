from config import load_config
import json

# Путь к файлу с логинами и паролями
config = load_config(None)
CREDENTIALS_USERS = config.db.db_CREDENTIALS_USERS
CREDENTIALS_ADMINS = config.db.db_CREDENTIALS_ADMINS
PASSWORDS = config.db.db_PASSWORDS
REQUESTS = config.db.db_REQUESTS


def save_request(name, topic, down_topic, description):
    cur = load_JSON(REQUESTS)
    num = str(len(cur) + 1)
    cur[num] = {
        'name': name,
        'topic': topic,
        'down_topic': down_topic,
        'description': description
    }

    save_JSON(cur, REQUESTS)


def change_passwords(isAdmin: bool, newpassword: str):
    # Загружаем текущие логины и пароли
    cur = load_JSON()
    if isAdmin:
        cur['admin'] = newpassword
    else:
        cur['user'] = newpassword

    save_JSON(cur, PASSWORDS)


def add_user(id, isAdmin, name: str | None):
    if isAdmin:
        credentials = load_JSON(CREDENTIALS_ADMINS)
    else:
        credentials = load_JSON(CREDENTIALS_USERS)

    if str(id) in credentials:
        return False
    else:
        credentials[str(id)] = {'name': name, 'state': False}
        if isAdmin:
            save_JSON(credentials, CREDENTIALS_ADMINS)
        else:
            save_JSON(credentials, CREDENTIALS_USERS)
        return True


def load_JSON(what):
    with open(what, 'r') as file:
        res = json.load(file)
    return res


def save_JSON(what, where):
    with open(where, 'w') as file:
        json.dump(what, file, indent=2)
