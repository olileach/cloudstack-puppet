# ntp

Manages ntp configuration and ntp service via Puppet

## Usage

### Install ntp. Parameters can be specified

```
   class { "ntp":
     servers    => [ 'myntpserver.com' ],
     autoupdate => false,
   }
```

## Additional class parameters
* servers parameters can be specified at node classfication level
