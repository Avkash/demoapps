from os import path
import requests


def validateLocalPath(file_path):
    return path.exists(file_path)

def validateUrlPath(url):
    try:
        page = requests.get(url)

    except Exception as e:
        return False

    if (page.status_code != 200):
        return False

    return True