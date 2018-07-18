from flask import Flask, request
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

country_list = []

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
        return "I can't seem to find that Country :(   ", 401

class Country(Resource):
    def get(self, name):
        country = data_list(name)
        return country




load_data(get_data())
api.add_resource(Country, '/<string:name>')
app.run(host='0.0.0.0')