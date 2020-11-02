# -*- coding: utf-8 -*-

"""
Search module to create index from Neo4j-database in ElsaticSearch.
"""

# standard libraries imports
import logging, sys

# additional libraries imports
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# module imports
from models import Person, Organization

# aliases
ALIAS_MEMBERSHIP = 'membership'
ALIAS_PEOPLE = 'people'

# intialize ElasticSearch
ELASTIC_ENGINE_FILE = 'ELASTIC_ENGINE_FILE'
es = Elasticsearch(
	Path(os.environ.get(ELASTIC_SEARCH_FILE)).read_text().strip(),
	http_compress=True
)


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
	helpers.bulk(es, actions)
	es.indices.refresh(index=alias)


def insert_index(alias: str, data: dict) -> None:
	"""
	Insert data to alias-index.
	"""
	es.index(index=alias, id=data['id'], body=data['body'])
	es.indices.refresh(index=alias)


def delete_index(alias: str, data: dict) -> None:
	"""
	Delete data from alias-index.
	"""
	es.delete(index=alias, id=data['id'])
	es.indices.refresh(index=alias)


def search(alias: str, body: dict) -> list:
	"""
	Search by body in alias-index.
	"""
	pass


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
	result = es.search(index=index, body=body)
	print("Hits: %d" % result['hits']['total']['value'])
	for value in result['hits']['hits']:
		print(value)
