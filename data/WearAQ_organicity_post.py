import requests
import json
import pandas as pd
import os

# Set Tokens

experiment_id = ""
experimenter_id = ""
application_id = ""
body_id = "urn:oc:entity:experimenters:" + experimenter_id + ":" + experiment_id + ":"

client_id = ""
client_secret = "" 


# Read in data

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data/Workshop data/") # set directory

perception = pd.read_csv("Perception/all_perceptions_avg.csv")

# =============================================================================
#  Get Token
# =============================================================================

url = " https://accounts.organicity.eu/realms/organicity/protocol/openid-connect/token"
headers = {'Host':'accounts.organicity.eu',
           'Content_Type':'application/x-www-form-urlencoded'}
body = {'grant_type':'client_credentials',
        'client_id':'',
        'client_secret':''}

body['client_id'] = client_id
body['client_secret'] = client_secret

r = requests.post(url, headers=headers, data=body)

response = r.json()

token = response['access_token']

# =============================================================================
#  Post data
# =============================================================================

body = {
  "id": "",
  "type": "urn:oc:entityType:perception",
  "perception": {
    "value": "",
    "type": "urn:oc:attributeType:umbrellium:perception"
  },
  "location": {
    "type" : "geo:point", 
    "value" : "" 
  }, 
  "TimeInstant" : {
   "type" : "urn:oc:attributeType:ISO8601", 
   "value" : "" 
  } 
}
  
url = "https://exp.orion.organicity.eu/v2/entities"
headers = {'Authorization':'',
           'Content_Type':'application/json',
           'Accept':'application/json',
           'X-Organicity-Application':'',
           'X-Organicity-Experiment':''}

headers['Authorization'] = "Bearer " + token
headers['X-Organicity-Application'] = application_id
headers['X-Organicity-Experiment'] = experiment_id


r = requests.post(url, headers=headers, json = body)
r.json()

for i in range(len(perception)):
    body['id'] = body_id + str(i+2)
    body['perception']['value'] = str(perception.iloc[i,2])
    body['location']['value'] = str(perception.iloc[i,4]) + ", " + str(perception.iloc[i,3])
    body['TimeInstant']['value'] = perception.iloc[i,5]
    
    print(body['id'])
    
    r = requests.post(url,headers = headers, json = body)
    
    
    
    