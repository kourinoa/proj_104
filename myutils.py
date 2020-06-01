import requests


def get_session() -> requests.session:
    return requests.session()
