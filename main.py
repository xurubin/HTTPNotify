from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import json
import os

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
            'entries': [json.dumps({'id' : 'adfa', 'url' : 'http://www.google.com', 'regex' : 'google', 'telnum': '12345689', 'mtime' : '2012-11-11', 'interval' : 60}),
                        ]
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

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
        
class AddEntryHandler(JsonHandler):
    ''' 
    Add new entry to the data store, returns its id upon success
    Need to start cron job as well. 
    '''
    def post(self):
        self.outputData({id : 1})
        
class UpdateEntryHandler(JsonHandler):
    '''
    Update the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        self.outputData({id : eid})

class ResetEntryHandler(JsonHandler):
    '''
    Reset the status and possibly restart cron job of the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        self.outputData({id : eid})

class DeleteEntryHandler(JsonHandler):
    '''
    Delete the given entry 
    '''
    def post(self, url_id):
        eid = int(url_id)
        self.outputData({id : eid})

class RefreshEntryHandler(JsonHandler):
    '''
    Perform check on the given entry
    If initialised by user then force recheck;
    If initialised by cron then obey the preset interval. 
    '''
    def get(self, url_id):
        eid = int(url_id)
        self.outputData({id : eid})


application = webapp.WSGIApplication([('/', MainPage),
                                      (r'^/add$',           AddEntryHandler),
                                      (r'^/update/(\d+)$',  UpdateEntryHandler),
                                      (r'^/reset/(\d+)$',   ResetEntryHandler),
                                      (r'^/delete/(\d+)$',  DeleteEntryHandler),
                                      (r'^/refresh/(\d+)$', RefreshEntryHandler),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
