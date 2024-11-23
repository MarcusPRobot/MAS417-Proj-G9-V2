import os
from time import sleep
import requests
import urllib.request
from apiKey import Meshy_APIKey

def gen_model(meshName, meshDesc):
    payload = {
        "mode": "preview",
        "prompt": meshDesc,
        "art_style": "realistic",
        "negative_prompt": "low quality, low resolution, low poly, ugly"
    }
    headers = {
        "Authorization": f"Bearer {Meshy_APIKey}"
    }

    response = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    taskID = response.json().get('result')

    progresscounter(taskID)
    retrieveModel(taskID, meshName)

def refineModel(taskID, meshName):
    payload = {
        "mode": "refine",
        "preview_task_id": taskID
    }
    headers = {
        "Authorization": f"Bearer {Meshy_APIKey}"
    }

    response = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers=headers,
        json=payload,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exception:
        print("Exception: " + exception.response.text)
        return

    taskID = response.json().get('result')

    progresscounter(taskID)
    retrieveModel(taskID, meshName)

def retrieveModel(task_id, meshName):
    success = True

    headers = {
        "Authorization": f"Bearer {Meshy_APIKey}"
    }

    response = requests.get(
        f"https://api.meshy.ai/v2/text-to-3d/{task_id}",
        headers=headers,
    )


    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exception:
        print("Exception: " + exception.response.text)
        success = False

    if success:
        print("Model generation successful")
        modelURLs = response.json().get('model_urls')
        print(modelURLs)
        if 'obj' in modelURLs:
            modelURL = modelURLs['obj']
        else:
            print("Model URL is not found\n")
            return
        print("Downloading model from: " + modelURL + "...\n")
        installmodel(modelURL, meshName)
    else:
        print("Model generation failed\n")
        return

def installmodel(modelURL, meshName):
    filePath = meshName + ".obj"
    fileDestination = "meshyModels/" + filePath

    urllib.request.urlretrieve(modelURL, filePath)
    print("Model downloaded as 3D Model.obj")

    os.rename(filePath, fileDestination)
    
def progresscounter(taskID):
    exceptionCount = 0
    print("Generating model - 0%")

    while True:
        headers = {
            "Authorization": f"Bearer {Meshy_APIKey}"
        }
        response = requests.get(
            f"https://api.meshy.ai/v2/text-to-3d/{taskID}",
            headers=headers,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            print("Exception: " + exception.response.text)
            print("Exception number " + str(exceptionCount) + " out of 3 permitted.")
            exceptionCount += 1
            if exceptionCount > 3:
                return

        taskProgress = response.json().get('progress')
        print(taskProgress)
        print("Generating model - " + str(taskProgress) + "%", end='\r')

        sleep(1)
        if taskProgress == 100:
            return