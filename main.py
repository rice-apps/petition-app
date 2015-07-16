#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from controllers import main, petitions, organizations, dashboards

app = webapp2.WSGIApplication([
    ('/petitions', petitions.PetitionsHandler),
    ('/petitions/sign', petitions.SignHandler),
    ('/petitions/unsign', petitions.UnsignHandler),
    ('/my', petitions.MyPageHandler),
    ('/organizations', organizations.OrganizationsHandler),
    ('/dashboard', dashboards.DashboardHandler),
    ('/dashboard/admins', dashboards.SaveAdminsHandler),
    ('/dashboard/elections', dashboards.ElectionHandler),
    ('/error', main.ErrorHandler),
    ('/', main.MainHandler)

], debug=True)
