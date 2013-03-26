# nfs

Manages and installs nfs with optional paramters via Puppet

## Usage

### Install nfs config file

```
    class { 'nfs': 

        $::nfsaccess = '/nfs' }
```

### parameters

* nfsaccess  - IP address of allow servers, i.e * for all or 10.0.0.1 for specific IP or network 10.0.0.0/24
* nfsfolder  - The nfs share point on the file system, e.g. /nfs or /secondarystorage
* auotupdate - Specify whther you would like to autoupdate the nfs packge, or stick with the present one available
