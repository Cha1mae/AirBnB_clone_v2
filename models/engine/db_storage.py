#!/usr/bin/python3
"""Module for DBStorage class"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base


def get_classes():
    global classes
    if classes is None:
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
    return classes


class DBStorage:
    """Database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Current database session"""
        from models import classes
        objects = {}
        if cls:
            query = self.__session.query(get_classes()[cls])
            for obj in query.all():
                key = "{}.{}".format(cls, obj.id)
                objects[key] = obj
        else:
            for clss in get_classes():
                query = self.__session.query(get_classes()[clss])
                for obj in query.all():
                    key = "{}.{}".format(clss, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
