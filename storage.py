# -*- coding: utf-8 -*-

"""
Storage module to initiate connection to database
and to store data from CSV-file to Neo4j-database.
"""

# Standard libraries imports
import logging
import sys
import os
import time
import csv
from functools import wraps
from pathlib import Path

# Additional libraries imports
from py2neo import Graph

# Modules imports
from models import Organization, Person
import search

# Constants
ON_EXCEPTION_RETRY_COUNT = 5

# Headers' names
HEADER_GROUP_ID = 'group_id'
HEADER_GROUP = 'group'
HEADER_ID = 'id'
HEADER_NAME = 'name'
HEADER_SORT_NAME = 'sort_name'
HEADER_EMAIL = 'email'
VALUE_NATIONALITY = 'GB (Great Britain)'

# Environments
NEO4J_URI_FILE = 'NEO4J_URI_FILE'
NEO4J_USER_FILE = 'NEO4J_USER_FILE'
NEO4J_PASSWORD_FILE = 'NEO4J_PASSWORD_FILE'

# Neo4j's graph object
__graph = None


def storage_decorator(func):
	"""
	Initiate graph and provide graph object to function.
	"""
	@wraps(func)
	def wrapper(*args, **kwds):
		global __graph
		retry_index = 0
		while retry_index < ON_EXCEPTION_RETRY_COUNT:
			try:
					# Check envoronment
					neo4j_uri_file = os.environ.get(NEO4J_URI_FILE)
					neo4j_user_file = os.environ.get(NEO4J_USER_FILE)
					neo4j_password_file = os.environ.get(NEO4J_PASSWORD_FILE)
					if neo4j_uri_file is None or neo4j_user_file is None \
							or neo4j_password_file is None:
						raise ValueError(''
							'Neo4j-graph initialization error, ' +
							'please, verify OS environments: %s, %s, %s' %
							(NEO4J_URI_FILE, NEO4J_USER_FILE, NEO4J_PASSWORD_FILE)
						)
						# Initiate
						__graph = Graph(
							Path(neo4j_uri_file).read_text().strip(),
							user=Path(neo4j_user_file).read_text().strip(),
							password=Path(neo4j_password_file).read_text().strip()
						)
					return func(graph=__graph, *args, **kwds)
			except Exception as exc:
				logging.error(getattr(exc, 'message', repr(exc)))
				time.sleep(5)
				retry_index += 1
	return wrapper


@storage_decorator
def get_graph(graph: Graph) -> Graph:
	"""
	Graph object getter.
	"""
	return graph


@storage_decorator
def read_and_store_data(graph: Graph, csv_file) -> None:
	"""
	Read data from CSV-file (uploaded) and store it to Neo4j-database.
	"""		
	# Initialize variables
	people_list = []
	membership_list = []
	headers = {}
	index = 0
	is_first_row = True
	# Iterate over file data
	for data in csv.reader(csv_file):
		if is_first_row: # Initialize headers' indexes
			for key in data:
				headers[key] = index
				index += 1
			is_first_row = False
		else: # Store data				
			# Store organization
			organization_group_id = data[headers[HEADER_GROUP_ID]]
			organization_name = data[headers[HEADER_GROUP]]
			organization = Organization(
				organization_group_id, organization_name
			)	
			graph.push(organization)
			# Load membership index
			membership_list += [
				search.make_organization_data(organization)
			]
			if len(membership_list) > 100:
				search.load_index(
					search.ALIAS_MEMBERSHIP, membership_list)
				membership_list = []
			# Store person
			person_id = data[headers[HEADER_ID]]
			person_name = data[headers[HEADER_NAME]]
			person_alias = data[headers[HEADER_SORT_NAME]]
			person_email = data[headers[HEADER_EMAIL]]
			person = Person(
				person_id, person_name, person_alias, person_email,
				VALUE_NATIONALITY, organization
			)
			graph.push(person)
			# Load people index
			people_list += [
				search.make_person_data(person)
			]
			if len(people_list) > 100:
				search.load_index(
					search.ALIAS_PEOPLE, people_list)
				people_list = []
		# Load indexes
		if len(membership_list) > 0:
			search.load_index(search.ALIAS_MEMBERSHIP, membership_list)
		if len(people_list) > 0:
			search.load_index(search.ALIAS_PEOPLE, people_list)

