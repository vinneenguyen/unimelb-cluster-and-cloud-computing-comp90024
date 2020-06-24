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
db=client['symptoms']

#Create a designdocument for views
ddoc = DesignDocument(db,'symptoms')
view=View(ddoc,'symptoms_location')
#the number of tweets in each symptom
with open('symptoms.json','w') as f:
    for row in view(reduce=True,group=True,group_level=1)['rows']:
        json.dump(row,f)

#the number of tweets in each symptom including their SA4 and SA4_source
with open('symptoms_location.json','w') as f:
    for row in view(reduce=True,group=True)['rows']:
        json.dump(row,f)
