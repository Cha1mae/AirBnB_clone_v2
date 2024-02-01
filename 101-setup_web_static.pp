# pp file adhearing to task 0

# updating tha package
exec {'update':
  command  => 'sudo apt-get -y update',
  path     => '/usr/bin',
  logoutput => true,
}

# Nginx instalation or update
exec {'install nginx':
  command  => 'sudo apt-get -y install nginx',
  path     => '/usr/bin',
  logoutput => true,
  require  => Exec['update'],
}

# is Nginx running
service {'nginx':
  ensure    => 'running',
  enable    => true,
  require   => Exec['install nginx'],
}

# mkdir
file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# silmodir rawr
file {'/data/web_static/shared/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file {'/data/web_static/releases/test/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# fake friends i mean html link
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html><head></head><body>Holberton School</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# simbahlik link
file {'/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# confugring nginx
exec {'serve current to hbnb_static':
  command => 'echo -e "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tautoindex off;\n\t}" | sudo tee -a /etc/nginx/sites-available/default',
  path    => '/usr/bin',
  require => File['/data/web_static/current'],
  notify  => Exec['restart nginx'],
}

# restarting nginx
exec {'restart nginx':
  command     => 'sudo service nginx restart',
  path        => '/usr/bin',
  refreshonly => true,
}
