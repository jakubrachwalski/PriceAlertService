__author__ = 'Jakub Rachwalski'

from typing import Dict
import uuid
import re
from models.model import Model
from dataclasses import dataclass, field, asdict


@dataclass(eq=False)
class Store(Model):

    collection: str = field(default="stores", init=False)
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return asdict(self)


#    def json(self) -> Dict:
#
#        jason = {
#            "_id": self._id,
#            "name": self.name,
#            "url_prefix": self.url_prefix,
#            "tag_name": self.tag_name,
#            "query": self.query
#        }
#        # print(jason)
#        return jason

    @classmethod
    def get_by_name(cls, store_name: str) -> 'Store':
        return cls.find_one_by('name', store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> 'Store':
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by('url_prefix', url_regex)

    @classmethod
    def get_by_url(cls, url: str) -> 'Store':
        url_regex = re.compile(r"(https?://.*?/)")
        match = url_regex.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
