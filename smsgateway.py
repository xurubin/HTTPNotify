'''
Created on 14 Nov 2012

@author: Rubin
'''

import config
import urllib
import urllib2
import base64

class SMSGateway():
    SMS_API_URL = "https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages.json"

    def __init__(self):
        self.setToken(config.Twilio_SID, config.Twilio_TOKEN)
        self.senderNum = config.Twilio_SendNumber
        
    def request(self, URL, params):
        request = urllib2.Request(URL % self.sid, urllib.urlencode(params))
        encoded_auth = base64.b64encode('%s:%s' % (self.sid, self.token))
        request.add_header("Authorization", "Basic %s" % encoded_auth)
        try:   
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise Exception("Request error: " + e.read())    

        if response.code == 200 or response.code == 201:
            return True
        else:
            print response.code
            raise Exception("Request error: " + response.read())    
        
    def setToken(self, sid, token):
        self.sid = sid
        self.token = token
        
    def send(self, tel, text):
        params = {'From' : self.senderNum,
                  'To'   : tel,
                  'Body' : text}
        return self.request(SMSGateway.SMS_API_URL, params)

if __name__ == "__main__":
    import sys
    tel = sys.argv[1]
    text = sys.argv[2]
    
    print SMSGateway().send(tel, text)