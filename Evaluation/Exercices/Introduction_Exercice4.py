#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Introduction_Exercice3 as ex3

test = ex3.HttpReq()

print(test)

test.get("https://www.github.com/")
print(test.resp_content[0:100])

test.clear_url()
print(test.resp_content[0:100])

test.format()
print(test.resp_content[0:100])

soup = test.soup()
test.get_core_content(soup, create_file=True)

print(test)
