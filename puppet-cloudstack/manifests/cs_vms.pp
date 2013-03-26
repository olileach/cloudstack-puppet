class cs_vms {

    Firewall {
        notify  => Exec["persist-firewall"],
        require => Exec["purge default firewall"],
    }

    $mysql_password = ('s333cret')

    case $role {

        'csm_server': {

            include 'vim'

            class { 'cloudstack' :
                mysql_password => [ $mysql_password ],
                require => Class[ 'mysql::server' ],
            }

            include 'apache'

            class { 'selinux' :
                mode => 'permissive'
            }

            class { 'mysql::server' :
                mysql_password => [ $mysql_password ],
            }

            class { 'iptables' :
                require => Class[ 'cloudstack' ],
			}
        }
        'nfs_server': {

            include 'nfs'
        }
    }
}
