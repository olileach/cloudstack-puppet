# Cloudstack 4.0.1 deploy

This project enables a running cloudstack instance 3.x and above to deploy Cloudstack 4.0.1 instances. This could
to demo Cloudstack 4.0.1 or used for testing purposes, by easily spinning up Cloudstack 4.0.1 instances. It could
also be used to provision private clouds.

## How to use this project

The python script and puppet manifests in this repo deploys cloudstack 4.0.1 using Puppet and the Cloudstack API.

For this to work, you need to use the python scripts and 2 puppet templates. One template is the puppet-master, and 
one template is the puppet-agent.

You need to configure the python parameters in the puppet-deploy.py script as per your environment. This
includes:

    1 - your API key
    2 - your secret key
    3 - your service offering
    4 - your Cloudstack zone ID
    5 - your network ID of your user account
    6 - The Cloudstack provisioning host IP and port
    7 - The Cloudstack protocol used (http or https)

You will also need your 2 template IDs for the puppet master and puppet agent

These templates can be downloaded using the following link:

### Puppet Agent

https://dl.dropbox.com/u/79905244/puppet-agent.7z

### Puppet Master

https://dl.dropbox.com/u/79905244/puppet-master.7z

Both templates are running CentOS 6.4 64-bit.. The puppet master is configured as a puppet-ca, a puppet server and a 
puppet agent. The puppet agent has the puppet agent installed and runs a userdata.rb script on startup. See the rc.local
file for further information.

Once the templates are unzipped and uploaded in to your provisioning Cloudstack instance, update the puppet-deploy.py 
script with the template IDs.

This project is just for fun, could be better written and I hold no repsonsibilty if you use the project. You are
allowed to do so.
