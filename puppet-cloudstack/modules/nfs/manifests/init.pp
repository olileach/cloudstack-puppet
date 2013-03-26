# Class nfs
#
# This class installs vim-enhanced and configures a vimrc global file
#
# Author: Oliver Leach
# Date : 8th March 2013
#
# Actions:
# Ensures nfs package is instaleld and configured using the exports file
#
# Requires:
# Centos - other operating systems are not currently supported by this module
#
# Sample Usage:
# include nfs
#
# Parameters
#
#  nfsaccess  - IP address of allow servers, i.e * for all or 10.0.0.1 for specific IP or network 10.0.0.0/24
#  nfsfolder  - The nfs share point on the file system
#  auotupdate - Specify whether you would like to autoupdate the nfs packge, or stick with the present one available

class nfs ($nfs_access, 
           $nfs_folder, 
           $auto_update, ){

# making sure defaults are set for parameters

    if $auto_update == true {
        $package_ensure = latest
    } 
    elsif $auto_update == false {
        $package_ensure = present
    }
    else {
        $package_ensure = present
    }
    if ($nfs_folder == undef){
            $nfs_folder_path = [ '/nfs', ]
    }
    else {
        $nfs_folder_path = $nfs_folder 
    }
    if ($nfs_access == undef){
            $nfs_access_node = [ '*', ]
    }
    else {
        $nfs_access_node = $nfs_access
    }

# case options - sets specific operating system values

    case $::operatingsystem {

        centos: {

            $supported  = true
            $nfsservice = 'nfs'
            $config_tpl = 'nfsexports.el.erb'
            $exports    = '/etc/exports'
        }

        default: {

            $supported = false
            notify { "${module_name} is unsupported":
                message => "The ${module_name} module is not supported on ${::operatingsystem}",
            }   
        }
    }

    if $supported == (true) {

        package { "nfs-utils"       : ensure => $package_ensure, }
        package { "nfs-utils-lib"   : ensure => $package_ensure, }
        package { "rpcbind"         : ensure => $package_ensure, }
        service { $nfsservice:
            ensure      => running,
            enable      => true,
            hasrestart  => true,
        } 

        file { "${nfs_folder_path}":
            ensure      => directory,
        }

        file { $exports:

            owner       => root,
            group       => root,
            mode        => '0644',
            content     => template("${module_name}/${config_tpl}"),
        }
    }
}
