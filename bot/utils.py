import datetime
import json
import os
import random
import time


def read_account_from_file(file_path='./accounts.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def log(account_id, data, write=True):
    date_time = get_date_time()

    text = f"{date_time} | id: {account_id}"
    for key, value in data.items():
        text += f" | {key}: {value}"

    print(text)

    if write:
        with open(f"accounts/account_{account_id}.txt", 'a+') as file:
            file.seek(0, 0)
            file.write(f"{text}\n")


def get_timestamp():
    return int(datetime.datetime.now().timestamp())


def get_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def delay(min, max):
    time.sleep(random.uniform(min, max))


def save_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def create_directory_structure():
    create_directory("./accounts")
    create_directory("./logs")


def create_directory(directory_name):
    os.makedirs(directory_name, exist_ok=True)
