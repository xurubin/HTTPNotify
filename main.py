# Main logic.
# Author: xurubin, monkeylyf
# Date: Nov 15 2012
import json
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import constant
import db_access
import utils


class MainPage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
            'entries': [json.dumps({'id' : 'adfa',
                                    'url' : 'http://www.google.com',
                                    'regex' : 'google',
                                    'phone': '12345689',
                                    'mtime' : '2012-11-11',
                                    'interval' : 60}),]
                         }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        self.response.out.write(db_access.retrieve_all())


class JsonHandler(webapp.RequestHandler):
    def outputJson(self, obj):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(obj))
    def outputError(self, error):
        self.outputJson({'result' : False, 'error' : error})
    def outputData(self, data):
        result = {'result' : True}
        result.update(data)
        self.outputJson(result)


def getRequestEntry(request):
    return {'url' : request.get('url', None),
            'regex' : request.get('regex', None),
            'interval' : request.get('interval', '3600'),
            'phone' : request.get('phone', None),
            }


class RefreshAllHandler(JsonHandler):
    """Refresh all the registered job in datastore and iterate all the job."""
    def post(self):
        for job_info in db_access.retrieve_all():
            if job_info['status'] == constant.ASSIGNED:
                utils.do_job(job_info)


class RefreshOneHandler(JsonHandler):
    """Refresh one registrered job in datastore and do job."""
    def post(self, url_id):
        eid = int(url_id)
        job_info = db_access.retrieve_by_id(eid)
        if job_info['status'] == constant.ASSIGNED:
            job_info = utils.do_job(job_info)
        self.outputData(job_info)
        

class AddEntryHandler(JsonHandler):
    ''' 
    Add new entry to the data store, returns its id upon success
    Need to start cron job as well. 
    '''
    def post(self):
        entry = getRequestEntry(self.request)
        self.outputData(db_access.add_entity(entry['url'],
                                             entry['regex'],
                                             entry['phone']))


class UpdateEntryHandler(JsonHandler):
    '''
    Update the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        entry = getRequestEntry(self.request)
        self.outputData(db_access.update_entity(eid,
                                                url=entry['url'],
                                                regex=entry['regex'],
                                                phone=entry['phone']))


class DeleteEntryHandler(JsonHandler):
    '''
    Delete the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        db_access.delete_entity(eid)
        self.outputData({})


class RefreshEntryHandler(JsonHandler):
    '''
    Perform check on the given entry
    If initialised by user then force recheck;
    If initialised by cron then obey the preset interval. 
    '''
    def get(self, url_id):
        eid = int(url_id)
        self.outputData(db_access.retrieve_by_id(eid))


application = webapp.WSGIApplication([('/', MainPage),
                                      (r'^/add$',           AddEntryHandler),
                                      (r'^/update/(\d+)$',  UpdateEntryHandler),
                                      (r'^/reset/(\d+)$',   RefreshOneHandler),
                                      (r'^/delete/(\d+)$',  DeleteEntryHandler),
                                      (r'^/refresh/(\d+)$', RefreshEntryHandler),
                                      (r'^/refreshall$', RefreshALLHandler),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
