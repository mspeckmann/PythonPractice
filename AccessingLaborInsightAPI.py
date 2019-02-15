import simplejson
import requests
from requests_oauthlib import OAuth1
import json


consumerSecret = 'REMOVED FOR SECURITY'
consumerKey = 'BGT'
accessToken = 'Insight'
accessTokenSecret = 'REMOVED FOR SECURITY'



def make_url(path):
    return "http://sandbox.api.burning-glass.com/v205/" + path

def _get(url):
    auth = OAuth1(consumerKey, consumerSecret, accessToken, accessTokenSecret)
    html = requests.get(make_url(url), auth=auth)
    d = simplejson.loads(html.text)
    return d['result']['data']

print _get("insight/lookups?type=Salary&geography=US")
#[{u'name': u'$35,000 to $49,999'}, {u'name': u'$50,000 to $74,999'}, {u'name': u'Less than $35,000'}, {u'name': u'More than $75,000'}]


def _post(url, body):
    auth = OAuth1(consumerKey, consumerSecret, accessToken, accessTokenSecret)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    html = requests.post(make_url(url), data=json.dumps(body), auth=auth, headers=headers)
    d = simplejson.loads(html.text)
    return d['result']['data']

bgtocc_list = ["Architect","Biomedical Engineer","Chemist","Web Developer","Computer Scientist"]

minAdEdu = {
	"groupBy":"MinimumAdvertisedEducation",
	"timePeriod":
	{
		"from":"2017-03-01T00:00:00",
		"to":"2017-04-30T00:00:00"
	},
	"queryString":"[nationwide]: \" nationwide  \" and [bgtocc]: \"%s\"",
	"geography":"US",
	"includeTotalClassifiedPostings":'true',
	"includeTotalUnclassifiedPostings":'true',
	"offset":0,
	"limit":10
},(bgtocc_list[0])


print _post("insight/jobs",minAdEdu)
# {"errorCode":"COR006","developerMessage":"The oAuth Header has an invalid oauth_signature specified: QvOg8KHLY2O2uz821fXGSyl7ZU4=","userMessage":"Not authorised to use Api","moreInfo":"http://developer.burning-glass.com/error/COR006","requestId":"2653c2a5-5b5c-4a08-93c6-c6ba8c41e6be","timestamp":1510688390,"status":"failure","statusCode":"Unauthorized"}



