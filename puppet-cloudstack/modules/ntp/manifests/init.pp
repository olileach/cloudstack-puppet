# Class: ntp
#
#   This module manages the ntp service.
#
# Author: Oliver Leach
# Date  : 5th March 2013 
#
# Actions:
#  Installs, configures, and manages the ntp service. Uses OS specific erb templates
#
# Requires:
#  The following operating systems are supported. Debian, ubunut, centos, redhat, fedora, freebsd
#
# Sample Usage:
#
#   class { "ntp":
#     servers    => [ 'ntp.tcllab.co.uk' ],
#     autoupdate => false,
#   }
#
#   Note - the $server is a class parameter and therefore can be set at node the classification level
#          otherwise, the default servers_real value is specified.

class ntp($servers,
          $ensure='running',
          $autoupdate=false, ) {

  if ! ($ensure in [ 'running', 'stopped' ]) {
    fail('ensure parameter must be running or stopped')
  }

  if $autoupdate == true {
    $package_ensure = latest
  } elsif $autoupdate == false {
    $package_ensure = present
  } else {
    fail('autoupdate parameter must be true or false')
  }

  case $::operatingsystem {
    debian, ubuntu: {
      $supported  = true
      $pkg_name   = [ 'ntp' ]
      $svc_name   = 'ntp'
      $config     = '/etc/ntp.conf'
      $config_tpl = 'ntp.conf.debian.erb'
      if ($servers == undef) {
        $servers_real = [ 'server 0.pool.ntp.org iburst', ]
      } else {
        $servers_real = $servers
      }
    }
    centos, redhat, fedora: {
      $supported  = true
      $pkg_name   = [ 'ntp' ]
      $svc_name   = 'ntpd'
      $config     = '/etc/ntp.conf'
      $config_tpl = 'ntp.conf.el.erb'
      if ($servers == undef) {
        $servers_real = [ 'server 0.pool.ntp.org iburst', ]
      } else {
        $servers_real = $servers
      }
    }
    freebsd: {
      $supported  = true
      $pkg_name   = ['.*/net/ntp']
      $svc_name   = 'ntpd'
      $config     = '/etc/ntp.conf'
      $config_tpl = 'ntp.conf.freebsd.erb'
      if ($servers == undef) {
        $servers_real = [ 'server 0.pool.ntp.org iburst maxpoll 9', ]
      } else {
        $servers_real = $servers
      }
    }
    default: {
      $supported = false
      notify { "${module_name}_unsupported":
        message => "The ${module_name} module is not supported on ${::operatingsystem}",
      }
    }
  }

  if ($supported == true) {

    package { 'ntp':
      ensure => $package_ensure,
      name   => $pkg_name,
    }

    file { $config:
      ensure  => file,
      owner   => 0,
      group   => 0,
      mode    => '0644',
      content => template("${module_name}/${config_tpl}"),
      require => Package[$pkg_name],
    }

    service { 'ntp':
      ensure     => $ensure,
      name       => $svc_name,
      hasstatus  => true,
      hasrestart => true,
      subscribe  => [ Package[$pkg_name], File[$config] ],
    }
  }
}
