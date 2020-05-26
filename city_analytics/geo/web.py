from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, static_folder='../georesults', template_folder='../georesults')

@app.route('/')
def index():
   data1 = 3333
   data2 = 6666
   return render_template('index.html', data1=data1, data2=data2)

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