from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View

#connect couchDB
client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)

session = client.session()
#print('Username: {0}'.format(session['userCtx']['name'])) 
#print('Databases: {0}'.format(client.all_dbs()))

#connect database in the couchDB
db=client['tweet-covid-covidsafe']

#Create a designdocument for views
ddoc = DesignDocument(db,'covidsafe')
#Create a mapreduce function to group the documents by sentiment and location
ddoc. add_view('sentiment_location','function(doc){\n emit([doc.sentiment,doc.SA4],1)}','_count')
ddoc.save()