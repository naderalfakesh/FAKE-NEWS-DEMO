from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_cors import CORS
from json import dumps
import mymodel
import scrapper
import pandas as pd 



# from flask.ext.jsonpify import jsonify

app = Flask(__name__)
CORS(app)
api = Api(app)

#  customer request input parsing
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('text')

class predict(Resource):
     #  make predictions on data from user inputs. 
     def post(self):
          args = parser.parse_args()
          news = str(args['title']) + ' ' + str(args['text'])
          return mymodel.prediction(news)

class fakes(Resource):
     #  scrape 10 news from fake news site and return the prediction as a list of dictionaries
     def get(self):
          prelist = []
          for new in scrapper.getnpr():
               prelist.append(mymodel.prediction(new))
          return prelist

class reals(Resource):
     #  scrape 10 news from BBC news site and return the prediction as a list of dictionaries
     def get(self):
          prelist = []
          for new in scrapper.getbbc():
               prelist.append(mymodel.prediction(new))
          return prelist

# API routes 
api.add_resource(predict, '/predict') # 
api.add_resource(fakes, '/fakes') # 
api.add_resource(reals, '/reals') # 

if __name__ == '__main__':
     app.run(port='5002',debug=False)

