import couchdb
import json

couch = couchdb.Server("http://admin:password@172.26.131.173:5984/")
# db = couch.create("myx-demo")
db = couch["twitter"]
cnt = 0

with open("results/10 May/cleaned_73m.json") as input:
    for line in input:
        cnt += 1
        js = json.loads(line)
        doc = {"_id": js["id_str"], "tweet": js}
        try:
            doc_id, doc_rev = db.save(doc)
        except couchdb.http.ResourceConflict:
            pass
        if cnt % 1000 == 0:
            print(cnt)

# print(cnt)
