"""
Model definition and functions for petitions.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

from google.appengine.ext import db
from user import User
from datetime import date, timedelta

class Petition(db.Model):
    user = db.ReferenceProperty(User, required=True)
    date_added = db.DateProperty(auto_now=True)
    title = db.StringProperty(required=True)
    note = db.TextProperty()
    organizer_email = db.StringProperty(required=True)
    organizer_name = db.StringProperty(required=True)
    votes = db.IntegerProperty(default = 0)
    voters = db.ListProperty(str)

    def to_json(self):
        return {
            'user': self.user,
            'id': str(self.key()),
            'title': self.title,
            'note': self.note,
            'votes': self.votes,
            'organizer_email': self.organizer_email,
            'organizer_name': self.organizer_name
        }
    def get_votes(self):
        return self.votes

    def get_voters(self):
        return self.votes

    def get_user(self):
        return self.user

    def get_org_email(self):
        return self.organizer_email

    def get_org_name(self):
        return self.organizer_name

    def add_voter(self,voter):
        net_id = voter.get_id()
        if net_id not in self.voters:
            self.voters.append(net_id)
            self.votes = self.votes + 1
            self.put()
            return True
        else:
            return False

    def unvote(self, voter):
        net_id = voter.get_id()
        if net_id in self.voters:
            self.voters.remove(net_id)
            self.votes = self.votes - 1
            self.put()
            return True
        else:
            return False


def create_petition(user, petition):
    #existing = Petition.gql('WHERE title = :1', petition['title']).get()
    existing = get_petitions(user)
    name_list = []
    for petition in existing:
        name_list.append(petition['title'])
    if not existing or petition['title'] not in name_list:
        petition = Petition(
            user=user.key(),
            title=petition['title'],
            note=petition['note'],
            organizer_email=petition['org-email'],
            organizer_name=petition['org-name'])
        petition.put()
        return petition
    else:
        return existing

def vote_petition(voter, petition):
    return petition.add_voter(voter)

def unvote_petition(unvoter, petition):
    return petition.unvote(unvoter)

def get_petition(key):
    return Petition.get(key)


def get_in_effect_petitions():
    result = []
    query = Petition.gql('WHERE date_added >= :1', date.today() - timedelta(14))
    for petition in query:
        result.append(petition.to_json())
    return result

def get_expired_petitions():
    result = []
    query = Petition.gql('WHERE date_added < :1', date.today() - timedelta(14))
    for petition in query:
        result.append(petition.to_json())
    return result

def delete_petition(petition):
    # Refactored into this method incase there are other things to be done
    # before deleting a petition
    petition.delete()

def get_petitions(user):
    result = []
    query = Petition.gql('WHERE user = :1', user)
    for petition in query:
        result.append(petition.to_json())
    return result
