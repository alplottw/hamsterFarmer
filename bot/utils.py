import datetime
import json
import random
import time


def read_account_from_file(file_path='./accounts.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def log(filename, text):
    with open(f"accounts/account_{filename}.txt", 'a+') as file:
        file.seek(0, 0)
        file.write(f"{text}\n")

def get_timestamp():
    return int(datetime.datetime.now().timestamp())


def get_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def delay(min, max):
    time.sleep(random.uniform(min, max))
