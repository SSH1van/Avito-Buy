import time
import os

FILE_PATH = "code.txt"

def fetch_code():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = f.read()
        os.remove(FILE_PATH)
        return data
    return None

def get_code():
    while True:
        data = fetch_code()
        if data:
            return data
        time.sleep(1)