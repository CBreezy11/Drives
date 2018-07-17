from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup


app = Flask("__name__")

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

def format_user(name):
    name = name.lower()
    name = name.capitalize()
    return name

"""@app.route('/', methods=['POST', 'GET'])
def home():
    pass"""

    

@app.route('/<country>')
def data_list(country):
    for countries in country_list:
        if country.lower() in countries['Country'].lower():
            x = countries['Country']
            y = countries['Side of Road']
            return "The Country {}, {}".format(x, y)
    return "I can't seem to find that Country :("

@app.route('/complete_dictionary')
def get_country():
    return jsonify({'country_list': country_list})



load_data(get_data())
app.run(port=5000)