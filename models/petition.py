"""
Model definition and functions for petitions.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

from google.appengine.ext import db
from user import User

class Petition(db.Model):
    user = db.ReferenceProperty(User, required=True)
    time_added = db.DateTimeProperty(auto_now=True)
    title = db.StringProperty(required=True)
    note = db.TextProperty()
    votes = db.IntegerProperty(default = 0)
    voters = db.ListProperty(str)

    def to_json():
        return {
            'id': str(self.key()),
            'title': self.title,
            'note': self.note,
            'votes': self.votes
        }

    def get_voters():
        return self.voters

    def add_voter(voter):
        net_id = voter.get_id()
        if net_id not in self.voters:
            voters.append(net_id)
            self.votes = self.votes + 1


def create_petition(user, petition):
    petition = Petition(
        user=user.key(),
        title=petition['title'],
        note=petition['note'])
    petition.put()
    return petition

def vote_petition(voter, petition):
    petition.add_voter(voter)

def get_petition(key):
    return Petition.get(key)

def get_all_petitions():
    return Petition.all()

def delete_petition(petition):
    # Refactored into this method incase there are other things to be done
    # before deleting a petition
    petition.delete()

def get_petitions(user):
    result = []
    query = Petition.gql('WHERE user = :1', user)
    for petition in query:
        result.append(petition.to_json)
    return result









