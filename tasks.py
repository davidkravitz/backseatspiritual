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
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email():
    fromaddr = 'dnkravitz@gmail.com'
    toaddrs = 'dnkravitz@gmail.com'
    msg = 'The eagle has landed.'

    #provide gmail user name and password
    username = 'dnkravitz'
    password = 'pentuphouse'

    # functions to send an email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

class Cron(webapp2.RequestHandler):
    def get(self):
        url = 'http://losangeles.ucbtrainingcenter.com/improv/101'
        opener = urllib2.build_opener()
        request = urllib2.Request(url)
        data = opener.open(request).read()
        soup = BeautifulSoup(data)
        links = soup.findAll(href=re.compile('/courses/view'))
        if any("Register" in link.contents[0] for link in links):
            send_email()

app = webapp2.WSGIApplication([
    ('/cron', Cron)
], debug=True)