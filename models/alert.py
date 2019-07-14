__author__ = 'Jakub Rachwalski'


# from common.database import Database
from typing import Dict
from dataclasses import dataclass, field, asdict
import uuid
from models.model import Model
from models.item import Item
from models.user import User
from libs.mailgun import Mailgun
from dotenv import load_dotenv
import os


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    item_name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.get_by_email(self.user_email)

    def json(self) -> Dict:
        return asdict(self)

#    def json(self) -> Dict:
#        return {
#            "_id": self._id,
#            "item_id": self.item_id,
#            "price_limit": self.price_limit,
#        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):

        # print(self.item.price)
        # print(self.price_limit)

        if self.item.price < self.price_limit:
            load_dotenv()
            from_email = os.environ.get('FROM_EMAIL', None)

            response = Mailgun.send_mail(
                [f"{from_email}"],
                f"Notification for {self.item_name}",
                f"Price of {self.item_name} has dropped below {self.price_limit}! Latest price: {self.item.price}. Go to this address to check your item: {self.item.url}.",
                f'<p>Price of {self.item_name} has dropped below {self.price_limit}! </p><p>Latest price: {self.item.price}. </p><p>Go to <a href="{self.item.url}">this</a. address to check your item.</p>'
            )
            print(response)
