#!/usr/bin/python3

"""
Fabric script that distributes an archive to my webserver
based on the first task
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime
from 1-pack_web_static.py import do_pack

env.hosts = ['<web-01 IP>', '<web-02 IP>']
env.user = 'ubuntu'


def do_deploy(ap):
    """
    Distributes an archive to my WS (web server)

    Args:
        ap (str): Path to the archive

    Returns:
        bool: True if all good or otherwise False
    """
    if not exists(ap):
        return False

    try:
        put(ap, "/tmp/")
        archive_name = ap.split("/")[-1]
        base_path = "/data/web_static/releases/"
        archive_base = archive_name.split(".")[0]
        release_path = base_path + archive_base
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))
        run("rm /tmp/{}".format(archive_name))
        mv_command = "mv {}/web_static/* {}".format(
            release_path, release_path
        )
        run(mv_command)
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    ap = do_pack()
    if ap:
        do_deploy(ap)
