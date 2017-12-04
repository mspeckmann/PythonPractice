from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import json
import pandas as pd
import csv




domain = "<domaoni>"
client_id = '<client id>'
client_secret = '<client secret>'


def get_token(domain,client_id,client_secret):
	auth = HTTPBasicAuth(client_id, client_secret)
	client = BackendApplicationClient(client_id=client_id)
	oauth = OAuth2Session(client=client)
	return oauth.fetch_token(token_url=domain+'/oauth/v2/token', auth=auth)

def similarity_api(domain,endpoint,payload,token):
	url = domain + endpoint

	headers = {
	    'content-type': "application/json",
	    'authorization': "Bearer "+token['access_token'],
	    'cache-control': "no-cache"
	    }

	return requests.request("POST", url, data=payload, headers=headers)


# Get Token
token = get_token(domain,client_id,client_secret)

#Load BGTOCC list
#output Similarity bgtoccs and Sim Score collected from the API

bgtocclist = pd.read_csv("C:/Users/MSpeckmann/PycharmProjects/Internal/bgtocc.csv")
with open("output.csv",'wb') as f:
	writer = csv.writer(f, dialect='excel')
	i = 0
	while i <= len(bgtocclist['BGTOccName']):
		bgtoccName = bgtocclist['BGTOccName'][i]
		bgtoccId = bgtocclist['Id'][i]
		#Query the API
		payload = json.dumps({'input': {'bgtocc': [bgtoccName]}, 'type': 'structured','count':100})
		response = similarity_api(domain, "/v2.1/similarity/bgtocc", payload, token)
		d = json.loads(json.dumps(response.json()))
		x = 0
		while x < len(d["response"]["result"]):
			writer.writerow([bgtoccId, bgtoccName, d["response"]["result"][x]["name"], d["response"]["result"][x]["score"]])
			x += 1
		i += 1
