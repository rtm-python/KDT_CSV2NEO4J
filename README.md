# KDT_CSV2NEO4J
_Store data from CSV-file to Neo4j-database (interview test)_


## Specification

A. Implement python-script, which handles data from CSV-file to store it in Neo4j-database. Follow next matching rules for Person and Organization entities:
id -> Person.id (unique)
name  -> Person.name
sort_name -> Person.alias
email -> Person.email
'GB (Great Britain) -> Person.nationality
id -> Person.membership_in
group_id -> Organization.group_id (unique)
group -> Organization.name
group_id -> Organization.members

B. Integrate ElasticSearch with Neo4j-database for fulltext searching

C. Implement base REST API service for data stored in Neo4j-database with Flask or similar framework

D. Dockerize python-script, REST API service and Neo4j / ElasticSearch with docker-compose


## Usage

Neo4j (Community Version) 4.1.3
ElasticSearch 7.9.3

Python 3.6.8
py2neo 2020.0.0