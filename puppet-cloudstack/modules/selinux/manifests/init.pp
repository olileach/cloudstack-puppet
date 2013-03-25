class selinux ( $mode ){

	 if ! ($mode in [ 'enforcing', 'permissive' , 'disable' ]) {
		fail('mode paramtermust be Enforcing, Permissive, Disable ')
	}

	include 'stdlib'

	if downcase($mode) == 'permissive' {
		$selinuxmode = '0'
	}
	elsif downcase($mode) == 'enforcing' {
		$selinuxmode = '1'
	}
	else {
		$selinuxmode = '0'
	}

	if $selinux_current_mode != $mode {

        exec { "set-selinux-mode" :
			command => "/usr/sbin/setenforce $selinuxmode && /bin/sed -ie 's/^SELINUX=.*/SELINUX=$mode/g' /etc/sysconfig/selinux",
		}
	}
}
