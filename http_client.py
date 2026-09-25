import requests


def get(url, params=None, timeout=10):
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response


def post(url, json=None, timeout=10):
    response = requests.post(url, json=json, timeout=timeout)
    response.raise_for_status()
    return response
