# Author: monkeylyf
# Data: Nov 14 2012

import re
import urllib2

def url_content_search(regex, url):
    """Search content of pass-in url for pass-in regex pattern."""
    try:
        handler = urllib2.urlopen(url)
        str = handler.read()
        handler.close()
    except Exception, e:
        raise Exception
    m = re.search(regex, str)
    if m:
        return True
    else:
        return False
