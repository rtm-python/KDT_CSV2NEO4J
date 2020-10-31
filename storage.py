# -*- coding: utf-8 -*-

"""
Storage module to initiate connection to database
and to store data from CSV-file to Neo4j-database.
"""

# standard libraries imports
import os, sys
import logging
import csv
from pathlib import Path

# additional libraries imports
from py2neo import Graph

# modules imports
from models import Organization, Person
import search

# headers' names
HEADER_GROUP_ID = 'group_id'
HEADER_GROUP = 'group'
HEADER_ID = 'id'
HEADER_NAME = 'name'
HEADER_SORT_NAME = 'sort_name'
HEADER_EMAIL = 'email'
VALUE_NATIONALITY = 'GB (Great Britain)'

# connect to Neo4j-database -----
NEO4J_DATABASE_FILE = 'NEO4J_DATABASE_FILE'
NEO4J_USER_FILE = 'NEO4J_USER_FILE'
NEO4J_PASSWORD_FILE = 'NEO4J_PASSWORD_FILE'

# try to connect
try:
	graph = Graph(
		Path(os.environ.get(NEO4J_DATABASE_FILE)).read_text(),
		user=Path(os.environ.get(NEO4J_USER_FILE)).read_text(),
		password=Path(os.environ.get(NEO4J_PASSWORD_FILE)).read_text()
	)
except Exception as exc:
	logging.error(getattr(exc, 'message', repr(exc)))
	logging.warning(
		'Neo4j-database connection error, ' +
		'verify OS environments: %s, %s, %s' %
		(NEO4J_DATABASE_FILE, NEO4J_USER_FILE, NEO4J_PASSWORD_FILE)
	)
	sys.exit(0)


def read_and_store_data(filepath: str) -> None:
	"""
	Read data from CSV-file (filepath) and store it to Neo4j-database. 
	"""
	logging.info('Handle CSV-file on path %s' % filepath)
	with open(filepath) as csv_file:
		
		# initialize variables
		people_list = []
		membership_list = []
		headers = {}
		index = 0
		is_first_row = True

		# iterate over file data
		for data in csv.reader(csv_file):
		
			if is_first_row: # initialize headers' indexes
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
				
				# load membership index
				membership_list += [
					search.make_organization_data(organization)
				]
				if len(membership_list) > 100:
					search.load_index(
						search.ALIAS_MEMBERSHIP, membership_list)
					membership_list = []
		
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

				# load people index
				people_list += [
					search.make_person_data(person)
				]
				if len(people_list) > 100:
					search.load_index(
						search.ALIAS_PEOPLE, people_list)
					people_list = []

		# load indexes
		if len(membership_list) > 0:
			search.load_index(search.ALIAS_MEMBERSHIP, membership_list)
		if len(people_list) > 0:
			search.load_index(search.ALIAS_PEOPLE, people_list)
