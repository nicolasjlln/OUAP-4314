#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


def get(url, headers, timeout=10, retry=3):
    """
    This method will build and send a HTTP request at the given url address.
    :param url: The url of the web page to reach.
    :param headers: The request header.
    :param timeout: timeout applied to the request.
    :param retry: maximum number of requests before return None.
    :return: the result of the request (could be 'None' is the serveur is
    unreachable).
    """
    response = requests.get(url, headers=headers, timeout=timeout)
    if retry is -1:
        raise TimeoutError("The server is unreachable at the moment...")
    elif response is None:
        get(url, headers, timeout=timeout, retry=retry - 1)
    else:
        return response


headers = {
    'Origin': 'https://www.qwant.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://www.qwant.com/',
    'Connection': 'keep-alive',
}


test = get("https://api.qwant.com/api/search/all?count=10&q=recherche", headers=headers)

with open('JSON_ex4.json', 'w') as fp:
    json.dump(test.json(), fp)
