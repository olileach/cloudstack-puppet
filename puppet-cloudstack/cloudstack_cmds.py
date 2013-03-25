import time

from dotdictify import dotdictify
from cloudstack_api import CloudstackAPI

class Cloudstack_Cmds(object):

    api_key = None
    secret_key = None
    cs_host = None
    cs_protocol = None
    pm_ipaddress = None
    snat_ipaddress = None
    csm_vmid = None
    snat_ipid = None

    def __init__(self, api_key=None, secret_key=None):

        self.api_key = api_key
        self.secret_key = secret_key

    def listaccounts(self):

        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)
         
        listaccounts = cs_api.request(dict({'command':'listAccounts'}))
        listaccounts = dotdictify(listaccounts)
        listcount = listaccounts.listaccountsresponse
        listaccounts = listaccounts.listaccountsresponse.account

        listindex = None
        for key, value in listcount.iteritems():
            if key == 'count' : listindex = value

        x, dom_name, userid  = 0, None, None

        while x < listindex:

            for key, value in listaccounts[x].iteritems():
                if key == 'domain': dom_name = value
                if key == 'id': userid = value
            print 'Domain name is', dom_name, 'and user ID is', userid
            x = x+1

    def listzones(self):     

        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        listzones = cs_api.request(dict({'command':'listZones'}))
        listzones = dotdictify(listzones)
        listcount = listzones.listzonesresponse
        listzones = listzones.listzonesresponse.zone
        listindex = None

        for key, value in listcount.iteritems():
            
            if key == 'count' : listindex = value

        x, zone_id, zone_name = 0, None, None
        while x < listindex:

            for key, value in listzones[x].iteritems():
                if key == 'id': zone_id = value
                if key == 'name' : zone_name = value
            print 'Zone id is', zone_id, 'and zone name is', zone_name
            x = x+1

                 
    def listserviceofferings(self):


        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        listso = cs_api.request(dict({'command':'listServiceOfferings'}))
        listso = dotdictify(listso)
        listcount = listso.listserviceofferingsresponse
        listso = listso.listserviceofferingsresponse.serviceoffering
        listindex = None

        for key, value in listcount.iteritems():
            if key == 'count' : listindex = value

        x, so_name, so_id = 0, None, None
        while x < listindex:

            for key, value in listso[x].iteritems():
                if key == 'id': so_id = value
                if key == 'name': so_name = value
            print 'Service offering ID is', so_id, 'and service offering name is', so_name
            x = x+1


    def listtemplates(self):


        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        listtempl = cs_api.request(dict({'command':'listTemplates', 'templatefilter':'executable'}))
        listtempl = dotdictify(listtempl)
        listcount = listtempl.listtemplatesresponse
        listtempl = listtempl.listtemplatesresponse.template
        listindex = None

        for key, value in listcount.iteritems():
            if key == 'count' : listindex = value

        x, templ_name, templ_id, templ_hyp = 0, None, None, None
        while x < listindex:

            for key, value in listtempl[x].iteritems():

                if key == 'id': templ_id = value
                if key == 'name': templ_name = value
                if key == 'hypervisor': tmpl_hyp = value
            print 'Template ID is', templ_id, 'template name is', templ_name, 'and hypervisor is', tmpl_hyp
            x = x+1


    def assocaiteip(self, zone_id):

        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        associateip  = cs_api.request(dict({'command':'associateIpAddress', 'zoneid': zone_id}))    
        associateip = dotdictify(associateip)
        associateip = associateip.associateipaddressresponse

        for key, value in associateip.iteritems():

            if key == 'jobid' : asyncjob = value

        cs_api.asyncresults(asyncjob,api_key=Cloudstack_Cmds.api_key, secret_key=Cloudstack_Cmds.secret_key)
        
        associateip_qryjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        associateip_qryjob = dotdictify(associateip_qryjob)
        associateip_qryjob = associateip_qryjob.queryasyncjobresultresponse.jobresult.ipaddress

        for key, value in associateip_qryjob.items():

            if key == 'id': Cloudstack_Cmds.snat_ipid = value 
            if key == 'ipaddress' : Cloudstack_Cmds.snat_ipaddress  = value

    def deployvm(self, *args, **kwargs):

        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        deployvm = cs_api.request(dict(kwargs))
        deployvm = dotdictify(deployvm)
        deployvm = deployvm.deployvirtualmachineresponse

        for key, value in deployvm.iteritems():

            if key == 'jobid' : asyncjob = value

        cs_api.asyncresults(asyncjob,api_key=Cloudstack_Cmds.api_key, secret_key=Cloudstack_Cmds.secret_key)

        deployvm_qryjob = cs_api.request(dict({'command':'queryAsyncJobResult', 'jobid':asyncjob}))
        deployvm_qryjob = dotdictify(deployvm_qryjob)
        deployvm_qryjob = deployvm_qryjob.queryasyncjobresultresponse.jobresult.virtualmachine

        ipaddress = None

        for v in args:
            if v == True:
                for key, value in deployvm_qryjob.items():
                    if key == 'id': Cloudstack_Cmds.csm_vmid = value


        for key, value in deployvm_qryjob.items():

            if key == 'nic':
                nic = value
                for key, value in nic[0].iteritems():
                    if kwargs.get('puppet_node') == 'puppet-master' and key == 'ipaddress' : Cloudstack_Cmds.pm_ipaddress = value

    def enablenat(self):

        cs_api = CloudstackAPI(api_key = Cloudstack_Cmds.api_key, secret_key = Cloudstack_Cmds.secret_key, host = Cloudstack_Cmds.cs_host, protocol = Cloudstack_Cmds.cs_protocol)

        enablenat = cs_api.request(dict({'command' : 'enableStaticNat' , 'ipaddressid' : Cloudstack_Cmds.snat_ipid, 'virtualmachineid' : Cloudstack_Cmds.csm_vmid}))
        time.sleep(15)

        enablenat = dotdictify(enablenat)
        enablenat = enablenat.enablestaticnatresponse

        createfw = cs_api.request(dict({'command' : 'createFirewallRule' , 'protocol' : 'tcp' , 'startport' : '80' , 'endport' : '80' , 'ipaddressid' : Cloudstack_Cmds.snat_ipid}))
        createfw = cs_api.request(dict({'command' : 'createFirewallRule' , 'protocol' : 'tcp' , 'startport' : '443' , 'endport' : '443' , 'ipaddressid' : Cloudstack_Cmds.snat_ipid}))
