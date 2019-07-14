__author__ = 'Jakub Rachwalski'

from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type, Dict, Union
from common.database import Database


T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *arg, **kwargs):
        pass

    @abstractmethod
    def json(self) -> Dict:
        return asdict(self)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    def save_to_mongo(self):
        jason = self.json()
        del jason["collection"]
        Database.update(self.collection, {"_id": self._id}, jason)

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        element_from_db = Database.find_one(cls.collection, {attribute: value})
        return cls(**element_from_db)

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {attribute: value})
        return [cls(**elem) for elem in elements_from_db]
