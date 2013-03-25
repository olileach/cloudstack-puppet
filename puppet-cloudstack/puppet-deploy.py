import base64

from cloudstack_cmds import Cloudstack_Cmds
from cloudstack_api import CloudstackAPI

# hardcoding some API paramaters

api_key                 = ''
secret_key              = ''
so_id                   = ''
zone_id                 = ''
network_id              = ''
cs_host                 = ''
cs_protocol             = ''


# setting the puppet master and puppet agent template ID - this will be unique for every environment

puppet_agent            = ''
puppet_master           = ''

# Setting the Cloudstack_Cmds class variables to the hardcodes APIs above.

api_cmd = Cloudstack_Cmds()
Cloudstack_Cmds.api_key = api_key
Cloudstack_Cmds.secret_key = secret_key
Cloudstack_Cmds.cs_host = cs_host
Cloudstack_Cmds.cs_protocol = cs_protocol

# calling various handy api commands for service offerings, template IDs etc so we know what values we
# can hardcode above. Uncomment if you need to use these

#api_cmd.listaccounts()
#api_cmd.listzones()
#api_cmd.listserviceofferings()
#api_cmd.listtemplates()

# First, we need to acquire a public IP address. This is used for the httpd module via a custom facter 
# and a snat in cloudstack 

api_cmd.assocaiteip(zone_id)

# Deploying a puppet master; needs no userdata values and the template_id
# is set to the puppet_master variable value

getvmid = False
template_id = puppet_master
puppet_node = 'puppet-master'

api_cmd.deployvm(getvmid, command = 'deployVirtualMachine', serviceofferingid = so_id, templateid = template_id, zoneid = zone_id, \
                 networkids = network_id, puppet_node = puppet_node)

# Deploying the puppet agents. Here we send some userdata to classify the nodes, depening on what the node is. 
# The node role is part of the user data and is in a simple list that we can loop through

puppet_node = 'puppet-agent'
node_role = 'csm_server', 'nfs_server'
template_id = puppet_agent

for value in node_role:

    getvmid = False
    userdata = ('puppet_master_ip=%s\nrole=%s\n' % (Cloudstack_Cmds.pm_ipaddress, value))
    
    if value == 'csm_server':
        getvmid = True
        userdata = userdata = ('puppet_master_ip=%s\nrole=%s\nsnat_ipaddress=%s\n' % (Cloudstack_Cmds.pm_ipaddress, value, Cloudstack_Cmds.snat_ipaddress))
    
    api_cmd.deployvm(getvmid, command = 'deployVirtualMachine', serviceofferingid = so_id, templateid = template_id, zoneid = zone_id, \
                     networkids = network_id, puppet_node = puppet_node, userdata = base64.b64encode(userdata))

# enable static NAT on csm_vm using the public IP acquired earlier. Also configuring the Cloudstack firewall to open ports 80 and 443.

api_cmd.enablenat()

# Printing summary message

print '\nYour Cloudstack 4.0.1 deployment should be accessible on the following IP address: ',Cloudstack_Cmds.snat_ipaddress,', once the puppet has completed the cloudstack 4.0.1 installation.\n'
