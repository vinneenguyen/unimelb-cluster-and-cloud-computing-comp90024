from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View
import json

#connect couchDB
client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)

session = client.session()
#print('Username: {0}'.format(session['userCtx']['name'])) 
#print('Databases: {0}'.format(client.all_dbs()))

#connect database in the couchDB
db=client['tweet-covid-covidsafe']

#connect a designdocument named covidsafe
ddoc = DesignDocument(db,'covidsafe')

#tweet-covid seperated by SA4_source
#view for all tweets include geo location
view=View(ddoc,'sentiment_location',partition_key='geo')


#the number of negative/positive/neutral tweets related covidsafe app
with open('covidsafe_geo.json','w') as f:
    for row in view(reduce=True,group=True,group_level=1)['rows']:
             json.dump(row,f)

#the number of negative/positive/neutral tweets including SA4
with open('covidsafe_geo_location.json','w') as f:
    for row in view(reduce=True,group=True)['rows']:
             json.dump(row,f)

#tweet-covid-covidsafe seperated by SA4_source
#view for all tweets include city name
view=View(ddoc,'sentiment_location',partition_key='name')


#the number of negative/positive/neutral tweets
with open('covidsafe_name.json','w') as f:
    for row in view(reduce=True,group=True,group_level=1)['rows']:
             json.dump(row,f)

#the number of negative/positive/neutral tweets including SA4
with open('covidsafe_name_location.json','w') as f:
    for row in view(reduce=True,group=True)['rows']:
             json.dump(row,f)