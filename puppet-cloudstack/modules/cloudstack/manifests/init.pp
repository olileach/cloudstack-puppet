# Class cloudstack
#
# This class installs cloudstack
#
# Author: Oliver Leach
# Date : 18th March 2013
#
# Actions:
# Installs the cloudstakc package
#
# This includes, the cloudstack-client, mysql-server and any install commands
#
# Currently the clodustack class is monlithic for demo purposes.
#
# Requires:
# Centos - other operating systems are not supported by this manifest
#
# Sample Usage:
# include cloudstack
#

class cloudstack ($mysql_password) {

	case $::operatingsystem {

		'centos': {
			$supported 	= true
		}
	}

	if ($supported == true) {

		yumrepo { 'cloudstack':
    		baseurl  => "http://cloudstack.apt-get.eu/rhel/4.0/",
			descr 	 => "Cloudstack 4.0.1 yum repo",
	   		enabled  => 1,
	   		gpgcheck => 0,
		}

		package { "cloud-client": 
			ensure 	=> "installed",
			require	=> Yumrepo["cloudstack"],
			}

		exec { "cloud-setup" :
			command => "/usr/bin/cloud-setup-databases cloud:cloud@localhost --deploy-as=root:${mysql_password} && /bin/sleep 3 && /usr/bin/cloud-setup-management && /bin/sleep 3 && /usr/bin/cloud-setup-databases cloud:cloud@localhost --deploy-as=root:${mysql_password} && /bin/sleep 3 && /usr/bin/cloud-setup-management",
			creates => '/var/lib/mysql/cloud',
			require => Package["cloud-client"],
		}

        service { "cloud-management":
    		ensure  => "running",
    		enable  => "true",
    		require => Exec["cloud-setup"],
		}
	}
}
