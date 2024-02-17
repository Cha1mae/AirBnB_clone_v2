#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            return {
                key: val for key, val in self.__objects.items()
                if isinstance(val, cls)
            }

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves the storage dictionary to a file"""
        with open(self.__file_path, 'w') as f:
            json.dump(
                {key: obj.to_dict() for key, obj in self.__objects.items()},
                f
            )

    def reload(self):
        """Loads the storage dictionary from a file"""
        try:
            classes = {
                'BaseModel': BaseModel, 'User': User, 'Place': Place,
                'State': State, 'City': City, 'Amenity': Amenity,
                'Review': Review
            }
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                self.__objects = {
                    key: classes[val['__class__']](**val)
                    for key, val in data.items()
                }
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes a given object if it exists."""
        if obj is not None:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Calls reload()"""
        self.reload()
