"""
Elections page controller.
"""

__author__ = 'Roshni Kaushik <rsk8@rice.edu>'

import json
import logging
import pages
import webapp2
import datetime

# from  mail import sendConfirmation

from authentication import auth

import models.organization
import models.user
import models.election

PAGE_URI = '/dashboard'
ADMIN_ID = 'rsk8'
ERROR_URI = '/error'

class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        # Get the organization
        organization_id = self.request.get('id')
        organization = models.organization.get_organization(organization_id).to_json()
        logging.info("Organization: %s", organization)

        # Make sure the user is authorized to delete the organization
        assert user.get_id() in organization['admins']

        admin_dict = {}
        for admin in organization['admins']:
            admin_dict[admin] = (user.get_id() == admin or ADMIN_ID == admin)
        organization['admins'] = admin_dict

        # Get all the elections for the organization
        elections = models.election.get_organization_elections(organization['id'])
        ongoing_elections = []
        upcoming_elections = []
        for election in elections:
            if election['start_date'] < datetime.date.today():
                ongoing_elections.append(election)
            else:
                upcoming_elections.append(election)
        logging.info("Elections: %s", elections)

        view = pages.render_view(PAGE_URI, {'organization': organization, 'ongoing_elections': ongoing_elections,
                                            'upcoming_elections': upcoming_elections})
        pages.render_page(self, view)


class SaveAdminsHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        data = json.loads(self.request.get('data'))
        logging.info('Save Admins Post: %s', data)

        models.organization.update_admins(data['organization_id'], data['admins'])

        self.response.out.write('Success!')


class AddElectionHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        data = json.loads(self.request.get('data'))
        logging.info('Add Election Post: %s', data)

        election = models.election.create_election(user, data)

        # Respond
        if not election:
            self.response.out.write('Duplicate Election')
        else:
            self.response.out.write('Success')


class DeleteElectionHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        election_id = self.request.get('id')
        election = models.election.get_election(election_id)
        models.election.delete_election(election)

        self.response.out.write('Success!')
