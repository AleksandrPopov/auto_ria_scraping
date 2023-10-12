import re
import requests


def validate_request(url: str):
    try:
        response = requests.get(url=url)
        return response if response.status_code == 200 else None
    except Exception as e:
        print(e)


def format_phone_number(phone_list: list) -> list:
    return ["+38" + re.sub(r'\D', '', i) for i in phone_list]
