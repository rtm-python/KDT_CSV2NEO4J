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
		if group_id is None or name is None:
			raise ValueError('Value of group_id and name could not be None')
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
		if id is None or name is None or alias is None or email is None or \
				nationality is None or organization is None:
			raise ValueError(
				'Value of id, namem aliasm email, nationality ' +
				'and organization could not be None'
			)
		self.id = id
		self.name = name
		self.alias = alias
		self.email = email
		self.nationality = nationality
		self.membership.add(organization)
