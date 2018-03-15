#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import random
import json
import ast


class HttpReq:
    """
    This Class will help to try some HTTP requests.
    """
    def __init__(self):
        """
        It inits the HttpReq object.
        """
        self.url = None
        self.resp = None
        self.resp_content = None
        self.resp_text = None
        self.ua = None
        self.core_content = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = ''
        if self.url is not None:
            string += "\n- Entire url :\t" + self.url
            string += "\n- Domain :\t\t" + self.domain()
        if self.ua is not None:
            string += "\n- User-agent used :\t" + self.ua
        if self.core_content is not None:
            string += "- And here you'll find the core content :\n" + self.core_content

        if string == '':
            string = '\nNo items are printable..\nUse the class methods to build Http requests !\n'
        else:
            string = '\n*************************************************\n' +\
                     'Here are the attributes of your HttpReq object :\n' +\
                     string + \
                     '\n\n*************************************************\n'

        return string

    def get(self, url, headers, timeout=10, retry=3):
        """
        This method will build and send a HTTP request at the given url address.
        :param url: The url of the web page to reach.
        :param headers: The request header.
        :param timeout: timeout applied to the request.
        :param retry: maximum number of requests before return None.
        :return: the result of the request (could be 'None' is the serveur is
        unreachable).
        """
        self.url = str(url)

        try:
            headers['User-agent']
        except KeyError:
            self.change_ua()

        response = requests.get(url, headers=headers, timeout=timeout)
        if retry is -1:
            raise TimeoutError("The server is unreachable at the moment...")
        elif response is None:
            self.get(url, headers, timeout=timeout, retry=retry-1)
        else:
            if isinstance(response, dict):
                print("The response is in a JSON file format.")
            self.resp = response
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

    def soup(self):
        """
        This method returns the BeautifulSoup object linked to the response
        object obtained before, with 'get()' method.
        :return: the BeautifulSoup object associated to HttpReq obj.
        """
        return BeautifulSoup(self.resp_text, "lxml")

    def web_content(self):
        """
        simply returns the HttpReq's response content
        :return: the content.
        """
        return self.resp_content

    def response(self):
        return self.resp

    def change_ua(self):
        """
        This method will permit to change the used User-agent for requests.
        :return: nothing
        """
        rand = random.randint(1, 31)
        ua = ""
        with open("User-agents.txt", 'r') as f:
            for line in range(rand):
                ua = f.readline()
        self.ua = ua

    def process_core_content(self, soup_obj, create_file=False):
        """
        If the items exist : all h1, Titles and links are stored in a JSON object,
        created in local directory.
        :return: nothing.
        """
        links = []
        for link in soup_obj.find_all('a'):
            ref = link.get('href')
            if ref is not None:
                if len(ref) > 0:
                    if ref[0] == 'h':
                        links.append(ref)

        titles = []
        for link in soup_obj.find_all('title'):
            title = link.string
            if len(title) > 0:
                titles.append(title)

        h1 = []
        for h in soup_obj.find_all('h1'):
            h = h.string
            if len(h) > 0:
                h1.append(h)

        main_text = []
        for text in soup_obj.find_all('p'):
            if text is not None:
                text = self.del_string_spaces(str(text.next_element))
                if len(text) > 0:
                    main_text.append(text)

        interesting_values = {
            'titles': titles,
            'h1': h1,
            'links': links,
            'main_text': main_text
        }

        self.core_content = json.dumps(interesting_values)

        if create_file:
            print("\nYou have selected the parameter create_file at True."
                  "\nSo a Json file containing the core content is generating..")
            with open('core_content.json', 'w') as fp:
                json.dump(interesting_values, fp)
                print('\nJSON file created  !\nName : "core_content.json"')
        else:
            print("\nParameter create_file has been set to False."
                  "\nSo the Json file containing the core content won't be generated")

    def get_core_content(self, soup_obj=None, create_file=False):
        """
        This method permits to get the core content in a JSON object.
        'Core' means : h1, titles, links and main text.
        :param soup_obj: the soup object containing the website text.
        :param create_file: If we want to generate the json file in the
        current directory.
        :return: the core content in a JSON object.
        """
        if self.core_content is None:
            if soup_obj is not None:
                self.process_core_content(soup_obj=soup_obj, create_file=create_file)
            else:
                print("You must specify a soup object when calling this method.")
        return ast.literal_eval(self.core_content)

    @staticmethod
    def del_string_spaces(a_string):
        """
        Deletes all the extra spaces in the string in parameter before
        returning it.
        :param a_string: the string we want to delete the extra spaces in.
        :return: the same string without the extra spaces.
        """
        return_string = a_string.strip()
        return "".join(return_string)

