"""
Petitions page controller.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

import json
import logging
import pages
import webapp2
from datetime import date
from  mail import sendConfirmation

from authentication import auth
from models.user import User

import models.petition
import models.election
import models.organization

PAGE_URI = '/petitions'
MY_PAGE_URI = '/my'
ERROR_URI = '/error'


class PetitionsHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        ongoing_elections = models.election.get_ongoing_elections()
        for election in ongoing_elections:
            organization = models.organization.get_organization(election['organization'])
            election['organization'] = organization.title

        logging.info("Ongoing Elections: %s", ongoing_elections)

        petitions = {}
        for election in ongoing_elections:
            election_id = election['id']
            petitions[election['title']] = {}
            for position in election['positions']:
                petitions[election['title']][position] = models.petition.get_petitions_for_position(election_id,
                                                                                                    position)
                for petition in petitions[election['title']][position]:
                    if petition['user'].get_id() == user.get_id():
                        petition['own'] = True
                    else:
                        petition['own'] = False
                    if user.get_id() in petition['signatures']:
                        petition['signed'] = True
                    else:
                        petition['signed'] = False

        logging.info("Petitions: %s", petitions)
        view = pages.render_view(PAGE_URI, {'petitions': petitions, 'ongoing_elections': ongoing_elections})
        pages.render_page(self, view)


class MyPageHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        if not user:
            return self.redirect(ERROR_URI)

        ongoing_elections = models.election.get_ongoing_elections()
        for election in ongoing_elections:
            organization = models.organization.get_organization(election['organization'])
            election['organization'] = organization.title

        petitions = models.petition.get_petitions(user)
        expired_petitions = []
        ongoing_petitions = []
        for petition in petitions:
            election = models.election.get_election(petition['election'])
            petition['election'] = election.title
            organization = models.organization.get_organization(election.organization)
            petition['organization'] = organization.title
            if election.end_date < date.today():
                expired_petitions.append(petition)
            else:
                ongoing_petitions.append(petition)

        view = pages.render_view(MY_PAGE_URI, {'expired_petitions': expired_petitions,
                                               'ongoing_petitions': ongoing_petitions,
                                               'ongoing_elections': ongoing_elections})
        pages.render_page(self, view)

    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)

        # Create petition
        data = json.loads(self.request.get('data'))
        logging.info('Petition Post: %s', data)
        petition = models.petition.create_petition(user, data)

        # Respond
        if not petition:
            self.response.out.write('Duplicate Petition')
        else:
            self.response.out.write('Success')


class SignHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)

        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)
        # sendConfirmation(petition.get_user().get_id(), petition.get_organization(), petition.get_election(),
        # petition.get_position(), petition.email())

        # Ensures you cannot vote your own petition.
        if user.get_id() != petition.get_user().get_id():
            models.petition.sign_petition(user, petition)
            self.response.out.write('Successfully signed!')
            # if petition.get_votes() == 25:
            # sendConfirmation(petition.get_user().get_id(), petition.get_organization(), petition.get_election(),
            # petition.get_position(), petition.email())
        else:
            self.response.out.write('You cannot sign your own petition!')


class UnsignHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        # Ensures you cannot unsign your own petition. You never voted in the first place.
        if user.get_id() != petition.get_user().get_id():
            models.petition.unsign_petition(user, petition)
            self.response.out.write('Successfully unsigned!')

        else:
            self.response.out.write('You cannot unsign your own petition!')


class GarbageHandler(webapp2.RequestHandler):
    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return self.redirect(ERROR_URI)
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        # Make sure the user is not trying to delete someone else's petition
        assert petition.user.key() == user.key()

        models.petition.delete_petition(petition)
        self.response.out.write('Success!')
