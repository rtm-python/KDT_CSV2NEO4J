# -*- coding: utf-8 -*-

'''
Main module to run application
'''

# standard libraries imports
import os, sys

# additional libraries imports
from py2neo import Graph

# modules imports
from models import Organization, Person

# connect to Neo4j-database
NEO4J_DATABASE = 'NEO4J_DATABASE'
NEO4J_USER = 'NEO4J_USER'
NEO4J_PASSWORD = 'NEO4J_PASSWORD'

# try to connect
try:
	graph = Graph(
		os.environ.get(NEO4J_DATABASE),
		user= os.environ.get(NEO4J_USER),
		password=os.environ.get(NEO4J_PASSWORD)
	)
except Exception as exc:
	print(getattr(exc, 'message', repr(exc)))
	print(
		'Neo4j-database connection error, ' +
		'verify os environments: %s, %s, %s' %
		(NEO4J_DATABASE, NEO4J_USER, NEO4J_PASSWORD)
	)
	sys.exit(0)


if __name__ == '__main__':
	print(
		'Organization: %d\r\nPerson      : %d' %
		(len(Organization.match(graph)), len(Person.match(graph)))
	)
