import requests
from bs4 import BeautifulSoup


def get_data():
    url = 'https://www.worldstandards.eu/cars/list-of-left-driving-countries/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all('td')
    return data

def load_data(data):
    i = 0
    country_list = []
    while i < len(data):
        new_entry = {
                'Country': data[i].text,
                'Side of Road': data[i+1].text
            }
        country_list.append(new_entry)
        i += 2
    return country_list

