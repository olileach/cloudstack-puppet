# ntp

Manages ntp configuration and ntp service via Puppet

## Usage

### Install ntp. Parameters can be specified

```
   class { "ntp":
     servers    => [ 'ntp.tcllab.co.uk' ],
     autoupdate => false,
   }
```

## Additional class parameters
* servers parameters can be specified at node classfication level
