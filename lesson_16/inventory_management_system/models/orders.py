import re

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .goods import Good


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    good_num = Column(Integer, ForeignKey("good.id"), nullable=False)
    good = relationship("Good")

    @classmethod
    def add(
        cls,
        name: str,
        address: str,
        notes: str,
        email: str,
        status: str,
        good_id: str,
        session: object,
    ):
        """Method recieves order data, session object. Requests good by id
        and adds order to DB
        """
        cls.__validate_data(name, address, email, status)

        session.add(
            Order(
                full_name=name,
                address=address,
                notes=notes,
                email=email,
                status=status,
                good_num=good_id,
            )
        )

    @classmethod
    def get_info(cls, id: int, session: object) -> dict:
        """Method recieves order id, requests it.
        Creates dictionary of the order data and returns it.
        """
        order = (
            session.query(Order)
            .filter_by(id=id)
            .join(Good, Good.id == Order.good_num)
            .first()
        )

        json_data = {
            "id": order.id,
            "name": order.full_name,
            "address": order.address,
            "notes": order.notes,
            "email": order.email,
            "status": order.status,
            "good": order.good.name,
            "good_id": order.good.id,
        }
        return json_data

    @classmethod
    def get_order_by_id(cls, id: int, session: object) -> object:
        """Method recieves object id, requests object and returns it"""
        order = session.query(Order).filter_by(id=id).first()
        return order

    @staticmethod
    def __validate_data(name, address, email, status):
        if name == "" or address == "" or email == "" or status == "":
            raise ValueError("Error: an empty field is prohibited")
        elif not re.match(r"^[-\w\.]+@[-\w\.]+\.[-\w]+$", email):
            raise ValueError("Email must contain 'a-z', 'A-Z', '0-9','@', '_.'")

    def update(
        self,
        name: str,
        address: str,
        notes: str,
        email: str,
        status: str,
        good_id: int,
        session: object,
    ):
        """Method recieves new order data, requests good
        and updates order record
        """
        self.__validate_data(name, address, email, status)

        session.query(Order).filter_by(id=self.id).update(
            {
                "full_name": name,
                "address": address,
                "notes": notes,
                "email": email,
                "status": status,
                "good_num": good_id,
            }
        )

    def delete(self, session: object):
        session.query(Order).filter_by(id=self.id).delete()
