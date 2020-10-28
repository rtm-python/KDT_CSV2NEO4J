# -*- coding: utf-8 -*-

'''
Service module with implementation of:
- reading data from CSV-file and storing it to Neo4j-database;
- handling REST requests to access data stored in Neo4j-database.
'''

# standard libraries imports
import os
import logging

# modules imports
from models import Organization, Person


def read_and_store_data(filepath: str) -> None:
	'''
	Read data from CSV-file (filepath) and store it to Neo4j-database. 
	'''
	logging.info('Handle CSV-file on path %s' % filepath)
	
