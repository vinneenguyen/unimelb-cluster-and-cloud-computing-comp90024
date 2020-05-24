from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
#from cloudant.query import Query
from cloudant.result import Result,ResultByKey
from cloudant.view import View
#from cloudant.database import CouchDatabase
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
ddoc.add_view('symptoms_location','function (doc) {\n for(var i in doc.symptoms){\n if(doc.symptoms[i]=="cough"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fever"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="throat"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fatigue"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="breathing"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="headache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="bodyache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="stloss"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="vomit"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="diarrhoea"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}}}','_count')

view=View(ddoc,'symptoms_location')
#Create a mapreduce function to group the documents by symptoms and location

ddoc.save()  
