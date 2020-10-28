# -*- coding: utf-8 -*-

'''
Models module for next entities:
Person
Organization
'''

# additional libraries imports
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom


class Organization(GraphObject):
	'''
	This is an Organization class.
	Properties: group_id and name.
	Relationships: members.
	'''
	__primarykey__ = "group_id"

	group_id = Property()
	name = Property()

	members = RelatedFrom("Person", "MEMBERSHIP")

	def __init__(self, group_id: int, name: str) -> 'Organization':
		'''
		Initialize object with properties:
		group_id, name.
		'''
		self.group_id = group_id
		self.name = name


class Person(GraphObject):
	'''
	This is a Person class.
	Properties: id, name, alias, email, nationality.
	Relationships: membership.
	'''
	__primarykey__ = "id"

	id = Property()
	name = Property()
	alias = Property()
	email = Property()
	nationality = Property()

	membership = RelatedTo(Organization)

	def __init__(self, id: int, name: str, alias: str, email: str,
				 nationality: str, organization: Organization) -> 'Person':
		'''
		Initialize object
		with properties (id, name, alias, email and nationality)
		and relationship (membership).
		'''
		self.id = id
		self.name = name
		self.alias = alias
		self.email = email
		self.nationality = nationality
		self.membership.add(organization)
