# -*- coding: utf-8 -*-

"""
Main module to run application
"""

# standard libraries imports
import os
import logging

# initalize basics ------------
LOGGING_LEVEL = 'LOGGING_LEVEL'

# initialize logging
logging.basicConfig(level=os.environ.get(LOGGING_LEVEL))

# module imports
import storage
import service

app = service.app

# read and store data -------
CSV_FILEPATH = 'CSV_FILEPATH'

# try preload CSV-file
if os.environ.get(CSV_FILEPATH) is not None:
	if os.path.isfile(os.environ.get(CSV_FILEPATH)):
		storage.read_and_store_data(os.environ.get(CSV_FILEPATH))
