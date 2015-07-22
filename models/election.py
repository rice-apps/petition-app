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
    start_date = db.DateProperty(required=True)
    end_date = db.DateProperty(required=True)
    organization = db.StringProperty(required=True)
    positions = db.ListProperty(str)

    def to_json(self):
        return {'user': self.user.get_id(), 'title': self.title, 'id': str(self.key()),
                'organization': self.organization, 'start_date': self.start_date, 'end_date': self.end_date,
                'positions': self.positions}

    def get_organization(self):
        return self.organization

    def get_title(self):
        return self.title

    def get_positions(self):
        return self.positions


def get_election(key):
    return Election.get(key)


def get_non_expired_elections():
    result = []
    query = Election.gql('WHERE end_date >= :1', date.today())
    for election in query:
        result.append(election.to_json())
    return result


def get_ongoing_elections():
    result = []
    query = Election.gql('WHERE end_date >= :1', date.today())
    for election in query:
        if election.start_date <= date.today():
            result.append(election.to_json())
    return result


def create_election(user, election):
    existing = get_non_expired_elections()
    name_list = []
    for existing_election in existing:
        if existing_election['organization'] == election['organization_id']:
            name_list.append(existing_election['title'])

    start_date = convert_to_date(election['start_date'])
    end_date = convert_to_date(election['end_date'])

    if election['title'] not in name_list or not existing:
        election = Election(
            user=user,
            title=election['title'],
            start_date=start_date,
            end_date=end_date,
            organization=election['organization_id'],
            positions=election['positions'])
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


def get_organization_elections(organization_id):
    result = []
    # Ongoing and Upcoming Elections
    query = Election.gql('WHERE end_date >= :1', date.today())
    for election in query:
        if election.organization == organization_id:
            result.append(election.to_json())
    return result
