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
import models.election
import models.position

PAGE_URI = '/petitions'
MY_PAGE_URI = '/my'

class PetitionsHandler(webapp2.RequestHandler):
    def get(self):
			user = auth.require_login(self)
			ongoingElections = models.election.get_ongoing_elections()
			effectivePetitions = []
			for election in ongoingElections:
					petition = models.petition.get_petitions_for_election(election)
					if petition != []:
						effectivePetitions.append(petition[0])
			logging.info("effective petitions: %s", effectivePetitions)
			view = pages.render_view(PAGE_URI, {'effectivePetitions':effectivePetitions, 'ongoingElections':ongoingElections})
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
        if not petition:
            data['id'] = 'Duplicate Petition'
        else:
            data['id'] = str(petition.key())
        self.response.out.write(json.dumps(data))

class MyPageHandler(webapp2.RequestHandler):
    def get(self):
        user = auth.require_login(self)
        myPetitions = models.petition.get_petitions(user)
        view = pages.render_view(MY_PAGE_URI, {'myPetitions': myPetitions})
        pages.render_page(self, view)

class SignHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return

        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)
        #sendConfirmation(petition.get_user().get_id(), petition.get_organization(), petition.get_election(), petition.get_position(), petition.email())

        #Ensures you cannot vote your own petition.
        if user.get_id() != petition.get_user().get_id():
            models.petition.sign_petition(user, petition)
            self.response.out.write('Successfully signed!')
            #if petition.get_votes() == 25:
            #sendConfirmation(petition.get_user().get_id(), petition.get_organization(), petition.get_election(), petition.get_position(), petition.email())
        else:
            self.response.out.write('You cannot sign your own petition!')
        
class UnsignHandler(webapp2.RequestHandler):
    def post(self):
        user = auth.get_logged_in_user()
        if not user:
            return
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        #Ensures you cannot unvote your own petition. You never voted in the first place.
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
            return      # Should return error message here
        petition_id = self.request.get('id')
        petition = models.petition.get_petition(petition_id)

        # Make sure the user is not trying to delete someone else's petition
        assert petition.user.key() == user.key()

        models.petition.delete_petition(petition)
        self.response.out.write('Success!')

class PositionsPopulateHandler(webapp2.RequestHandler):
		def post(self):
			user = auth.get_logged_in_user()
			if not user:
				return # Should return error message here
			election_name = self.request.get('election')
			
			current_positions = models.position.get_positions_for_election(election_name)
			data = []
			for current_position in current_positions:
				data.append(str(current_position['title']))
			self.response.out.write(data)