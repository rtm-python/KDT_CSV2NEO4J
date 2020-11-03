# -*- coding: utf-8 -*-

"""
Main module to run application
"""

# Standard libraries imports
import os
import logging

# Initalize basics ------------
LOGGING_LEVEL = 'LOGGING_LEVEL'

# Initialize logging
logging.basicConfig(level=os.environ.get(LOGGING_LEVEL))

# Module imports
import storage
import service

app = service.app

