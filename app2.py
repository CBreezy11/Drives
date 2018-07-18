"""All the imports, everything from flask for the web/API part
requests to pull webpages and Beautiful Soup to parse/scrap them"""

from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import util.DriveonData as DO 
from util.DriveonData import country_list


app = Flask("__name__")           #Make an instance of the Flask class
DO.load_data(DO.get_data())


@app.route('/')
def index():
    return "Type in /'countryname'  placing the desired\n country name in your browser to get results"

@app.route('/<string:name>')
def results(name):
    return DO.data_list(name)

@app.route('/complete_dictionary')
def get_country():
    return jsonify({'country_list': country_list})



app.run(host='0.0.0.0')