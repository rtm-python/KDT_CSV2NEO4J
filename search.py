# -*- coding: utf-8 -*-

"""
Search module to create index from Neo4j-database in ElsaticSearch.
"""

# standard libraries imports
import logging, sys

# additional libraries imports
from elasticsearch import Elasticsearch

# module imports
from models import Person, Organization

# aliases
ALIAS_MEMBERSHIP = 'MEMBERSHIP'
ALIAS_PEOPLE = 'PEOPLE'

# intialize ElasticSearch
es = Elasticsearch(http_compress=True)


def make_organization_data(organization: Organization) -> dict:
	"""
	Make index data from Organization-entity.
	"""
	return {

	}


def make_person_data(person: Person) -> dict:
	"""
	Make index data from Person-entity.
	"""
	return {

	}


def load_index(alias: str, data_list: [dict]) -> None:
	"""
	Bulk load data to alias-index. 
	"""
	pass


def insert_index(alias: str, data: dict) -> None:
	"""
	Insert data to alias-index.
	"""
	pass


def delete_index(alias: str, data: dict) -> None:
	"""
	Delete data from alias-index.
	"""
	pass


def search(alias: str, body: dict) -> list:
	"""
	Search by body in alias-index.
	"""
	pass


if __name__ == '__main__':
	logging.info(
		search(
			sys.argv[1] if len(sys.argv) > 1 else ALIAS_PEOPLE,
			{

			}
		)
	)
