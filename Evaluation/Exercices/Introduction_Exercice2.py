#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re


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

        headers = {'User-Agent': self.change_ua()}
        response = requests.get(url, headers=headers, timeout=timeout)
        if retry is -1:
            raise TimeoutError("The server is unreachable at the moment...")
        elif response is None:
            self.get(url, timeout=timeout, retry=retry-1)
        else:
            self.resp_content = str(response.content)
            self.resp_text = str(response.text)

    def clear_url(self):
        """
        This method will delete every useless spaces in the giver url.
        """
        self.resp_content = self.del_string_spaces(self.resp_content)

    def format(self):
        """
        This method will only save the alphanumerical characters in the http
        response previously requested with method '.get()'
        """
        resp_cleaned = ''
        for character in self.resp_content:
            if character.isalnum():
                resp_cleaned += character
            else:
                resp_cleaned += ' '
        self.resp_content = resp_cleaned

    def domain(self):
        """
        This method will return the domain name from the url given in 'get()'
        methode. The proess uses Regular Expressions.
        :return: url domain name.
        """
        reg = re.compile("(https://)?(http://)?(www.)?(fr.)?"
                         "([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3})(\/\S*)?")
        match = reg.match(self.url)
        return_str = ""
        if match.group(3) is not None:
            return_str += match.group(3) if not None else ""
        if match.group(4) is not None:
            return_str += match.group(4) if not None else ""
        return_str += match.group(5) if not None else ""
        return return_str

