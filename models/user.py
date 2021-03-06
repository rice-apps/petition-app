"""
Model definition and functions for users.
"""

from google.appengine.ext import db


class User(db.Model):
    net_id = db.StringProperty(required=True)
    
    def get_id(self):
        return self.net_id


def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id).put()
    return user
