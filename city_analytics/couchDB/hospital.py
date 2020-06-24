from cloudant.client import CouchDB
from cloudant.document import Document
from cloudant.design_document import DesignDocument
from cloudant.query import Query
from cloudant.result import Result,ResultByKey
from cloudant.view import View
from cloudant.database import CouchDatabase
import json
import time
import sys
import math

try:
    client = CouchDB("admin", "password", url='http://172.26.132.48:5984', connect=True)
    session = client.session()
except Exception as e:
    print('Connection unsuccessful')
    sys.exit()


try:
    db = client['myhospital']
except:
    db = client.create_database('myhospital')

with open('data3036041311591781631.json') as f:
    data = json.load(f)


pathSA4 = "SA4_area_coordinates.json"

def check_SA4_with_geo(input_json):
    """
        calculate the distance between the tweet geo location with the boundaries of each statistics area,
        return the area code with minimum distance. If the minimum distance is greater than 10 we treat it
        as not in Australia or location point is not accurate.
    """
    with open(pathSA4) as f:
        for line in f:
            SA4_json = json.loads(line)

    input_geo_point = [input_json['properties']['long'], input_json['properties']['lat']]
    sa4_code = -1  # default -1
    min_distance = 999999999999
    for i in range(len(SA4_json['features'])):
        feature = SA4_json['features'][i]
        cur_sa4_code = feature['properties']['sa4_code_2016']
        for j in range(len(feature['geometry']['coordinates'])):
            coordinate = feature['geometry']['coordinates'][j]
            for k in range(len(coordinate[0])):
                try:
                    point = coordinate[0][k]  # point[0] : longitude, point[1] : latitude
                    cur_distance = math.sqrt(
                        (input_geo_point[0] - point[0]) ** 2 + (input_geo_point[1] - point[1]) ** 2)
                    if cur_distance < min_distance:
                        sa4_code = cur_sa4_code
                        min_distance = cur_distance
                except TypeError:
                    pass
    return -1 if min_distance > 10 else int(sa4_code)


for tweet in data['features']:

    a = check_SA4_with_geo(tweet)
    doc = {'_id': str(tweet['properties']['id']), 'SA4': a}
    doc.update(tweet)
    db.create_document(doc)




ddoc = DesignDocument(db,'myhospital')
ddoc.add_view('sentiment_location','function(doc){\n emit([doc.SA4],1)}','_count')
try:
    ddoc.save()
except Exception as e:
        print('Connection unsuccessful')















