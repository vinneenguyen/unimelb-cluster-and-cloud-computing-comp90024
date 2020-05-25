from cloudant.client import CouchDB
import geopandas as gpd

client = CouchDB("admin", "password", url='http://172.26.132.48:5984', connect=True)
