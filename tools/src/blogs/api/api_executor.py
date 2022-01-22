from typing import Optional, Callable

import requests
from requests import Response


def execute_get_api(url: str, headers: object,
                    response_resolver: Callable[[str, Response, str], Optional[str]]) -> Optional[str]:
    response = requests.get(url, headers=headers)
    return response_resolver('GET', response, url)


def execute_put_api(url: str, headers: object, body: object,
                    response_resolver: Callable[[str, Response, str], Optional[str]]) -> Optional[str]:
    response = requests.put(url, headers=headers, data=body)
    return response_resolver('PUT', response, url)


def execute_post_api(url: str, headers: object, body: object,
                     response_resolver: Callable[[str, Response, str], Optional[str]]) -> Optional[str]:
    response = requests.post(url, headers=headers, data=body)
    return response_resolver('POST', response, url)


def execute_delete_api(url: str, headers: object,
                       response_resolver: Callable[[str, Response, str], Optional[str]]) -> Optional[str]:
    response = requests.delete(url, headers=headers)
    return response_resolver('DELETE', response, url)
