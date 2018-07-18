"""All the imports, everything from flask for the web/API part
requests to pull webpages and Beautiful Soup to parse/scrap them"""

from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup


app = Flask("__name__")           #Make an instance of the Flask class
country_list = []                 #Create global variable to hold all the data pulled from the web


def get_data():
    url = 'https://www.worldstandards.eu/cars/list-of-left-driving-countries/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('td')
    return data


def load_data(data):
    i = 0
    while i < len(data):
        new_entry = {
            'Country': data[i].text,
            'Side of Road': data[i+1].text
        }
        country_list.append(new_entry)
        i += 2
    return country_list


def data_list(country):
    try:
        data = next(filter(lambda x: country.lower() in x['Country'].lower(), country_list))
        y = data['Country']
        z = data["Side of Road"]
        return "The Country {}, {}".format(y, z), 200
    except:
        return "I can't seem to find that Country :(   ", 404

@app.route('/')
def index():
    return "Type in /'countryname'  placing the desired\n country name in your browser to get results"

@app.route('/<string:name>')
def results(name):
    return data_list(name)

@app.route('/complete_dictionary')
def get_country():
    return jsonify({'country_list': country_list})


load_data(get_data())
app.run(host='0.0.0.0')