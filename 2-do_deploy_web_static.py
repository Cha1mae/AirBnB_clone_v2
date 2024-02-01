#!/usr/bin/python3

"""
Fabric script that distributes an archive to my webserver
based on the first task
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['52.91.152.110', '52.87.152.252']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the web_static folder content

    Returns:
        str: Archive path or None otherwise.
    """
    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ap = f"versions/web_static_{timestamp}.tgz"
    ac = f"tar -cvzf {ap} web_static"
    result = local(ac)

    if result.failed:
        return None
    else:
        output = f"web_static packed: {ap} -> "
        output += f"{result.stdout.split()[-1]}Bytes"
        print(output)
        return ap


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


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        do_deploy(archive_path)
