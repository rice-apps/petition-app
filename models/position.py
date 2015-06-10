"""
Model definition and functions for positions.
"""

__author__ = 'Roshni Kaushik <rsk8@rice.edu>'

from google.appengine.ext import db
from user import User
from datetime import date, timedelta


class Position(db.Model):
    user = db.ReferenceProperty(User, required=True)
    title = db.StringProperty(required=True)
    date_added = db.DateProperty(auto_now=True)
    organization = db.StringProperty(required=True)
    election = db.StringProperty(required=True)

    def to_json(self):
        return {'user': self.user, 'title': self.title, 'id': str(self.key()), 'organization': self.organization,
                'election': self.election}
       
    def get_organization(self):
        return self.organization

    def get_election(self):
        return self.election

    def get_title(self):
        return self.title


def get_position(key):
    return Position.get(key)


def get_positions_for_election(election_name):
    result = []
    while election_name.endswith(" "):
        election_name = election_name[:-1]

    query = Position.gql('WHERE election = :1', election_name)
    for position in query:
        result.append(position.to_json())
    return result


def create_position(user, position):
    election = position['election'].split('-')[0][0:-1]
    while election.endswith(" "):
        election = election[:-1]

    existing = get_positions_for_election(election)
    name_list = []
    for existing_position in existing:
        name_list.append(existing_position["title"])

    if position['title'] not in name_list or not existing:
        position = Position(user=user, title=position['title'], election=election,
                            organization=position['organization'])
        position.put()
        return position
    else:
        return None


def delete_position(position):
    # Refactored into this method in case there are other things to be done
    # before deleting a position
    position.delete()
