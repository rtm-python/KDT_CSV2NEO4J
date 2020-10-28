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

# cypher matching expressions
MATCH_PERSONS_WITH_ORGANIZATION_EXPRESSION = \
	'MATCH (Person)-[MEMBERSHIP]->(Organization) ' + \
	'RETURN Person, Organization ORDER BY Person.name SKIP %d LIMIT %d'
MATCH_PERSON_WITH_ORGANIZATION_EXPRESSION = \
	'MATCH (Person)-[MEMBERSHIP]->(Organization) ' + \
	'WHERE Person.id = "%s" RETURN Person, Organization'


class OrganizationData(BaseModel):
	'''
	This is an OrganizationData class to retreive request data.
	Variables: group_id, name.
	'''
	group_id: str
	name: str


class PersonData(BaseModel):
	'''
	This is an PersonData class to retreive request data.
	Variables: id, name, alias, email, nationality, organization_group_id.
	'''
	id: str
	name: str
	alias: str
	email: str
	nationality: str
	organization_group_id: str


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
	node_matcher = NodeMatcher(graph)
	return {
		'name': 'KDT_CSV2NEO4J',
		'organizations': len(node_matcher.match('Organization')),
		'persons': len(node_matcher.match('Person'))
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
	page_count = int(page_count) + 1 \
		if int(page_count) < page_count else int(page_count)
	if page_index < 1 or page_index > page_count:
		raise HTTPException(status_code=400, detail="Page index error")
	if per_page < 1:
		raise HTTPException(status_code=400, detail="Per page error")
	return {
		'total': total,
		'page_count': page_count,
		'page_index': page_index,
		'per_page': per_page,
		'organizations': list(
			node_matcher.match('Organization').order_by('_.name').\
				skip((page_index - 1) * per_page).limit(per_page)
		)
	}
		

@app.get("/api/organization/{organization_group_id}/")
def read_organization(organization_group_id: str):
	'''
	Return organization data by organization_id.
	'''
	organization = Organization.match(graph, organization_group_id).first()
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
	organization = Organization(
		organization_data.group_id, organization_data.name)
	graph.push(organization)
	return {
		'status': 'created',
		'group_id': organization.group_id,
		'name': organization.name
	}


@app.put("/api/organization/{organization_group_id}/")
def update_organization(organization_group_id: str,
						organization_data: OrganizationData):
	'''
	Update organization by organization_id and return result status.
	'''
	organization = Organization.match(graph, organization_group_id).first()
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


@app.delete("/api/organization/{organization_group_id}/")
def delete_organization(organization_group_id: str):
	'''
	Delete organization by organization_id and return result status.
	'''
	organization = Organization.match(graph, organization_group_id).first()
	if organization is None:
		raise HTTPException(status_code=404, detail="Organization not found")
	result = {
		'status': 'deleted',
		'group_id': organization.group_id,
		'name': organization.name
	}
	graph.delete(organization)
	return result


@app.get("/api/persons/")
def read_person_list(page_index: int = 1, per_page: int = 10):
	'''
	Return person's data list.
	Request arguments: page_index, per_page
	'''
	node_matcher = NodeMatcher(graph)
	total = len(node_matcher.match('Person'))
	page_count = total / per_page
	page_count = int(page_count) + 1 \
		if int(page_count) < page_count else int(page_count)
	if page_index < 1 or page_index > page_count:
		raise HTTPException(status_code=400, detail="Page index error")
	if per_page < 1:
		raise HTTPException(status_code=400, detail="Per page error")
	expression = MATCH_PERSONS_WITH_ORGANIZATION_EXPRESSION % \
		((page_index - 1) * per_page, per_page)
	return {
		'total': total,
		'page_count': page_count,
		'page_index': page_index,
		'per_page': per_page,
		'persons': [
			{
				'id': person.get('id'),
				'name': person.get('name'),
				'alias': person.get('alias'),
				'email': person.get('email'),
				'nationality': person.get('nationality'),
				'organization': {
					'group_id': organization.get('group_id'),
					'name': organization.get('name')
				}
			} for person, organization in graph.run(expression)
		]
	}
	

@app.get("/api/person/{person_id}/")
def read_person(person_id: str):
	'''
	Return person data by person_id.
	'''
	expression = MATCH_PERSON_WITH_ORGANIZATION_EXPRESSION % person_id
	data = graph.run(expression).data()
	if len(data) == 0:
		raise HTTPException(status_code=404, detail="Person not found")
	data = data[0]
	person = data.get('Person')
	organization = data.get('Organization')
	return {
		'id': person.get('id'),
		'name': person.get('name'),
		'alias': person.get('alias'),
		'email': person.get('email'),
		'nationality': person.get('nationality'),
		'organization': {
			'group_id': organization.get('group_id'),
			'name': organization.get('name')
		}
	}


@app.post("/api/person/")
def create_person(person_data: PersonData):
	'''
	Create new person and return result info.
	'''
	organization = Organization.match(
		graph, person_data.organization_group_id).first()
	person = Person(
		person_data.id, person_data.name, person_data.alias,
		person_data.email, person_data.nationality,
		organization
	)
	graph.push(person)
	return {
		'status': 'created',
		'id': person.id,
		'name': person.name,
		'alias': person.alias,
		'email': person.email,
		'nationality': person.nationality,
		'organization': {
			organization.group_id,
			organization.name
		}
	}


@app.put("/api/person/{person_id}/")
def update_person(person_id: str, person_data: PersonData):
	'''
	Update person by person_id and return result status.
	'''
	organization = Organization.match(
		graph, person_data.organization_group_id).first()
	if organization is None:
		raise HTTPException(status_code=404, detail="Organization not found")
	person = Person.match(graph, person_id).first()
	if person is None:
		raise HTTPException(status_code=404, detail="Person not found")
	person.id = person_data.id
	person.name = person_data.name
	person.alias = person_data.alias
	person.email = person_data.email
	person.nationality = person_data.nationality
	person.organization = organization
	graph.push(person)
	return {
		'status': 'updated',
		'id': person.id,
		'name': person.name,
		'alias': person.alias,
		'email': person.email,
		'nationality': person.nationality,
		'organization': {
			organization.group_id,
			organization.name
		}
	}


@app.delete("/api/person/{person_id}/")
def delete_person(person_id: str):
	'''
	Delete person by person_id and return result status.
	'''
	person = Person.match(graph, person_id).first()
	if person is None:
		raise HTTPException(status_code=404, detail="Person not found")
	result = {
		'status': 'deleted',
		'id': person.id,
		'name': person.name,
		'alias': person.alias,
		'email': person.email,
		'nationality': person.nationality,
		'organization': [
			{
				'group_id': related_to.group_id,
				'name': related_to.name
			} for related_to in person.membership
		][0]
	}
	graph.delete(person)
	return result
