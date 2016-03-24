from flask import Flask
from flask.ext.restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class PersonListApi(Resource):
    """docstring for PersonList"""
    def get(self):
        pass

    def post(self):
        pass


class PersonApi(Resource):
    """docstring for PersonApi"""
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(
    PersonListApi,
    '/family/api/v1.0/persons',
    endpoint='persons')

api.add_resource(
    PersonApi,
    '/family/api/v1.0/persons/<int:id>',
    endpoint='person')

if __name__ == '__main__':
    app.run(debug=True)
