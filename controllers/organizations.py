"""
Elections page controller.
"""

import json
import logging
import pages
import webapp2

from authentication import auth
import models.organization
import models.user
import models.election
import models.petition
from config import *


class OrganizationsHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        # Get all the organizations
        organizations = models.organization.get_all_organizations()
        logging.info("organizations: %s", organizations)

        is_admin = user.get_id() == ADMIN_ID
        for organization in organizations:
            if user.get_id() in organization['admins'] or is_admin:
                organization['dashboard'] = True
            else:
                organization['dashboard'] = False

        if user.get_id() == ADMIN_ID:
            admins = ADMIN_ID
        else:
            admins = ADMIN_ID + ',' + user.get_id()

        view = pages.render_view(ORGANIZATION_URI, {'organizations': organizations, 'is_admin': is_admin,
                                                    'admins': admins, 'admin': ADMIN_ID})
        pages.render_page(self, view)

    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)

        # Create organization
        data = json.loads(self.request.get('data'))
        logging.info('Organization Post: %s', data)
        organization = models.organization.create_organization(user, data)

        # Respond
        if not organization:
            self.response.out.write('Duplicate Organization')
        else:
            self.response.out.write('Success')

    def delete(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)
        organization_id = self.request.get('id')
        organization = models.organization.get_organization(organization_id)

        # Make sure the user is authorized to delete the organization
        assert user.get_id() == ADMIN_ID

        models.organization.delete_organization(organization)

        elections = models.election.get_organization_elections(organization_id)
        for election in elections:
            for position in election.positions:
                petitions = models.petition.get_petitions_for_position(election.id, position)
                for petition in petitions:
                    models.petition.delete_petition(petition)
            models.election.delete_election(election)
        self.response.out.write('Success!')
