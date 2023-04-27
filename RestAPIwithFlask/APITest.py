from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# create the flask app
app = Flask(__name__)
# create API object
api = Api(app)

## each class is a resource the GET, PUT, POST,    ##
## DELETE methods are the GET, PUT, POST requests. ##
## These are automatically mapped by flask_restful ##

class Hello(Resource):
    
    # get method = GET request
    def get(self):
        return jsonify({'message': 'Hello, world!'})
    
    # post method = POST request
    def post(self):
        return jsonify({"message" : "help"}), 201 # <-- This is the status code for the request
    
# A new resource that calculates the square of a number
class Square(Resource):

    def get(self, num):
        return jsonify({'square': num**2})
    

## Defines the resources and their paths in the api ##
api.add_resource(Hello, '/') # <-- '/' signifies the root of the API (ex. 'https://api.test.com/')
api.add_resource(Square, '/square/<int:num>') # <-- '<int:num>' signifies this path takes an argument "num" that is an integer type. (ex. 'https://api.test.com/square/{num})

# only run the flask server if this file is executed, not imported

if __name__ == '__main__':
    # Run a development server on "https://127.0.0.1:5000"
    # app.run(debug=False)

    # Uncomment the code below to run on a production WSGI server
    # Server will be access
    from waitress import serve
    serve(app, host='192.168.3.213', port=8080)