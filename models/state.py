#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", backref="state", cascade="all, delete-orphan"
    )

    def to_dict(self):
        """wa kanghwt wa 3yit"""
        dict_representation = super().to_dict()
        dict_representation['__class__'] = self.__class__.__name__
        return dict_representation

    def __str__(self):
        """ i added this in hopes of winning"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.to_dict()
        )
