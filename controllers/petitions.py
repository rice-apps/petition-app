"""
Petitions page controller.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

import json
import logging
import pages
import webapp2
from  mail import sendConfirmation

from authentication import auth
from models.user import User

import models.petition

PAGE_URI = '/petitions'
MY_PAGE_URI = '/my'

class PetitionsHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        #petitions = models.petition.get_petitions(user)
        effectivePetitions = models.petition.get_in_effect_petitions()
        expiredPetitions = models.petition.get_expired_petitions()
        logging.info("effective petitions: %s", effectivePetitions)
        for petition in effectivePetitions:
            print petition['votes']
        view = pages.render_view(PAGE_URI, {'effectivePetitions': effectivePetitions, 'expiredPetitions':expiredPetitions})
        pages.render_page(self, view)

    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return      # Should return error message here
        # Create petition
        data = json.loads(self.request.get('data'))
        logging.info('Petition Post: %s', data)
        petition = models.petition.create_petition(user, data)

        # Respond
        data['id'] = str(petition.key())
        self.response.out.write(json.dumps(data))

class MyPageHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        myPetitions = models.petition.get_petitions(user)
        view = pages.render_view(MY_PAGE_URI, {'myPetitions': myPetitions})
        pages.render_page(self, view)

class VoteHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return

        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        #Ensures you cannot vote your own petition.
        if user.get_id() != petition.get_user().get_id():
            models.petition.vote_petition(user, petition)
            self.response.out.write('Successfully voted!')
            if petition.get_votes() == 25:
                sendConfirmation(petition.get_user().get_id(), petition.get_org_name(), petition.get_org_email())
        else:
            self.response.out.write('You cannot vote on your own petition!')

class UnvoteHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        #Ensures you cannot unvote your own petition. You never voted in the first place.
        if user.get_id() != petition.get_user().get_id():
            models.petition.unvote_petition(user, petition)
            self.response.out.write('Successfully unvoted!')

        else:
            self.response.out.write('You cannot unvote your own petition!')


class GarbageHandler(webapp2.RequestHandler):
    def post(self):
        # Authenticate user
        user = auth.get_logged_in_user()
        if not user:
            return      # Should return error message here
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        # Make sure the user is not trying to delete someone else's petition
        assert petition.user.key() == user.key()

        models.petition.delete_petition(petition)
        self.response.out.write('Success!')



