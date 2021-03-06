import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
'''
def init():
    KEY = "1d8af000bf8146bbaad633bae10a8d7e"
    ENDPOINT = "https://ece3502.cognitiveservices.azure.com/"
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    return face_client
'''
def person_group(face_client):
    PERSON_GROUP_ID = str(uuid.uuid4())
    print('Person group ID:', PERSON_GROUP_ID)
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
    neeraj=face_client.person_group_person.create(PERSON_GROUP_ID, "Neeraj")
    utkarsh=face_client.person_group_person.create(PERSON_GROUP_ID, "Utkarsh")
    shivani=face_client.person_group_person.create(PERSON_GROUP_ID, "Shivani")
    pulkit=face_client.person_group_person.create(PERSON_GROUP_ID, "Pulkit")

    neeraj_images=[file for file in glob.glob('*.jpg') if file.startswith("N")]
    utkarsh_images=[file for file in glob.glob('*.jpg') if file.startswith("U")]
    shivani_images=[file for file in glob.glob('*.jpg') if file.startswith("S")]
    pulkit_images=[file for file in glob.glob('*.jpg') if file.startswith("P")]

    for image in neeraj_images:
        n = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, neeraj.person_id,n)
    
    #time.sleep(60)

    for image in utkarsh_images:
        u = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, utkarsh.person_id,u)

    #time.sleep(60)

    for image in shivani_images:
        s = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, shivani.person_id,s)
    
    #time.sleep(60)

    for image in pulkit_images:
        p = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, pulkit.person_id,p)

    #time.sleep(60)

    print('Training the person group...')

    face_client.person_group.train(PERSON_GROUP_ID)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
            sys.exit('Training the person group has failed.')
        time.sleep(5)

    return PERSON_GROUP_ID

def get_person_info(endpoint, key, group_id, candidate_id):
    """GET Request to retrieve the person info identified"""
    face_api_url = '{0}/face/v1.0/persongroups/{1}/persons/{2}'.format(endpoint, group_id, candidate_id)
    headers = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(face_api_url, headers=headers)
    return response.json()

if __name__=='__main__':
    #face_client=init()
    KEY = "1d8af000bf8146bbaad633bae10a8d7e"
    ENDPOINT = "https://ece3502.cognitiveservices.azure.com/"
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    PERSON_GROUP_ID=person_group(face_client)
