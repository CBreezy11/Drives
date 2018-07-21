"""All the imports, everything from flask for the web/API part
requests to pull webpages and Beautiful Soup to parse/scrap them"""

from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import util.DriveonData as DO  
from util.DriveonData import country_list
    


app = Flask("__name__")           #Make an instance of the Flask class
DO.load_data(DO.get_data())

@app.route('/', methods=['POST', 'GET'])
def index():
    greeting = "Hello World"
    if request.method == 'POST':
        country = request.form['country']
        greeting = DO.data_list(country)
        return render_template('index.html', greeting = greeting)
    else:
        return render_template('hello_form.html')

"""Create a path where the entire data_list
can be seen, just for funsies"""
          
@app.route('/complete_dictionary')
def get_country():
    return jsonify({'country_list': country_list})

"""Call load_data passing get_data to
create our data and start the API on
port 5000"""

app.run(host='0.0.0.0')