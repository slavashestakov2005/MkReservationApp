from ..config import Config
from requests import post
from hashlib import sha256
from ..database import Visitor


class TinkoffCard:
    @staticmethod
    def __eval_hash(data: map):
        data['Password'] = Config.TERMINAL_PASSWORD
        data = sorted(data.items())
        result = ''
        for item in data:
            result += str(item[1])
        return sha256(result.encode()).hexdigest()

    @staticmethod
    def __do_post(url: str, data: map):
        data['TerminalKey'] = Config.TERMINAL_KEY
        data['Token'] = TinkoffCard.__eval_hash(data)
        response = post(Config.TINKOFF_API_URL + url, json=data)
        return response.json()

    @staticmethod
    def __gen_order_id(visitor: int):
        res = str(visitor)
        return "0" * (36 - len(res)) + res

    @staticmethod
    def __gen_url(url: str, visitor: int):
        return Config.SITE_URL + url + '?id=' + str(visitor)

    @staticmethod
    def __gen_result(data, *args):
        error = data['ErrorCode']
        ans = [error]
        for arg in args:
            ans.append(data[arg] if error == '0' else None)
        return ans

    @staticmethod
    def receipt(cost: int, visitor: int, description: str):
        data = {'Amount': cost * 100, 'OrderId': TinkoffCard.__gen_order_id(visitor), 'Description': description,
                'SuccessURL': TinkoffCard.__gen_url('t_success', visitor),
                'FailURL': TinkoffCard.__gen_url('t_fail', visitor)}
        data = TinkoffCard.__do_post('Init', data)
        return TinkoffCard.__gen_result(data, 'PaymentURL', 'PaymentId')

    @staticmethod
    def get_state(payment: int):
        data = {'PaymentId': payment}
        data = TinkoffCard.__do_post('GetState', data)
        return TinkoffCard.__gen_result(data, 'Status')

    @staticmethod
    def get_status(status):
        if status in Config.PAID_STATES:
            return Visitor.PAID
        elif status in Config.NOT_PAID_STATES:
            return Visitor.NOT_PAID
        return None
