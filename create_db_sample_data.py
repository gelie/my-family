from py2neo import Graph, authenticate, Node, Relationship
import os

username = os.environ.get("NEO4J_USERNAME")
password = os.environ.get("NEO4J_PASSWORD")

authenticate('localhost:7474', username, password)

graph = Graph('http://localhost:7474/db/data')

# Clear db first
graph.delete_all()

tx = graph.cypher.begin()
a = "CREATE CONSTRAINT ON (p:Person) ASSERT p.name is UNIQUE"
tx.append(a)
tx.commit()

# Import sample Persons
tx = graph.cypher.begin()

q1 = "Create (p:Person {name:'Gavin Lester Elie', dob:-80827200, sex:'M'})"
q2 = "Create (p:Person {name:'Irvin Alfred Elie', dob:-800798400, sex:'M'})"
q3 = "Create (p:Person {name:'Myrtle Sophia Elie', dob:-674913600, sex:'F'})"
q4 = "Create (p:Person {name:'Lester Colin Elie', dob:19828800, sex:'M'})"
q5 = "Create (p:Person {name:'Lynne Celeste Elie', dob:705412800, sex:'F'})"
q6 = "Create (p:Person {name:'Eustin Mark Elie', dob:-22420800, sex:'M'})"
q7 = "Create (p:Person {name:'Jacky Margaret Lewis', dob:26481600, sex:'F'})"
q8 = "Create (p:Person {name:'Ryan Benjamin Elie', dob:1140696000, sex:'M'})"
q9 = "Create (p:Person {name:'Alex Dale Elie', dob:1228219200, sex:'M'})"
q10 = "Create (p:Person {name:'Emily Kate Elie', dob:1367236800, sex:'F'})"
q11 = "Create (p:Person {name:'Jamie Marvin Lewis', dob:822052800, sex:'M'})"
q12 = "Create (p:Person {name:'Calem Elie', dob:-22420800, sex:'M'})"
q13 = "Create (p:Person {name:'Ethan Elie', dob:-22420800, sex:'M'})"
q14 = "Create (p:Person {name:'Corbin Elie', dob:-22420800, sex:'M'})"
q15 = "Create (p:Person {name:'Nazley Elie', dob:-22420800, sex:'F'})"

# Create relationships between Persons

q16 = "Match (n:Person {name:'Eustin Mark Elie'}), (b:Person {name:'Calem Elie'}) merge (n)-[:FATHER_OF]->(b)"
q17 = "Match (n:Person {name:'Nazley Elie'}), (b:Person {name:'Calem Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q18 = "Match (n:Person {name:'Eustin Mark Elie'}), (b:Person {name:'Ethan Elie'}) merge (n)-[:FATHER_OF]->(b)"
q19 = "Match (n:Person {name:'Nazley Elie'}), (b:Person {name:'Ethan Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q20 = "Match (n:Person {name:'Eustin Mark Elie'}), (b:Person {name:'Corbin Elie'}) merge (n)-[:FATHER_OF]->(b)"
q21 = "Match (n:Person {name:'Nazley Elie'}), (b:Person {name:'Corbin Elie'}) merge (n)-[:MOTHER_OF]->(b)"

q22 = "Match (n:Person {name:'Gavin Lester Elie'}), (b:Person {name:'Ryan Benjamin Elie'}) merge (n)-[:FATHER_OF]->(b)"
q23 = "Match (n:Person {name:'Jacky Margaret Lewis'}), (b:Person {name:'Ryan Benjamin Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q24 = "Match (n:Person {name:'Gavin Lester Elie'}), (b:Person {name:'Alex Dale Elie'}) merge (n)-[:FATHER_OF]->(b)"
q25 = "Match (n:Person {name:'Jacky Margaret Lewis'}), (b:Person {name:'Alex Dale Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q26 = "Match (n:Person {name:'Gavin Lester Elie'}), (b:Person {name:'Emily Kate Elie'}) merge (n)-[:FATHER_OF]->(b)"
q27 = "Match (n:Person {name:'Jacky Margaret Lewis'}), (b:Person {name:'Emily Kate Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q28 = "Match (p1:Person {name:'Jamie Marvin Lewis'}),(p2:Person {name:'Jacky Margaret Lewis'}) MERGE (p2)-[r:MOTHER_OF]->(p1)"

q29 = "Match (n:Person {name:'Irvin Alfred Elie'}), (b:Person {name:'Gavin Lester Elie'}) merge (n)-[:FATHER_OF]->(b)"
q30 = "Match (n:Person {name:'Myrtle Sophia Elie'}), (b:Person {name:'Gavin Lester Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q31 = "Match (n:Person {name:'Irvin Alfred Elie'}), (b:Person {name:'Eustin Mark Elie'}) merge (n)-[:FATHER_OF]->(b)"
q32 = "Match (n:Person {name:'Myrtle Sophia Elie'}), (b:Person {name:'Eustin Mark Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q33 = "Match (n:Person {name:'Irvin Alfred Elie'}), (b:Person {name:'Lester Colin Elie'}) merge (n)-[:FATHER_OF]->(b)"
q34 = "Match (n:Person {name:'Myrtle Sophia Elie'}), (b:Person {name:'Lester Colin Elie'}) merge (n)-[:MOTHER_OF]->(b)"
q35 = "Match (n:Person {name:'Irvin Alfred Elie'}), (b:Person {name:'Lynne Celeste Elie'}) merge (n)-[:FATHER_OF]->(b)"
q36 = "Match (n:Person {name:'Myrtle Sophia Elie'}), (b:Person {name:'Lynne Celeste Elie'}) merge (n)-[:MOTHER_OF]->(b)"

q37 = "MATCH (a:Person)<-[r1:FATHER_OF|MOTHER_OF]-(p:Person)-[r2:FATHER_OF|MOTHER_OF]->(b:Person) WHERE p.name IN ['Gavin Lester Elie','Jacky Margaret Lewis']MERGE (a)-[r3:SIBLING_OF]-(b)"

q38 = "MATCH (a:Person)<-[r1:FATHER_OF|MOTHER_OF]-(p:Person)-[r2:FATHER_OF|MOTHER_OF]->(b:Person) WHERE p.name IN ['Irvin Alfred Elie','Myrtle Sophia Elie'] MERGE (a)-[r3:SIBLING_OF]-(b)"
q39 = "Match (a:Person)<-[r1:FATHER_OF|MOTHER_OF]-(p:Person)-[r2:FATHER_OF|MOTHER_OF]->(b:Person) WHERE p.name IN ['Eustin Mark Elie','Nazley Elie'] MERGE (a)-[r3:SIBLING_OF]-(b)"

tx.append(q1)
tx.append(q2)
tx.append(q3)
tx.append(q4)
tx.append(q5)
tx.append(q6)
tx.append(q7)
tx.append(q8)
tx.append(q9)
tx.append(q10)
tx.append(q11)
tx.append(q12)
tx.append(q13)
tx.append(q14)
tx.append(q15)
tx.append(q16)
tx.append(q17)
tx.append(q18)
tx.append(q19)
tx.append(q20)
tx.append(q21)
tx.append(q22)
tx.append(q23)
tx.append(q24)
tx.append(q25)
tx.append(q26)
tx.append(q27)
tx.append(q28)
tx.append(q29)
tx.append(q30)
tx.append(q31)
tx.append(q32)
tx.append(q33)
tx.append(q34)
tx.append(q35)
tx.append(q36)
tx.append(q37)
tx.append(q38)
tx.append(q39)

tx.commit()
