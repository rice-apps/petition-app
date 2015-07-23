"""
Main page controller.
"""

__author__ = 'Xiaoyu Chen <xc12@rice.edu>'

import pages
import webapp2

PAGE_URI = '/main'
ERROR_URI = '/error'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(PAGE_URI)
        pages.render_page(self, view)


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(ERROR_URI)
        pages.render_page(self, view)
