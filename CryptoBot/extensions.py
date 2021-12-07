from AppConfig import *
import requests
import json


class APIException(Exception):
    def __init__(self, text):
        self.description = text


class API_Connector():


    @staticmethod
    def get_values():
        r = requests.get(EX_BASE_URL + '/symbols', params={'access_key': EX_TOKEN})
        d = json.loads(r.content)
        if d['success']:
            return d['symbols']
        else:
            raise APIException('Ошибка API при запросе списка валют')


    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        amount = amount.replace(',','.')
        try:
            f = float(amount)
        except ValueError:
            raise APIException('Неверно указано сумма конвертируемой валюты\nНеобходимо указать числовое значение')
        else:
            if f <= 0:
                raise APIException('Сумма конвертируемой валюты должна быть выражена положительным числом')
            r = requests.get(EX_BASE_URL + '/latest', params={'access_key': EX_TOKEN, 'base':base, 'symbols':quote})
            d = json.loads(r.content)
            try:
                b = d['success']
            except KeyError:
                raise APIException('Ошибка при обращении к API:\n' + d['error']['code'] + '\n' + d['error']['message'])
            else:
                if d['success']:
                    p = d['rates'][quote]
                    return round(f * p, 2)
                else:
                    raise APIException('Ошибка при обращении к API:\n'+ d['error']['info'])