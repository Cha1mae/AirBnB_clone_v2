# puppet time 
# Nginx package installing
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

# mkdir si lmodir
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# the fake html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html><head></head><body>Holberton School Puppet</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# the links 
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# this will change the ownership
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Nginx update
file { '/etc/nginx/sites-available/default':
  content => template('/etc/nginx/nginx.conf'),
  notify  => Service['nginx'],
}

# Nginx is running
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
