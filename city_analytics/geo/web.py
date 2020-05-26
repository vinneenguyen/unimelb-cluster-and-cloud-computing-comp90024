from flask import Flask, redirect, url_for, request, render_template
from cloudant.client import CouchDB
from cloudant.design_document import DesignDocument
from cloudant.view import View
import json

app = Flask(__name__, static_folder='../georesults', template_folder='../georesults')

def _access_covid_nums():
    client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)
    session = client.session()
    db=client['tweet-covid']

        #Connect a designdocument name covid
    ddoc = DesignDocument(db,'covid') 
    total = 0
    view=View(ddoc,'sentiment_location',partition_key='name')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']

    view=View(ddoc,'sentiment_location',partition_key='geo')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']

    view=View(ddoc,'sentiment_location',partition_key='none')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']
    
    return total

def _access_covidsafe_nums():
    client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)
    session = client.session()
    db=client['tweet-covid-covidsafe']

        #Connect a designdocument name covid
    ddoc = DesignDocument(db,'covidsafe') 
    total = 0
    view=View(ddoc,'sentiment_location',partition_key='name')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']

    view=View(ddoc,'sentiment_location',partition_key='geo')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']

    view=View(ddoc,'sentiment_location',partition_key='none')

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']
    
    return total

def _access_symptoms_nums():
    client = CouchDB("admin", "password", url='http://172.26.131.173:5984', connect=True)

    session = client.session()
    #print('Username: {0}'.format(session['userCtx']['name'])) 
    #print('Databases: {0}'.format(client.all_dbs()))

    #connect database in the couchDB
    db=client['symptoms']

    #Create a designdocument for views
    ddoc = DesignDocument(db,'symptoms')
    view=View(ddoc,'symptoms_location')
    total = 0

    for i in view(reduce=True,group=True,group_level=1)['rows']:
        print(i['value'])
        total = total + i['value']
    
    return total

@app.route('/')
def index():

    total = _access_covid_nums()
    total2 = _access_covidsafe_nums()
    total3 = _access_symptoms_nums()
    return render_template('index.html', data1=total, data2=total2, data3=total3)

@app.route('/get_map1')
def get_map1():
    return render_template('covid_sa4.html')

@app.route('/get_map2')
def get_map2():
    return render_template('covidsafe_sentiment_sa4.html')

@app.route('/get_map3')
def get_map3():
    return render_template('chart1.html')

@app.route('/get_map4')
def get_map4():
    return render_template('chart2.html')

"""
@app.route('/success/<name>')
def success(name):
	

	f2 = open("test.txt","r")
	lines = f2.readlines()
	webpage = name + '.html'
	#return "%s" % lines
	return render_template(webpage)

@app.route('/data',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

"""
if __name__ == '__main__':
   app.run(
      #host='0.0.0.0',
      #port= 6666,
      debug=True
    )