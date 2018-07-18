"""All the imports, everything from flask for the web/API part
requests to pull webpages and Beautiful Soup to parse/scrap them"""

from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup


app = Flask("__name__")           #Make an instance of the Flask class
country_list = []                 #Create global variable to hold all the data pulled from the web

"""Define method to connect to webpage and return
the html parts with the desired data"""

def get_data():
    url = 'https://www.worldstandards.eu/cars/list-of-left-driving-countries/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('td')
    return data

"""define method to parse the data into
something we can add in to our global list"""

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

"""Define a module to take the user input
and search through the list for a match. This
needs to account for using of capitilization in
input and data. If match is found format a string that gets passed to the 
html file.  If not found format a string saying so"""

def data_list(country):
    try:
        data = next(filter(lambda x: country.lower() in x['Country'].lower(), country_list))
        y = data['Country']
        z = data["Side of Road"]
        return "The Country {}, {}".format(y, z)
    except:
        return "I can't seem to find that Country :(   "

"""API will run on / with a form asking for 
input of a country.  Then sends to data_list to handle
the work and data_list returns the output back here
where the templates get rendered"""

@app.route('/', methods=['POST', 'GET'])
def index():
    greeting = "Hello World"
    if request.method == 'POST':
        country = request.form['country']
        greeting = data_list(country)
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

load_data(get_data())
app.run(host='0.0.0.0')