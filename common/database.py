__author__ = 'Jakub Rachwalski'

from typing import Dict
import pymongo
import os

class Database:
    URI = os.environ.get('MONGOLAB_URI', None)
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert( collection: str,data: Dict ):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> Dict:
        return Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)
