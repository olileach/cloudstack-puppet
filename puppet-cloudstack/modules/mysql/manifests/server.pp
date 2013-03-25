# Class myslqserver
#
# This class installs cloudstack
#
# Author: Oliver Leach
# Date : 20th March 2013
#
# Actions:
# Installs the mysql server package
#
# This includes, the mysql-server package
#
# Requires:
# Centos - other operating systems are not supported by this manifest
#
# Sample Usage:
# include mysql::server
#

class mysql::server ($mysql_password) {

	case $::operatingsystem {
		"centos": {
			$supported 	= true
		}
	}

	if ($supported == true) {

        file { "flag-files" :

            ensure  => directory,
            path    => "/var/lib/puppet/flags/",
            owner   => root,
            group   => root,
            mode    => "0644",
        }

		package { "mysql-server":
			ensure 	=> installed,
			require	=> File["flag-files"], 
		}

        file { "/etc/my.cnf" :
            owner   => "root",
            group   => "root",
            source  => "puppet:///modules/mysql/my.cnf",
			require	=> Package["mysql-server"],
        }

		service { "mysqld" :
			enable 	=> true,
			ensure 	=> running,
	        require => File["/etc/my.cnf"],
		}

        $mysql_server_exec_1 = "0000000000001"
        $mysql_server_file_1 = "/var/lib/puppet/flags/mysql_server_exec_1"

		exec { "restart-mysqld" :
            command => "/sbin/service mysqld restart && echo \"$mysql_server_exec_1\" > \"$mysql_server_file_1\"",
            unless  => "/usr/bin/test \"`/bin/cat $mysql_server_file_1 2>/dev/null`\" = \"$mysql_server_exec_1\"",
            require => Service["mysqld"],
            }

		exec { "set-mysql-password" :
			unless 	=> "/usr/bin/mysqladmin -uroot -p${mysql_password} status",
			command => "/usr/bin/mysqladmin -uroot password ${mysql_password}",
			require => Exec["restart-mysqld"],
		}

		$mysql_server_exec_2 = "0000000000001"
		$mysql_server_file_2 = "/var/lib/puppet/flags/mysql_server_exec_2"		

		exec { "remove-test-dbs" :
			command => "/usr/bin/mysql -u root -p${mysql_password} -e \"DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';\" && echo \"$mysql_server_exec_2\" > \"$mysql_server_file_2\"",
			unless 	=> "/usr/bin/test \"`/bin/cat $mysql_server_file_2 2>/dev/null`\" = \"$mysql_server_exec_2\"",
			require	=> Exec["set-mysql-password"],
			}

	    $mysql_server_exec_3 = "0000000000003"
        $mysql_server_file_3 = "/var/lib/puppet/flags/mysql_server_exec_3"

		exec { "remove-remote-root-access" :
			command => "/usr/bin/mysql -u root -p${mysql_password} -e \"DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');\" && echo \"$mysql_server_exec_3\" > \"$mysql_server_file_3\"",
			unless 	=> "/usr/bin/test \"`/bin/cat $mysql_server_file_3 2>/dev/null`\" = \"$mysql_server_exec_3\"",
			require	=> Exec["set-mysql-password"],
		}
	}
}
