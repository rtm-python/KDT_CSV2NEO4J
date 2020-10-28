# -*- coding: utf-8 -*-

'''
Service module with implementation of reading data
from CSV-file and storing it to Neo4j-database;
'''

# standard libraries imports
import csv
import logging

# modules imports
from run import graph, app
from models import Organization, Person

# headers' names
HEADER_GROUP_ID = 'group_id'
HEADER_GROUP = 'group'
HEADER_ID = 'id'
HEADER_NAME = 'name'
HEADER_SORT_NAME = 'sort_name'
HEADER_EMAIL = 'email'
VALUE_NATIONALITY = 'GB (Great Britain)'


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


def statistics() -> str:
	'''
	Return statistics for database.
	'''
	return {'Organization': 0, 'Person': 0}


@app.get("/")
def home():
	'''
	Return home page data.
	'''
    return {'name': 'KDT_CSV2NEO4J'}

