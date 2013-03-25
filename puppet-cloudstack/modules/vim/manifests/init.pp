# Class vim
#
# This class installs vim
#
# Author: Oliver Leach
# Date : 18th March 2013
#
# Actions:
# Installs the vim package
#
# Requires:
# Centos - other operating systems are not supported by this manifest
#
# Sample Usage:
# include vim
#

class vim {

    case $operatingsystem {

        centos: {
   	    package { "vim-enhanced": ensure => "installed" }

    }

    default: {

	$supported = false
	    notify { "${module_name} is unsupported":
	    message => "The ${module_name} module is not supported on ${::operatingsystem}",
            }
        }
    }
}
