#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    print("Using DBStorage")
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    print("Using FileStorage")
    storage = FileStorage()

storage.reload()
