#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            "City", backref="state", cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """returns list of Cities and some relationships"""
            cities_instances = []
            cities_dict = models.storage.all(models.City)
            for key, value in cities_dict.items():
                if self.id == value.state_id:
                    cities_instances.append(value)
            return cities_instances

    def to_dict(self):
        """Returns a dictionary representation of the State instance."""
        dict_representation = super().to_dict()
        dict_representation['__class__'] = self.__class__.__name__
        return dict_representation

    def __str__(self):
        """Returns a string representation of the State instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.to_dict()
        )
