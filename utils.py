# Author: monkeylyf
# Data: Nov 14 2012

import datetime
import re
import urllib2

import constant
import db_access
import smsgateway

def url_content_search(regex, url):
    """Search content of pass-in url for pass-in regex pattern."""
    try:
        handler = urllib2.urlopen(url)
        content = handler.read()
        handler.close()
        m = re.search(regex, content)
        if m:
            return constant.FINISHED
        else:
            return constant.ASSIGNED
    except:
        return constant.ASSIGNED

def do_job(job_info):
    """Do job logic.
    
    :return updated job info: dict, no matter the job failed or finished or
    still assigned.
    """
    result = url_content_search(job_info['regex'], job_info['url'])
    if result == constant.FINISHED:
        if not smsgateway.SMSGateway().send(job_info['phone'], constant.TEXT):
            result = constant.FAILED
    return db_access.update_entity(job_info['id'],
                                   status=result,
                                   mtime=datetime.datetime.now())
