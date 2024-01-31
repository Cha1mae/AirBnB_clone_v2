#!/usr/bin/env bash
# this sets up the web servers for the deployment of web_static

# i do have nginx but just to be sure
sudo apt-get update
sudo apt-get -y install nginx

# hope this will create the files asked for
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# this will create the fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu
sudo chown -R ubuntu:ubuntu /data/

# this update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/location \/hbnb_static {/!b;n;c\\talias /data/web_static/current/;' "$config_file"

# Restarting Nginx ofc
sudo service nginx restart

# Exiting successfully
exit 0
