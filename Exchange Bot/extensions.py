import json
import requests
from config import keys

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Currency {base} is not found!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Currency {quote} is not found!")

        if base_key == quote_key:
            raise APIException(f'It is not possible to convert the same currency {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'The amount can not be processed {amount}!')
        
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        resp = json.loads(r.content)[quote_key]
        total = resp * amount
        total = round(total, 3)
        message = f"The exchange of {amount} {base} in {quote} is {total}"
        return message
