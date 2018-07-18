from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'coolguy'
api = Api(app)
jwt = JWT(app, authenticate, identity)

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
        
    @jwt_required()
    def delete(self, name):
        global country_list
        country_list = list(filter(lambda x: x['Country'].lower() != name.lower(), country_list))
        return "{} deleted".format(name)

class Countries(Resource):
    @jwt_required()
    def get(self):
        return country_list




load_data(get_data())
api.add_resource(Country, '/<string:name>')
api.add_resource(Countries, '/fulllist')

app.run(host='0.0.0.0', debug=True)