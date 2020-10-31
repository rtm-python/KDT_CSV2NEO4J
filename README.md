# KDT_CSV2NEO4J
_Store data from CSV-file to Neo4j-database (interview test)_


## Specification

A. Implement python-script, which handles data from CSV-file to store it in Neo4j-database. Follow next matching rules for Person and Organization entities:
* id -> Person.id (unique)
* name  -> Person.name
* sort_name -> Person.alias
* email -> Person.email
* 'GB (Great Britain)' -> Person.nationality
* id -> Person.membership_in
* group_id -> Organization.group_id (unique)
* group -> Organization.name
* group_id -> Organization.members

B. Integrate ElasticSearch with Neo4j-database for fulltext searching

C. Implement base REST API service for data stored in Neo4j-database with Flask or similar framework

D. Dockerize python-script, REST API service and Neo4j / ElasticSearch with docker-compose


## Implementation

### A. Implemented in modules: run.py, storage.py and models.py 

It is recomended to run python script in virtual environment:
```
$ python -m venv <path_to_venv>
$ . <path_to_venv>/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

Should be defined several variables in OS environment before run script: 
```
$ export LOGGING_LEVEL=<LEVEL NAME>
$ export NEO4J_DATABASE=<NEO4J DATABASE URI>
$ export NEO4J_USER=<NEO4J USERNAME>
$ export NEO4J_PASSWORD=<NEO4J PASSWORD>
$ export CSV_FILEPATH=<PATH TO CSV FILE>
```

Next run script to store data from CSV-file to Neo4j-database:
```
(venv) $ python run.py
```

Resulted database could be viewed in Neo4j-browser:
```
http://localhost:7474/browser/
```

There are two expressions to see data below: 
```
neo4j$ MATCH (Person)-[MEMBERSHIP]->(Organization) RETURN Person, Organization
neo4j$ CALL db.schema.visualization()
```

### B. Implemented with elasticsearch-py in modules: search, storage and service

It is simple functions to bulk load, item insertion and deletion, which called each time on data manipulation. As a result it is possible to see created indexes:
```
$ curl -X GET "localhost:9200/_cat/indices?v" -H 'Content-Type: application/json'
```

And make sample search:
```
(venv) $ python search.py <index> <simple_query_string>
```

### C. Implemented with FastAPI in modules: run.py and service.py

Running is the same as in the A implementation, but now should be used uvicorn:
```
(venv) $ uvicorn run:app
```

Resulted REST API accessible with SwaggerUI in browser:
```
http://localhost:8000/docs/
```

### D. Implemented with docker-compose [KDT_DOCKERIZE](https://github.com/rtm-python/KDT_DOCKERIZE)



## Usage

* [Neo4j (Community Version) 4.1.3](https://neo4j.com/docs/operations-manual/current/installation/linux/rpm/#linux-rpm-install-standard)
* [ElasticSearch 7.9.3](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/rpm.html)
* [Python 3.6.8](https://centos.pkgs.org/8/okey-x86_64/python36-3.6.8-2.el8.x86_64.rpm.html)
* [py2neo 2020.0.0](https://py2neo.org/2020.0/)
* [FastAPI o.61.1](https://github.com/tiangolo/fastapi)
* [Uvicorn 0.12.2](http://www.uvicorn.org/#quickstart)
* [Python ElasticSearch Client 7.9.1](https://elasticsearch-py.readthedocs.io/en/7.9.1/index.html)
