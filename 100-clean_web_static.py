#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run
from datetime import datetime
from fabric.decorators import runs_once

env.hosts = ['<52.91.152.110>', '<52.87.152.252>']
env.user = 'ubuntu'


@runs_once
def do_clean(number=0):
    """
    Deletes unnecessary cash

    Args:
        number (int): Number of archives i want kept

    Returns:
        None
    """
    try:
        number = int(number)
        if number < 0:
            return

        # Local cleanup on the machine
        local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

        # Remote cleanup on the  web servers
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}"
            .format(number + 1))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    do_clean()