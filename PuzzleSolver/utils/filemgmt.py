import os
from os import path
import requests
import shutil


import utils.globalDefine as globalDefine

puzzleSourceName =  "shuffle_image.jpg"
puzzleSolutionName =  "solution_image.jpg"

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

def downloadImageAndSave(imgUrl, targetFileName):
    img_resp = requests.get(imgUrl, stream=True)
    local_file = open(targetFileName, 'wb')
    img_resp.raw.decode_content = True
    shutil.copyfileobj(img_resp.raw, local_file)
    return validateLocalPath(targetFileName)

def processPuzzleUrl(imgUrl):
    shuffle_img = os.path.join(os.getcwd(), globalDefine.MAIN_DATA_HOME, puzzleSourceName)
    return downloadImageAndSave(imgUrl, shuffle_img), shuffle_img

def processSolutionUrl(imgUrl):
    solution_img = os.path.join(os.getcwd(), globalDefine.MAIN_DATA_HOME, puzzleSolutionName)
    return downloadImageAndSave(imgUrl, solution_img), solution_img

