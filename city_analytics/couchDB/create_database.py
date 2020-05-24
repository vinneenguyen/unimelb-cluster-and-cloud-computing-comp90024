from cloudant.client import CouchDB
#use client to connect couchdb
client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)

covid_db=client.create_database('tweet-covid',partitioned=True)
covidsafe_db=client.create_database('tweet-covid-covidsafe',partitioned=True)
symptom_db=client.create_database('tweet-symptom',partitioned=True)
