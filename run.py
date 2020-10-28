# -*- coding: utf-8 -*-

'''
Main module to run application
'''

# standard libraries imports
import os
import logging

# modules imports
from models import Organization, Person
import service

# initalize basics ------------
LOGGING_LEVEL = 'LOGGING_LEVEL'

# initialize logging
logging.basicConfig(level=os.environ.get(LOGGING_LEVEL))

# read and store data -------
CSV_FILEPATH = 'CSV_FILEPATH'

# try preload CSV-file
if os.environ.get(CSV_FILEPATH) is not None:
	if os.path.isfile(os.environ.get(CSV_FILEPATH)):
		service.read_and_store_data(os.environ.get(CSV_FILEPATH))


if __name__ == '__main__':
	logging.info(
		'Organization = %d, Person = %d' %
		(len(Organization.match(service.graph)), len(Person.match(service.graph)))
	)
