import requests

__all__ = ['Client']


class Client:
    @staticmethod
    def send(data: dict):
        url = "https://calant.azurewebsites.net/api/leadin/index.php"
        params = \
            {
                'name': '1',
                'phone': data['phone'],
                'tax': '1'
            }
        requests.post(url=url, json=params)