

__author__ = 'Jakub Rachwalski'


# item = Item (URL, tag_name, query )
# item.load_price()
# item.save_to_mongo()
# items_loaded = Item.all()
# items_loaded[0]

from typing import Dict
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, asdict
import requests
import re
import uuid
from models.model import Model
# from common.database import Database


@dataclass(eq=False)
class Item(Model):

    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:

        print(type(self.query))

        response = requests.get(self.url)

        content = response.content

        soup = BeautifulSoup(content, "html.parser")
        # print(soup)

        element = soup.find(self.tag_name, self.query)
        # print(self.tag_name)
        # print(self.query)
        # print(element)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d*,?\d+[\.,]\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        if '.' in found_price:
            without_coma = found_price.replace(",", "")
        else:
            without_coma = found_price.replace(",", ".")

        self.price = float(without_coma)

        return self.price

    def json(self) -> Dict:
        return asdict(self)

#        jason = {
#            "_id": self._id,
#            "url": self.url,
#            "tag_name": self.tag_name,
#           "query": self.query
#
#        }
#        # print(jason)
#
#        return jason
