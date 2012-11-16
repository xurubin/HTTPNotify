# Main logic.
# Author: xurubin, monkeylyf
# Date: Nov 15 2012
import json
import os
import datetime
import calendar

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import logging
import constant
import db_access
import utils


class EntityEncoder(json.JSONEncoder):
    """ 
    Special JSON encoder for Entity, which converts a 
    datetime to a string representation
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            #return "new Date.UTC(%d, %d, %d, %d, %d, %d, %d)" % \
            #    (obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond)
            return  calendar.timegm(obj.utctimetuple())
        else:
            return json.JSONEncoder.default(self, obj)


class MainPage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        template_values = {'entries' : [json.dumps(e, cls=EntityEncoder) for e in db_access.retrieve_all()]}

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class JsonHandler(webapp.RequestHandler):
    def outputJson(self, obj):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(obj, cls=EntityEncoder))
    def outputError(self, error):
        logging.error("Error occurred: " + error)
        self.outputJson({'result' : False, 'error' : error})
    def outputData(self, data):
        result = {'result' : True}
        result.update(data)
        self.outputJson(result)
    def outputEntity(self, entity):
        self.outputData({'entry' : entity})

def getRequestEntry(request):
    return {'url' : request.get('url', None),
            'regex' : request.get('regex', None),
            'interval' : request.get('interval', '3600'),
            'phone' : request.get('phone', None),
            }


class RefreshAllHandler(JsonHandler):
    """Refresh all the registered job in datastore and iterate all the job."""
    def get(self):
        for job_info in db_access.retrieve_all():
            if job_info['status'] == constant.ASSIGNED:
                utils.do_job(job_info)


class RefreshOneHandler(JsonHandler):
    """Refresh one registrered job in datastore and do job."""
    def get(self, url_id):
        eid = int(url_id)
        job_info = db_access.retrieve_by_id(eid)
        try:
            if job_info['status'] == constant.ASSIGNED:
                job_info = utils.do_job(job_info)
            self.outputEntity(job_info)
        except Exception as e:
            self.outputError(str(e))

class AddEntryHandler(JsonHandler):
    ''' 
    Add new entry to the data store, returns its id upon success
    Need to start cron job as well. 
    '''
    def post(self):
        entry = getRequestEntry(self.request)
        entity = db_access.add_entity(entry['url'],
                                     entry['regex'],
                                     entry['phone'])
        if entity:
            self.outputEntity(entity)
        else:
            self.outputError("Cannot add entry.")


class UpdateEntryHandler(JsonHandler):
    '''
    Update the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        entry = getRequestEntry(self.request)
        entity = db_access.update_entity(eid, 
                                     entry['url'],
                                     entry['regex'],
                                     entry['phone'])
        if entity:
            self.outputEntity(entity)
        else:
            self.outputError("Cannot update entry.")


class ResetEntryHandler(JsonHandler):
    '''
    Reset the status and possibly restart cron job of the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        entity = db_access.update_entity(eid, status='assigned')
        if entity:
            self.outputEntity(entity)
        else:
            self.outputError("Cannot reset entry status.")


class DeleteEntryHandler(JsonHandler):
    '''
    Delete the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        db_access.delete_entity(eid)
        self.outputData({})


application = webapp.WSGIApplication([('/', MainPage),
                                      (r'^/add$',           AddEntryHandler),
                                      (r'^/update/(\d+)$',  UpdateEntryHandler),
                                      (r'^/reset/(\d+)$',   ResetEntryHandler),
                                      (r'^/delete/(\d+)$',  DeleteEntryHandler),
                                      (r'^/refresh/(\d+)$', RefreshOneHandler),
                                      (r'^/refreshall$',    RefreshAllHandler),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
