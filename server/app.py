"""My Family App."""
from flask import Flask, jsonify, request
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
    'parents': fields.Url('parents', absolute=True, scheme='https'),
    'uri': fields.Url('person', absolute=True, scheme='https')
}


class PersonListApi(Resource):
    """Displaying all the persons and adding to the list."""

    def __init__(self):
        """Init method."""
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
        """Retrieve all Persons."""
        query = """
            match (p:Person)
            return p.name, p.dob, p.sex, id(p)
            order by p.name
            """
        result = graph.cypher.execute(query)
        output = []
        for x in result:
            dob = time.strftime("%c", time.gmtime(x[1]))
            person = marshal(
                {"name": x[0], "dob": dob, "sex": x[2],
                 "id": x[3]}, person_fields)
            output.append(person)
        return {'persons': output}

    def post(self):
        """Create a new Person."""

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
        person['id'] = result[0][0]
        person['dob'] = time.strftime("%c", time.gmtime(person['dob']))
        return {"person": marshal(person, person_fields)}


class PersonApi(Resource):
    """docstring for PersonApi."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('dob', type=int, location='json')
        self.reqparse.add_argument('sex', type=str, location='json')
        super(PersonApi, self).__init__()

    def get(self, id):
        """."""
        result = graph.cypher.execute(
            "match(p: Person) where id(p)={id}\
            return p.name, p.dob, p.sex", {"id": id})
        dob = time.strftime("%c", time.gmtime(result[0][1]))
        person = {"name": result[0][0], "dob": dob,
                  "sex": result[0][2], "id": id}
        return {'person': marshal(person, person_fields)}

    def put(self, id):
        """Updating a Person's details."""
        result = graph.cypher.execute(
            "MATCH (p:Person) WHERE id(p)={id} RETURN p", {"id": id})
        person = result[0][0].properties
        args = request.json  # self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                person[k] = v

        return {"person": person}

    def delete(self, id):
        """Delete a person and all his relations from the database."""

        query = "MATCH (n) WHERE id(n)={id} DETACH DELETE n"
        graph.cypher.execute(query, {"id": id})
        return jsonify({"message": "Record %d deleted!" % id})


class ParentsListApi(Resource):
    """Retrieve a person's parents."""

    def __init__(self):
        """initialise parser."""
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
        super(ParentsListApi, self).__init__()

    def get(self, id):
        """Retrieve a person's parents."""
        query = """
            MATCH (a:Person)<-[r:MOTHER_OF|FATHER_OF]-(b)
            WHERE id(a)={id}
            RETURN b.name, b.dob, b.sex, id(b)
            """
        result = graph.cypher.execute(query, {"id": id})
        parents = {}
        for parent in result:
            person = {"name": parent[0], "dob": parent[
                1], "sex": parent[2], "id": parent[3]}
            person = marshal(person, person_fields)
            if parent[2] == "F":
                parents['mother'] = person
            else:
                parents['father'] = person
        return {"parents": parents}

    def post(self, id):
        """Add a person's parent."""

        # check how many parents there are.
        query = "MATCH (a:Person)<-[r:MOTHER_OF|FATHER_OF]-(b) WHERE id(a)={id} RETURN count(*) as count"
        result = graph.cypher.execute(query, {"id": id})

        if (result[0].count < 2):
            person = {}
            args = self.reqparse.parse_args()
            for k, v in args.iteritems():
                if v is not None:
                    person[k] = v
            tx = graph.cypher.begin()
            query = "MERGE (parent:Person {name: {person}.name}) ON CREATE SET parent = {person} RETURN parent"
            tx.append(query)
            if person.sex == "M":
                rel = "FATHER_OF"
            else:
                rel = "MOTHER_OF"
            graph.cypher.execute(query, {"person": person})
            tx.commit()
            return jsonify({'person': person})
        else:
            return jsonify({'error': 'Person has 2 parents already!!'})

api.add_resource(
    PersonListApi,
    '/family/api/v1.0/persons',
    endpoint='persons')

api.add_resource(
    PersonApi,
    '/family/api/v1.0/persons/<int:id>',
    endpoint='person')

api.add_resource(
    ParentsListApi,
    '/family/api/v1.0/persons/<int:id>/parents',
    endpoint='parents')

if __name__ == '__main__':
    app.run(debug=True, ssl_context=context)
