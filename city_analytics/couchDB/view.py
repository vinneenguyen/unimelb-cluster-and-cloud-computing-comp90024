from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View

#connect couchDB
client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)

session = client.session()
#print('Username: {0}'.format(session['userCtx']['name'])) 
#print('Databases: {0}'.format(client.all_dbs()))

#connect covidsafe database in the couchDB
covidsafe_db=client['tweet-covid-covidsafe']

#Create a covidsafe designdocument for views
covidsafe_ddoc = DesignDocument(covidsafe_db,'covidsafe')

#Create a mapreduce function to group the documents by sentiment and location
covidsafe_ddoc.add_view('sentiment_location','function(doc){\n emit([doc.sentiment,doc.SA4],1)}','_count')
covidsafe_ddoc.save()

#connect covid database in the couchDB
covid_db=client['tweet-covid']

#Create a designdocument for views
covid_ddoc = DesignDocument(covid_db,'covid')

#Create a mapreduce function to group the documents by sentiment and location
covid_ddoc.add_view('sentiment_location','function(doc){\n emit([doc.sentiment,doc.SA4],1)}','_count')
covid_ddoc.save()

#connect symptoms database in the couchDB
symptoms_db=client['symptoms']

#Create a symptoms designdocument for views
symptoms_ddoc = DesignDocument(symptoms_db,'symptoms')
symptoms_ddoc.add_view('symptoms_location','function (doc) {\n for(var i in doc.symptoms){\n if(doc.symptoms[i]=="cough"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fever"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="throat"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fatigue"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="breathing"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="headache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="bodyache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="stloss"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="vomit"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="diarrhoea"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}}}','_count')

symptoms_ddoc.save()