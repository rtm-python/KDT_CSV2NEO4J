# -*- coding: utf-8 -*-

"""
Search module to create index from Neo4j-database in ElsaticSearch.
"""

# Standard libraries imports
import logging
import sys
import os
import time
from functools import wraps
from pathlib import Path

# Additional libraries imports
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Module imports
from models import Person, Organization

# Constants
ON_EXCEPTION_RETRY_COUNT = 5

# Aliases
ALIAS_MEMBERSHIP = 'membership'
ALIAS_PEOPLE = 'people'

# Environments
ELASTIC_URI_FILE = 'ELASTIC_URI_FILE'

# ElasticSearch object
__es = None


def initiate_decorator(func):
	"""
	Initiate decorator.
	"""
	@wraps(func)
	def wrapper(*args, **kwds):
		global __es
		retry_index = 0
		while retry_index < ON_EXCEPTION_RETRY_COUNT:
			try:
				if __es is None:
					# check envoronment
					elastic_uri_file = os.environ.get(ELASTIC_URI_FILE)
					if elastic_uri_file is None:
						raise ValueError(''
							'ElasticSearch initialization error, ' +
							'please, verify OS environments: %s' %
							ELASTIC_URI_FILE 
						)
					# initiate
					__es = Elasticsearch(
						Path(elastic_uri_file).read_text().strip(),
						http_compress=True
					)
				return func(*args, **kwds)
			except Exception as exc:
				logging.error(getattr(exc, 'message', repr(exc)))
				time.sleep(5)
				retry_index += 1
	return wrapper


def make_organization_data(organization: Organization) -> dict:
	"""
	Make index data from Organization-entity.
	"""
	return {
		'id': organization.group_id,
		'body': {
			'name': organization.name
		}
	}


def make_person_data(person: Person) -> dict:
	"""
	Make index data from Person-entity.
	"""
	return {
		'id': person.id,
		'body': {
			'name': person.name,
			'alias': person.alias,
			'email': person.email,
			'nationality': person.nationality
		}
	}


@initiate_decorator
def load_index(alias: str, data_list: [dict]) -> None:
	"""
	Bulk load data to alias-index. 
	"""
	actions = [
		{
			'_index': alias,
			'_source': data
		} for data in data_list
	]
	helpers.bulk(__es, actions)
	__es.indices.refresh(index=alias)


@initiate_decorator
def insert_index(alias: str, data: dict) -> None:
	"""
	Insert data to alias-index.
	"""
	__es.index(index=alias, id=data['id'], body=data['body'])
	__es.indices.refresh(index=alias)


@initiate_decorator
def delete_index(alias: str, data: dict) -> None:
	"""
	Delete data from alias-index.
	"""
	__es.delete(index=alias, id=data['id'])
	__es.indices.refresh(index=alias)


@initiate_decorator
def search(alias: str, body: dict) -> list:
	"""
	Search by body in alias-index.
	"""
	return __es.search(index=allias, body=body)


if __name__ == '__main__':
	index = sys.argv[1] if len(sys.argv) > 1 else None
	if len(sys.argv) < 3:
		body = 	{
			'query': {
				'match_all': {

				}
			}
		}
	else:
		body = {
			'query': {
				'simple_query_string': {
					'query': sys.argv[2]
				}
			}
		}
	result = search(index, body)
	print("Hits: %d" % result['hits']['total']['value'])
	for value in result['hits']['hits']:
		print(value)

