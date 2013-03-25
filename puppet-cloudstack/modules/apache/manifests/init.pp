class apache {

	$snat_ip = $snat_ipaddress

	case $operatingsystem {

		'CentOS', 'RedHat' : {
			$supported = true
		}
	}	

	if ($supported == true) {

		file { 'httpd_conf_d' :
			ensure 	=> directory,
        	path  	=> '/etc/httpd/conf.d/',
        	recurse => true,
        	purge   => true,
        	force   => true,
        	owner   => "root",
        	group   => "root",
        	mode    => 0644,
			require => Package['httpd'],
		}

		file { 'cloudstack_conf' :

			path	=> '/etc/httpd/conf.d/cloudstack.conf',
			owner 	=> root,
			group	=> root,
			mode 	=> '0644',
			content => template('apache/cloudstack.conf.erb'),
			require => File['httpd_conf_d'],
		}

        package { 'httpd' :
			ensure 	=> present,
		}

        package { 'mod_ssl' : 
			ensure 	=> present,
		}

      	service { 'httpd' :
       		ensure 	=> 'running',
       		enable 	=> true,
			require => File['cloudstack_conf'],
		}
	}
}
