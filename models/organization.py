"""
Model definition and functions for organizations.
"""

from google.appengine.ext import db
from user import User


class Organization(db.Model):
    user = db.ReferenceProperty(User, required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    admins = db.ListProperty(str)

    def to_json(self):
        return {'user': self.user.get_id(), 'title': self.title, 'id': str(self.key()), 'description': self.description,
                'admins': self.admins}

    def get_admins(self):
        return self.admins

    def get_title(self):
        return self.title

    def set_admins(self, admins):
        self.admins = admins


def get_organization(key):
    return Organization.get(key)


def get_all_organizations():
    result = []
    query = Organization.gql('')
    for organization in query:
        result.append(organization.to_json())
    return result


def create_organization(user, organization):
    existing = get_all_organizations()
    name_list = []
    for existing_organizations in existing:
        name_list.append(existing_organizations['title'].replace(' ', ''))

    if organization['title'].replace(' ', '') not in name_list or not existing:
        organization = Organization(
            user=user,
            title=organization['title'].rstrip(),
            description=organization['description'],
            admins=organization['admins'])
        organization.put()
        return organization
    else:
        return None


def delete_organization(organization):
    # Refactored into this method in case there are other things to be done
    # before deleting a organization
    organization.delete()


def update_admins(organization_id, admins):
    organization = get_organization(organization_id)
    organization.set_admins(admins)
    organization.put()
    return
