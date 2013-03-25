import urllib
import urllib2
import hmac
import hashlib
import base64
import json
import time
from dotdictify import *

class CloudstackAPI(object):

    jobresults = None
    api_key = None
    secret_key = None
    host = None
    protocol = None

    def __init__(self, protocol = None, host = None , uri = '/client/api', api_key = None, secret_key = None, asyncjob = None):

        self.protocol = protocol
        self.host = host
        self.uri = uri
        self.api_key = api_key
        self.secret_key = secret_key
        self.errors = []
        self.aysncjob = asyncjob

    def request(self, params):

        """Builds a query from params and return a json object of the result or None"""

        if self.api_key and self.secret_key:
            # add the default and dynamic params
            params['response'] = 'json'
            params['apiKey'] = self.api_key

            # build the query string
            query_params = map(lambda (k,v):k+"="+urllib.quote(str(v)), params.items())
            query_string = "&".join(query_params)

            # build signature
            query_params.sort()
            signature_string = "&".join(query_params).lower()
            signature = urllib.quote(base64.b64encode(hmac.new(self.secret_key, signature_string, hashlib.sha1).digest()))

            # final query string...
            url = self.protocol+"://"+self.host+self.uri+"?"+query_string+"&signature="+signature

            output = None
            try:
                output = json.loads(urllib2.urlopen(url).read())
            except urllib2.HTTPError, e:
                self.errors.append("HTTPError: "+str(e.code))
            except urllib2.URLError, e:
                self.errors.append("URLError: "+str(e.reason))

            return output
        else:
            self.errors.append("missing api_key and secret_key in the constructor")
            return None

    def asyncresults(self, asyncjob, api_key, secret_key):

        cs_api = CloudstackAPI(api_key=api_key, secret_key=secret_key)
        qryasyncjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        qryasyncjob = dotdictify(qryasyncjob)
        qryasyncjob = qryasyncjob.queryasyncjobresultresponse

        print ('\n\nChecking the progress of the async jobid %s every 5 seconds to see if it has completed.\n\nPlease wait....\n' % (asyncjob))

        for key, value in qryasyncjob.items():

            if key == 'jobstatus':
                if value == 0:

                    status=0
                    while status==0:

                        qryasyncjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
                        qryasyncjob = dotdictify(qryasyncjob)
                        qryasyncjob = qryasyncjob.queryasyncjobresultresponse

                        for key, value in qryasyncjob.iteritems():
                            if key == 'jobstatus' : status = value
                            if key == 'jobstatus' : CloudstackAPI.jobresults = value
                        time.sleep(5)

                    print 'API job complete. Moving on to next task.'
                    queryasyncjobresponse = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
                    return queryasyncjobresponse


