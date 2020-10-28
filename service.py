# -*- coding: utf-8 -*-

'''
Service module with implementation of:
- reading data from CSV-file and storing it to Neo4j-database;
- handling REST requests to access data stored in Neo4j-database.
'''

# modules imports
from models import Organization, Person


def read_and_store_data(filepath: str) -> None:
	'''
	Read data from CSV-file (filepath) and store it to Neo4j-database. 
	'''
	pass
