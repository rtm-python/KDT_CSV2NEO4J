# -*- coding: utf-8 -*-

'''
Main module to run application
'''

# standard libraries imports
import os, sys
import logging

# additional libraries imports
from py2neo import Graph
from fastapi import FastAPI

# initalize basics ------------
LOGGING_LEVEL = 'LOGGING_LEVEL'

# initialize logging
logging.basicConfig(level=os.environ.get(LOGGING_LEVEL))

# connect to Neo4j-database -----
NEO4J_DATABASE = 'NEO4J_DATABASE'
NEO4J_USER = 'NEO4J_USER'
NEO4J_PASSWORD = 'NEO4J_PASSWORD'

# try to connect
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

# iniitalize application
app = FastAPI()

# module imports (preventing circular)
import service

# read and store data -------
CSV_FILEPATH = 'CSV_FILEPATH'

# try preload CSV-file
if os.environ.get(CSV_FILEPATH) is not None:
	if os.path.isfile(os.environ.get(CSV_FILEPATH)):
		service.read_and_store_data(os.environ.get(CSV_FILEPATH))
