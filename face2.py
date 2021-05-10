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
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# This key will serve all examples in this document.
KEY = "1d8af000bf8146bbaad633bae10a8d7e"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://ece3502.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

Person_Group_ID='a70b585f-5570-4997-9c6b-ca0c227df201'

test_image_array = glob.glob('test-image-person-group.jpg')
image = open(test_image_array[0], 'r+b')

print('Pausing for 30 seconds to avoid triggering rate limit on free account...')
time.sleep (30)

# Detect faces
face_ids = []
# We use detection model 3 to get better performance.
faces = face_client.face.detect_with_stream(image, detection_model='detection_03')
for face in faces:
    face_ids.append(face.face_id)
    #print(face.face_id)
# </snippet_identify_testimage>

def get_person_info(endpoint, key, group_id, candidate_id):
    """GET Request to retrieve the person info identified"""
    face_api_url = '{0}/face/v1.0/persongroups/{1}/persons/{2}'.format(endpoint, group_id, candidate_id)
    headers = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(face_api_url, headers=headers)
    return response.json()

# <snippet_identify>
# Identify faces
results = face_client.face.identify(face_ids, Person_Group_ID)
print('Identifying faces in {}'.format(os.path.basename(image.name)))
if not results:
    print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
for person in results:
	if len(person.candidates) > 0:
		print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
		person_info=get_person_info(ENDPOINT,KEY,Person_Group_ID,person.candidates[0].person_id)
		print('Name Group person identified: {0}'.format(person_info['name']))
	else:
		print('No person identified for face ID {} in {}.'.format(person.face_id, os.path.basename(image.name)))
# </snippet_identify>
print()

