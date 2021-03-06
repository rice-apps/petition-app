"""
Elections page controller.
"""

import json
import logging
import pages
import webapp2
import datetime

# from  mail import sendConfirmation

from authentication import auth
from config import *
import models.organization
import models.user
import models.election
import models.petition


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
        expired_elections = []
        for election in elections:
            positions = {}
            for position in election['positions']:
                petitions = models.petition.get_petitions_for_position(election['id'], position)
                for petition in petitions:
                    petition['signatures_left'] = election['threshold'] - petition['signature_num']
                    if petition['signatures_left'] < 0:
                        petition['signatures_left'] = 0
                positions[position] = petitions
            election['positions'] = positions
            if election['start_date'] > datetime.date.today():
                upcoming_elections.append(election)
            elif election['end_date'] < datetime.date.today():
                expired_elections.append(election)
            else:
                ongoing_elections.append(election)
        logging.info("Elections: %s", elections)

        view = pages.render_view(DASHBOARD_URI, {'organization': organization,
                                                 'ongoing_elections': ongoing_elections,
                                                 'upcoming_elections': upcoming_elections,
                                                 'expired_elections': expired_elections})
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


class ElectionHandler(webapp2.RequestHandler):
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

    def delete(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        election_id = self.request.get('id')
        election = models.election.get_election(election_id)
        models.election.delete_election(election)

        self.response.out.write('Success!')
