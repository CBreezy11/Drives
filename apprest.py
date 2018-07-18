from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import util.DriveonData as DO 
from util.DriveonData import country_list


app = Flask(__name__)
app.secret_key = 'coolguy'
api = Api(app)
jwt = JWT(app, authenticate, identity)

DO.load_data(DO.get_data())



class Country(Resource):
    def get(self, name):
        country = DO.data_list(name)
        return country
        
    @jwt_required()
    def delete(self, name):
        global country_list
        country_list = list(filter(lambda x: x['Country'].lower() != name.lower(), country_list))
        return "{} deleted".format(name)

class Countries(Resource):
    def get(self):
        return country_list


api.add_resource(Country, '/<string:name>')
api.add_resource(Countries, '/fulllist')

app.run(host='0.0.0.0', debug=True)