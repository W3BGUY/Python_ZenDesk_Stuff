import os
import time
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib
import datetime
from datetime import timezone
from datetime import datetime

from additionalFunctions import runZenDeskCall
from additionalFunctions import makeItWait

zdSiteURL='https://{domain}.zendesk.com'

def getAllTickets(nextPage):
	if(nextPage=='NONE'):
		apiURL=zdSiteURL+'/api/v2/search.json?query=type:ticket%20via:api%20created<2015-12-15'
	else:
		apiURL=nextPage
	
	print("URL: "+str(apiURL));
	runagain=True
	
	getAllResults=runZenDeskCall('GET',apiURL,'')
	count=0
	deleteArray=''
	
	for key in getAllResults['results']:
		runagain=True
		print(str(key['id'])+" -> "+str(key['assignee_id'])+" -> "+str(key['updated_at']));
		
		deleteArray=deleteArray+str(key['id'])+","
		count+=1
	
	if(len(str(deleteArray))>1):
		print(str(deleteArray))
		apiURL=zdSiteURL+'/api/v2/tickets/destroy_many.json?ids='+str(deleteArray)
		getDeleteResults=runZenDeskCall('DELETE',apiURL,'')
		print("deleted: "+str(getDeleteResults))
	
	print("Waiting 3 seconds");
	print("next: "+str(getAllResults['next_page']))
	makeItWait(3)
	
	if(runagain==True):
		print("I'm going again")
		if(getAllResults['next_page'] and getAllResults['next_page']!=''):
			getAllTickets(getAllResults['next_page']);
		else:
			getAllTickets('NONE');
	else:
		print("I'm done")
		return


getAllTickets('NONE');
