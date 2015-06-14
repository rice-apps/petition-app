import urllib2
import json

api_key = ""


def netid2name(netid):
    # Get the JSON response from the server
    apiResponseString = urllib2.urlopen("http://api.riceapps.org/api/people?key=" + api_key + "&net_id=" + netid).read()
    apiResponse = json.loads(apiResponseString)

    # Do something useful with it
    if apiResponse["result"] == "success":
        students = apiResponse["people"]["students"]
        return students[0]["name"]
    else:
        print "An error was encountered:", apiResponse["message"]




