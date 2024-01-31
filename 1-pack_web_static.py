#!/usr/bin/python3
"""
This is a fabric script to generate a .tgz archive from the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the web_static folder content

    Returns:
        str: Archive path or None otherwise.
    """
    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"
    archive_command = f"tar -cvzf {archive_path} web_static"
    result = local(archive_command)

    if result.failed:
        return None
    else:
        output = f"web_static packed: {archive_path} -> "
        output += f"{result.stdout.split()[-1]}Bytes"
        print(output)
        return archive_path
