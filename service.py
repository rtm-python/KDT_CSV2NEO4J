# -*- coding: utf-8 -*-

'''
Service module with implementation of reading data
from CSV-file and storing it to Neo4j-database;
'''

# standard libraries imports
import csv
import logging

# additional libraries imports
from typing import Optional
from pydantic import BaseModel
from py2neo import NodeMatcher
from fastapi import HTTPException

# modules imports
from run import graph, app
from models import Organization, Person

# headers' names
HEADER_GROUP_ID = 'group_id'
HEADER_GROUP = 'group'
HEADER_ID = 'id'
HEADER_NAME = 'name'
HEADER_SORT_NAME = 'sort_name'
HEADER_EMAIL = 'email'
VALUE_NATIONALITY = 'GB (Great Britain)'


class OrganizationData(BaseModel):
	'''
	This is an OrganizationData class to retreive request data.
	Variables: group_id, name.
	'''
	group_id: str
	name: str


def read_and_store_data(filepath: str) -> None:
	'''
	Read data from CSV-file (filepath) and store it to Neo4j-database. 
	'''
	logging.info('Handle CSV-file on path %s' % filepath)
	with open(filepath) as csv_file:
		headers = {}
		index = 0
		is_first_row = True
		for data in csv.reader(csv_file):
			if is_first_row: # initiate headers' indexes
				for key in data:
					headers[key] = index
					index += 1
				is_first_row = False
			else: # store data
				# store organization
				organization_group_id = data[headers[HEADER_GROUP_ID]]
				organization_name = data[headers[HEADER_GROUP]]
				organization = Organization(
					organization_group_id, organization_name
				)	
				graph.push(organization)
				# store person
				person_id = data[headers[HEADER_ID]]
				person_name = data[headers[HEADER_NAME]]
				person_alias = data[headers[HEADER_SORT_NAME]]
				person_email = data[headers[HEADER_EMAIL]]
				person = Person(
					person_id, person_name, person_alias, person_email,
					VALUE_NATIONALITY, organization
				)
				graph.push(person)


@app.get("/")
def read_statistics():
	'''
	Return statistics data.
	'''
	return {
		'name': 'KDT_CSV2NEO4J',
		'organizations': 0,
		'persons': 0
	}


@app.get("/api/organizations/")
def read_organization_list(page_index: int = 1, per_page: int = 10):
	'''
	Return organization's data list.
	Request arguments: page_index, per_page
	'''
	node_matcher = NodeMatcher(graph)
	total = len(node_matcher.match('Organization'))
	page_count = total / per_page
	page_count = int(page_count) + 1 if int(page_count) < page_count else int(page_count)
	if page_index < 1 or page_index > page_count:
		raise HTTPException(status_code=400, detail="Page index error")
	if per_page < 1:
		raise HTTPException(status_code=400, detail="Per page error")
	return {
		'total': total,
		'page_count': page_count,
		'page_index': page_index,
		'per_page': per_page,
		'organizations': list(node_matcher.match('Organization').order_by('_.name').skip((page_index - 1) * per_page).limit(per_page))
	}
		

@app.get("/api/organization/{organization_id}/")
def read_organization(organization_id: str):
	'''
	Return organization data by organization_id.
	'''
	organization = Organization.match(graph, organization_id).first()
	if organization is None:
		raise HTTPException(status_code=404, detail="Organization not found")
	return {
		'group_id': organization.group_id,
		'name': organization.name
	}


@app.post("/api/organization/")
def create_organization(organization_data: OrganizationData):
	'''
	Create new organization and return result info.
	'''
	organization = Organization(organization_data.group_id, organization_data.name)
	graph.push(organization)
	return {
		'status': 'created',
		'group_id': organization.group_id,
		'name': organization.name
	}


@app.put("/api/organization/{organization_id}/")
def update_organization(organization_id: str, organization_data: OrganizationData):
	'''
	Update organization by organization_id and return result status.
	'''
	organization = Organization.match(graph, organization_id).first()
	if organization is None:
		raise HTTPException(status_code=404, detail="Organization not found")
	organization.group_id = organization_data.group_id
	organization.name = organization_data.name
	graph.push(organization)
	return {
		'status': 'updated',
		'group_id': organization.group_id,
		'name': organization.name
	}


@app.delete("/api/organization/{organization_id}/")
def delete_organization(organization_id: str):
	'''
	Delete organization by organization_id and return result status.
	'''
	organization = Organization.match(graph, organization_id).first()
	if organization is None:
		raise HTTPException(status_code=404, detail="Organization not found")
	graph.delete(organization)
	return {
		'status': 'deleted',
		'group_id': organization.group_id,
		'name': organization.name
	}


@app.get("/api/persons/")
def read_person_list():
	'''
	Return person's data list.
	'''
	return {
		'total': 0,
		'page_count': 0,
		'page_index': 0,
		'per_page': 0,
		'persons': list([])
	}


@app.get("/api/person/{person_id}/")
def read_person(person_id: int):
	'''
	Return person data by person_id.
	'''
	return {
		'name': 'KDT_CSV2NEO4J'
	}


@app.post("/api/person/")
def create_person():
	'''
	Create new person and return result info.
	'''
	return {'name': 'KDT_CSV2NEO4J'}


@app.put("/api/person/{person_id}/")
def update_person():
	'''
	Update person by person_id and return result status.
	'''
	return {'name': 'KDT_CSV2NEO4J'}


@app.delete("/api/person/{person_id}/")
def delete_person():
	'''
	Delete person and return result status.
	'''
	return {'name': 'KDT_CSV2NEO4J'}

