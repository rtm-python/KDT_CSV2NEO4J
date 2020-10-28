# -*- coding: utf-8 -*-

'''
Service module with implementation of:
- reading data from CSV-file and storing it to Neo4j-database;
- handling REST requests to access data stored in Neo4j-database.
'''

# standard libraries imports
import os, sys
import csv
import logging

# additional libraries imports
from py2neo import Graph

# modules imports
from models import Organization, Person

# headers' names
HEADER_GROUP_ID = 'group_id'
HEADER_GROUP = 'group'
HEADER_ID = 'id'
HEADER_NAME = 'name'
HEADER_SORT_NAME = 'sort_name'
HEADER_EMAIL = 'email'
VALUE_NATIONALITY = 'GB (Great Britain)'

# connect to Neo4j-database
NEO4J_DATABASE = 'NEO4J_DATABASE'
NEO4J_USER = 'NEO4J_USER'
NEO4J_PASSWORD = 'NEO4J_PASSWORD'

# try to connect
graph = None
try:
	graph = Graph(
		os.environ.get(NEO4J_DATABASE),
		user=os.environ.get(NEO4J_USER),
		password=os.environ.get(NEO4J_PASSWORD)
	)
except Exception as exc:
	logging.error(getattr(exc, 'message', repr(exc)))
	logging.warning(
		'Neo4j-database connection error, ' +
		'verify OS environments: %s, %s, %s' %
		(NEO4J_DATABASE, NEO4J_USER, NEO4J_PASSWORD)
	)
	sys.exit(0)


def read_and_store_data(filepath: str) -> None:
	'''
	Read data from CSV-file (filepath) and store it to Neo4j-database. 
	'''
	logging.info('Handle CSV-file on path %s' % filepath)
	with open(filepath) as csv_file:
		headers = {}
		index = 0
		is_first_row = True
		for data in csv.reader(csv_file):
			if is_first_row: # initiate headers' indexes
				for key in data:
					headers[key] = index
					index += 1
				is_first_row = False
			else: # store data
				# store organization
				organization_group_id = data[headers[HEADER_GROUP_ID]]
				organization_name = data[headers[HEADER_GROUP]]
				organization = Organization(
					organization_group_id, organization_name
				)	
				graph.push(organization)
				# store person
				person_id = data[headers[HEADER_ID]]
				person_name = data[headers[HEADER_NAME]]
				person_alias = data[headers[HEADER_SORT_NAME]]
				person_email = data[headers[HEADER_EMAIL]]
				person = Person(
					person_id, person_name, person_alias, person_email,
					VALUE_NATIONALITY, organization
				)
				graph.push(person)
