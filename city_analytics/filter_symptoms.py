from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.query import Query
from cloudant.result import Result,ResultByKey
from cloudant.view import View
from cloudant.database import CouchDatabase
import json
import time
import sys

# Connect to CouchDB

def init_connect(retries=0):
	'''
	Connect to CouchDB, keep trying if fails to connect after 10s
	'''
	try:
		client = CouchDB("admin", "password", url='http://172.26.132.48:5984', connect=True)
		session = client.session()
	except Exception as e:
	    print('Connection unsuccessful' + str(retries))
	    time.sleep(10)
	    return init_connect(retries+1)
	
	return client


def create_views(client):
	"""
	Create views if doesn't exist, and connect to databases
	"""

	try:
		symptoms_db = client['symptoms']
	except:
		symptoms_db = client.create_database('symptoms')
		ddoc_symptoms = DesignDocument(symptoms_db,'symptoms')
		ddoc_symptoms.add_view('symptoms_location','function (doc) {\n for(var i in doc.symptoms){\n if(doc.symptoms[i]=="cough"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fever"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="throat"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="fatigue"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="breathing"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="headache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="bodyache"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="stloss"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="vomit"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}\n if(doc.symptoms[i]=="diarrhoea"){\n emit([doc.symptoms[i],doc.SA4,doc.SA4_source],1);}}}','_count')
		view=View(ddoc_symptoms,'symptoms_location')
		#Create a mapreduce function to group the documents by symptoms and location

		ddoc_symptoms.save()	
	covidsymptom_db=client['tweet-covid-symptom']


	#CovidSafe Database and create views
	#Create a covidsafe designdocument for views
	#Create a mapreduce function to group the documents by sentiment and location
	covidsafe_db=client['tweet-covid-covidsafe']
	covidsafe_ddoc = DesignDocument(covidsafe_db,'covidsafe')
	covidsafe_ddoc.add_view('sentiment_location','function(doc){\n emit([doc.sentiment,doc.SA4],1)}','_count')
	try:
		covidsafe_ddoc.save()
	except:
		pass

	#Covid Database, create views, and mapreduce functions
	covid_db=client['tweet-covid']
	covid_ddoc = DesignDocument(covid_db,'covid')
	covid_ddoc.add_view('sentiment_location','function(doc){\n emit([doc.sentiment,doc.SA4],1)}','_count')
	try:
		covid_ddoc.save()
	except:
		pass

	return symptoms_db,covidsymptom_db,covidsafe_db,covid_db

# Filter tweet-covid-symptom and to symptom db continuously, sleep for 15

	
def get_timestamp(symptoms_db):
	"""
	Update view and get last timestamp
	"""
	try:	
		ddoc = DesignDocument(symptoms_db,'timestamp')
		view=View(ddoc,'timestamp')
		for row in view(descending=True,limit=1)['rows']:
			timestamp = (row['key'])
	except:
		ddoc = DesignDocument(symptoms_db,'timestamp')
		ddoc.add_view('timestamp','function(doc){\n emit(doc.timestamp,1)}')
		ddoc.save()
		timestamp=1

	return timestamp


#fever, cough, throat, fatigue, breathing, headache, bodyache, stloss, vomit, diarrhoea 

def create_doc(tweet,symptoms_db, sym_name):

	symptoms_db.create_document({
	'_id': tweet['id_str'],
	'create_at': tweet['create_at'],
	'sentiment': tweet['sentiment'],
	'SA4': tweet['SA4'],
	'SA4_source': tweet['SA4_source'],
	'symptoms': [[sym_name]],
	'timestamp': tweet['timestamp']
	})

def update_doc(tweet,symptoms_db,sym_name):
	
	doc_=symptoms_db[tweet['id_str']]
	if [sym_name] not in doc_['symptoms']:
		doc_['symptoms'].append([sym_name])
		doc_.save()


def selector_sym(db,timestamp, regex, sym_name):
	selector={'timestamp':{'$gte':timestamp},'text':{'$regex':regex}}
	docs = db.get_query_result(selector)
	number_doc=0
	for tweet in docs:
		number_doc += 1
		try:
			if tweet['id_str'] in symptoms_db:
				update_doc(tweet,symptoms_db,sym_name)
								
			else:
				create_doc(tweet,symptoms_db,sym_name)
				
		except Exception as e:
			print('uh oh')
	print('number of doc filtered', sym_name,' :', number_doc)
	return docs

def symptoms(db, symptoms_db):
	
	timestamp = get_timestamp(symptoms_db)
	print(timestamp)
	selector_sym(db,timestamp,regex='(?i)(fever)',sym_name='fever')
	selector_sym(db,timestamp,regex='(?i)(cough|dry cough)',sym_name='cough')
	selector_sym(db,timestamp,regex='(?i)(sore throat)',sym_name='throat')
	selector_sym(db,timestamp,regex='(?i)(fatigue|tiredness)',sym_name='fatigue')
	selector_sym(db,timestamp,regex='(?i)(difficulty breathing)',sym_name='breathing')
	selector_sym(db,timestamp,regex='(?i)(headache)',sym_name='headache')
	selector_sym(db,timestamp,regex='(?i)(joint pain|bodyache)',sym_name='bodyache')
	selector_sym(db,timestamp,regex='(?i)(smell loss|taste loss)',sym_name='stloss')
	selector_sym(db,timestamp,regex='(?i)(vomit|nausea)',sym_name='vomit')
	selector_sym(db,timestamp,regex='(?i)(diarrhoea|diarrhea)',sym_name='diarrhoea')
	


def updateViews(symptoms_db,covidsafe_db,covid_db):
	# Update Views
	ddoc_symptoms = DesignDocument(symptoms_db,'symptoms')
	view=View(ddoc_symptoms,'symptoms_location')

	covidsafe_ddoc = DesignDocument(covidsafe_db,'covidsafe')
	view=View(covidsafe_ddoc,'symptoms_location')

	covid_ddoc = DesignDocument(covid_db,'covid')
	view=View(covid_ddoc,'symptoms_location')


	
if __name__ == '__main__':

    client=init_connect()
    while True:
	    symptoms_db,covidsymptom_db,covidsafe_db,covid_db=create_views(client)
	    symptoms(covidsymptom_db,symptoms_db)
	    updateViews(symptoms_db,covidsafe_db,covid_db)
	    time.sleep(2)


	#Create a designdocument for views


	#client.disconnect()

	# selector={'create_at':{'$gt':last_id},'text':{'$regex':}}
	# docs = selector_sym(timestamp, '(?i)(fever)')
	
	# for tweet in docs:
	# 	#print(tweet['id_str'])
		
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'fever')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'fever')
				
	# 	except Exception as e:
	# 		print('uh oh')

	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(cough|dry cough)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'cough')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'cough')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'cough')

	# 	except Exception as e:
	# 		print('uh oh')

	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(sore throat)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'throat')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'throat')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'throat')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(fatigue|tiredness)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'fatigue')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'fatigue')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'fatigue')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(difficulty breathing)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'breathing')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'breathing')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'breathing')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(headache)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'headache')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'headache')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'headache')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(joint pain|bodyache)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'bodyache')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'bodyache')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'bodyache')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(smell loss|taste loss)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'smtloss')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'stloss')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'stloss')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(vomit)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'vomit')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'vomit')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'vomit')

	# 	except Exception as e:
	# 		print('uh oh')


	# selector={'id_str':{'$gt':last_id},'text':{'$regex':'(?i)(diarrhoea)'}}
	# docs = db.get_query_result(selector)
	# print(last_id,'diarrhoea')
	# for tweet in docs:
	# 	print(tweet['id_str'])
	# 	try:
	# 		if tweet['id_str'] in symptoms_db:
	# 			update_doc(tweet,symptoms_db,'diarrhoea')
								
	# 		else:
	# 			create_doc(tweet,symptoms_db,'diarrhoea')

	# 	except Exception as e:
	# 		print('uh oh')


	

                                