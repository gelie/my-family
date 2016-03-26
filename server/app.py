"""My Family App."""
from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, fields, marshal, reqparse
from py2neo import Graph, authenticate
import os
import time
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('/etc/nginx/ssl/nginx.crt', '/etc/nginx/ssl/nginx.key')

app = Flask(__name__)
api = Api(app)

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

if username and password:
    authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

person_fields = {
    'name': fields.String,
    'dob': fields.String,
    'sex': fields.String,
    'uri': fields.Url('person', absolute=True, scheme='https'),
    'parents': {},
    'siblings': {}
}


class PersonListApi(Resource):
    """docstring for PersonList."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No name provided',
                                   location='json')
        self.reqparse.add_argument('dob', type=int, required=True,
                                   help='Enter your date of birth ',
                                   location='json')
        self.reqparse.add_argument('sex', type=str, required=True,
                                   help='Enter your sex',
                                   location='json')
        super(PersonListApi, self).__init__()

    def get(self):
        """."""
        query = """
            match (p:Person)
            return p.name, p.dob, p.sex, id(p)
            order by p.name
            """
        result = graph.cypher.execute(query)
        output = []
        for x in result:
            dob = time.strftime("%c", time.gmtime(x[1]))
            person = marshal({"name": x[0], "dob": dob, "sex": x[2], "id": x[3]}, person_fields)
            output.append(person)
        return {'persons': output}

    def post(self):
        """."""

        args = self.reqparse.parse_args()
        person = {
            "name": args['name'],
            "dob": args['dob'],
            "sex": args['sex'],
        }

        query = """
            CREATE (p:Person {name: {name}, dob: {dob}, sex: {sex}})
            RETURN id(p)
            """
        result = graph.cypher.execute(query, person)
        id = result[0][0]
        dob = time.strftime("%c", time.gmtime(person['dob']))

        person['id'] = id
        person['dob'] = dob

        # result = graph.cypher.execute(query, {"name": args['name'], "dob": args['dob'], "sex": args['sex']})
        # output = []
        # for x in result:
        #     output.append(x.Name)
        return {"person": marshal(person, person_fields)}


class PersonApi(Resource):
    """docstring for PersonApi."""

    def get(self, id):
        """."""
        result = graph.cypher.execute(
            "match(p: Person) where id(p)={id}\
            return p.name, p.dob, p.sex", {"id": id})
            # "match(p: Person) where p.name='Gavin Lester Elie'\
            # return p.name, p.dob, p.sex")
        dob = time.strftime("%c", time.gmtime(result[0][1]))
        person = {"name": result[0][0], "dob": dob, "sex": result[0][2], "id": id}
        return {'person': marshal(person, person_fields)}

    def put(self, id):
        """."""
        pass

    def delete(self, id):
        """."""
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
    app.run(debug=True, ssl_context=context)
