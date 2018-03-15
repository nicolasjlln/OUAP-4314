#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class HttpReq:
    """
    This Class will help to try some HTTP requests.
    """
    def __init__(self):
        """
        It inits the HttpReq object.
        """
        self.url = None
        self.resp_content = None
        self.resp_text = None
        self.ua = None
        self.core_content = None

    def get(self, url, timeout=10, retry=3):
        """
        This method will build and send a HTTP request at the given url address.

        :param url: The url of the web page to reach.
        :param timeout: timeout applied to the request.
        :param retry: maximum number of requests before return None.
        :return: the result of the request (could be 'None' is the serveur is
        unreachable).
        """
        self.url = str(url)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X "\
        "1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95"\
        " Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=timeout)
        if retry is -1:
            raise TimeoutError("The server is unreachable at the moment...")
        elif response is None:
            self.get(url, timeout=timeout, retry=retry-1)
        else:
            self.resp_content = str(response.content)
            self.resp_text = str(response.text)
