# Install Nginx package
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

# Create required directories
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
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

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html><head></head><body>Holberton School Puppet</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/index.html',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Change ownership of /data/ recursively
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => template('/etc/nginx/nginx.conf'),
  notify  => Service['nginx'],
}

# Ensure Nginx service is running
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
