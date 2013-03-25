class mysqldb ( $user, $password, $mysql_password) {

	exec { "create-${name}-db":
    	unless  => "/usr/bin/mysql -u${user} -p${password} ${name}",
    	command => "/usr/bin/mysql -uroot -p${mysql_password} -e \"create database ${name}; grant all on ${name}.*
    				to ${user}@localhost identified by '$password'; flush privileges;\"",
    	require => Service["mysqld"],
    }
}
