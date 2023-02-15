from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime, date
import numpy as np
     

class itemProperty():
    brand: str
    item_type: str
    item_category: str
    price: float
    expired_date: int

    def __init__(self, brand: str, item_type: str, item_category: str, price: float, expired_date: str) -> None:

        self.brand = brand
        self.item_type = item_type
        self.item_category = item_category
        self.price = price
        self.expired_date = expired_date

    @property
    def expired_date(self) -> date:
        return self._expired_date

    @expired_date.setter
    def expired_date(self, value: str):
        if value == None:
            self._expired_date = 'No Expired Date'
            return self._expired_date
        else:
            date_obj = datetime.strptime(value, '%Y-%m-%d').date()
            self._expired_date = date_obj
            return self._expired_date


class shoppingCart():
    def __init__(self) -> None:
        self.dict_item = {}

    def add_item(self, brand: str, item_type: str, item_category: str, price: float, expired_date: date) -> None:
        self.dict_item[brand] = itemProperty(brand, item_type, item_category, price, expired_date)

    def remove_item(self, brand: str):
        del self.dict_item[brand]

    def print_list(self) -> None:
        for k, v in self.dict_item.items():
            print(f'Brand: {k}')
            print(f'Item Type: {v.item_type}')
            print(f'Item Category: {v.item_category}')
            print(f'Item Price in Rupiah: {v.price}')
            print(f'Expiration Date: {v.expired_date}')
            print('')


class Payment(ABC):
    # Find the importance of class variable over instance attributes
    def __init__(self, cart: shoppingCart) -> None:
        self.cart = cart

    def total_price(self) -> float:
        list_prices = [val.price for val in self.cart.dict_item.values()]
        return np.sum(list_prices)

    @abstractmethod
    def transaction(self):
        pass

    @abstractmethod
    def discount(self):
        pass

    def payment_process(self) -> float:
        self.transaction()
        print(f'Payment in progress...')
        gross_price = self.total_price()
        net_price = self.discount(gross_price)
        print(f'Payment Successful')
        return int(gross_price), int(net_price)

    def Pay(self):
        gross_price, net_price = self.payment_process()

        print('=========================================')
        print('Receipt')

        for i, k in enumerate(self.cart.dict_item):
            print(f'{i+1}. Brand: {k:<20}{self.cart.dict_item[k].price:>10}')

        print('=========================================')
        print(f"{'Total price before discount':<20}{gross_price:>13}")
        print(f"{'Total price after discount':<20}{net_price:>14}")
            


class CashPayment(Payment):
    def transaction(self) -> None:
        print('Paying with cash...')

    def discount(self, total_price: float) -> float:
        net_prices = total_price
        return net_prices


class CreditPayment(Payment):
    def transaction(self) -> None:
        print('Paying with credit card...')

    def discount(self, total_price: float) -> float:
        net_prices = total_price * (1 - 0.7)
        return net_prices


cart1 = shoppingCart()
cart1.add_item('Lifeboy', 'Shampoo', 'Cosmetics', 15_000, '2024-05-28')
cart1.add_item('Chimory Yogurt', 'Yogurt', 'Food and Drinks', 8_500, '2026-01-03')
cart1.add_item('Nivea', 'Deodorant', 'Cosmetics', 15_000, None)

pay1 = CreditPayment(cart1)
pay1.Pay()
