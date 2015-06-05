"""
Model definition and functions for elections.
"""

__author__ = 'Roshni Kaushik <rsk8@rice.edu>'

from google.appengine.ext import db
from user import User
from datetime import date, timedelta

class Election(db.Model):
		user = db.ReferenceProperty(User, required=True)
		title = db.StringProperty(required=True)
		date_added = db.DateProperty(auto_now=True)
		date_expired = db.DateProperty()
		email = db.StringProperty(required=True)
		organization = db.StringProperty(required=True)
		def to_json(self):
			return {
				'user': self.user,
				'title': self.title,
				'id': str(self.key()),
				'email': self.email,
				'organization': self.organization,
				'date_expired': self.date_expired
				}
			 
		def get_organization(self):
			return self.organization
		def get_title(self):
			return self.title
    
def get_election(key):
    return Election.get(key)
    
def get_ongoing_elections():
    result = []
    query = Election.gql('WHERE date_expired > :1', date.today())
    for election in query:
        result.append(election.to_json()) 
    return result
    
def create_election(user, election):
	existing = get_ongoing_elections()
	name_list = []
	for existing_elections in existing:
		name_list.append(existing_elections["title"].replace(' ', ''))
	date_expired = convert_to_date(election['date_expired'])

	election_name = election['title']
	while election_name.endswith(" "): election_name = election_name[:-1]

	if election['title'].replace(' ', '') not in name_list or not existing:
		election = Election(
			user = user,
			title = election_name,
			email = election['email'],
			date_expired = date_expired,
			organization = election['organization'] )
		election.put()
		return election
	else:
		return None
 
def delete_election(election):
    # Refactored into this method in case there are other things to be done
    # before deleting a election
    election.delete() 
    
def convert_to_date(date1):
    list1 = date1.split('-')
    date2 = date(int(list1[0]), int(list1[1]), int(list1[2]))
    return date2