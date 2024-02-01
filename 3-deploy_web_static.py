#!/usr/bin/python3

"""
Fabric script that distributes an archive to my webserver
based on the first task and the second
"""

from fabric.api import env, run
from os.path import exists
from datetime import datetime
from fabric.api import local, put

env.hosts = ['52.91.152.110', '52.87.152.252']
env.user = 'ubuntu'


def do_pack():
    """
    Creates a tar archive of the web_static folder

    Returns:
        str: Path of the created archive, or None if unsuccessful
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to my WS (web server)

    Args:
        archive_path (str): Path to the archive

    Returns:
        bool: True if all good or otherwise False
    """
    if not exists(archive_path):
        return False

    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]

        # Uploading archive to /tmp/
        if put(archive_path, "/tmp/{}".format(file)).failed:
            return False

        # Removing existing release directory
        if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
            return False

        # Creating new release directory
        if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
            return False

        # Extracting archive to new release directory
        if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
               .format(file, name)).failed:
            return False

        # Cleaning up /tmp/
        if run("rm /tmp/{}".format(file)).failed:
            return False

        # Moving contents to release directory
        if run("mv /data/web_static/releases/{}/web_static/* "
               "/data/web_static/releases/{}/".format(name, name)).failed:
            return False

        # Cleaning up old web_static directory
        if run("rm -rf /data/web_static/releases/{}/web_static"
               .format(name)).failed:
            return False

        # Updating the symbolic link
        if run("rm -rf /data/web_static/current").failed:
            return False

        if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
               .format('test')).failed:
            return False

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Creates and distributes an archive to my WS (web server)

    Returns:
        bool: True if all operations were successful, or False otherwise
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
