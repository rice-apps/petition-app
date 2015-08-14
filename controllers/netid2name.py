import urllib2
import json

api_key = ""


def netid2name(netid):
    # Get the JSON response from the server
    api_response_string = urllib2.urlopen("http://api.riceapps.org/api/people?key=" + api_key + "&net_id=" + netid).read()
    api_response = json.loads(api_response_string)

    # Do something useful with it
    if api_response["result"] == "success":
        students = api_response["people"]["students"]
        return students[0]['name']
    else:
        print "An error was encountered:", api_response["message"]
