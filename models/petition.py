"""
Model definition and functions for petitions.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

from google.appengine.ext import db
from user import User
from datetime import date, timedelta


class Petition(db.Model):
    
    user = db.ReferenceProperty(User, required=True)
    name = db.StringProperty(required=True)
    date_added = db.DateProperty(auto_now=True)
    email = db.StringProperty(required=True)
    message = db.TextProperty()
    election = db.StringProperty(required=True)
    organization = db.StringProperty(required=True)
    position = db.StringProperty(required=True)
    signature_num = db.IntegerProperty(default=0)
    signatures = db.ListProperty(str)
    
    def to_json(self):
        return {
            'user': self.user,
            'name': self.name,
            'id': str(self.key()),
            'email': self.email,
            'message': self.message,
            'election': self.election,
            'organization': self.organization,
            'position': self.position,
            'signature_num': self.signature_num,
            'signatures': self.signatures
            }

    def get_signature_num(self):
        return self.signature_num

    def get_signatures(self):
        return self.signatures

    def get_user(self):
        return self.user

    def get_election(self):
        return self.election

    def get_organization(self):
        return self.organization

    def get_position(self):
        return self.position
    
    def add_signature(self, signee):
        net_id = signee.get_id()
        if net_id not in self.signatures:
            self.signatures.append(net_id)
            self.signature_num += 1
            self.put()
            return True
        else:
            return False
          
    def remove_signature(self, signee):
        net_id = signee.get_id()
        if net_id in self.signatures:
            self.signatures.remove(net_id)
            self.signature_num -= 1
            self.put()
            return True
        else:
            return False


def create_petition(user, petition):
    existing = get_petitions(user)
    name_list = []
    election = petition['election'].split('-')[0][0:-1]
    for existing_petition in existing:
        name_list.append((existing_petition['user'].key(), existing_petition['election'],
                          existing_petition['organization'], existing_petition['position']))

    petition_tuple = (user.key(), election, petition['organization'], petition['position'])
    if petition_tuple not in name_list or not existing:
        petition = Petition(
            user=user,
            name=petition['name'],
            email=petition['email'],
            message=petition['message'],
            election=election,
            organization=petition['organization'],
            position=petition['position'])
        petition.put()
        return petition
    else:
        return None


def sign_petition(signee, petition):
    return petition.add_signature(signee)


def unsign_petition(unsignee, petition):
    return petition.remove_signature(unsignee)


def get_petition(key):
    return Petition.get(key)


def get_petitions_for_election(election):
    result = []
    query = Petition.gql('WHERE election = :1', election['title'])
    for petition in query:
        result.append(petition.to_json())
    return result


# def get_expired_petitions():
    # result = []
    # query = Petition.gql('WHERE date_added < :1', date.today() - timedelta(14))
    # for petition in query:
    # result.append(petition.to_json())
    # return result


def delete_petition(petition):
    # Refactored into this method in case there are other things to be done
    # before deleting a petition
    petition.delete()


def get_petitions(user):
    result = []
    query = Petition.gql('WHERE user = :1', user)
    for petition in query:
        result.append(petition.to_json())
    return result
