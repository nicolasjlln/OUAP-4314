import Introduction_Exercice3 as ex3

test = ex3.HttpReq()

headers = {}
url = "http://www.lemonde.fr/les-decodeurs/article/2018/03/14/ce-que-les-travaux-de-stephen-hawking-ont-apporte-a-la-physique_5271032_4355770.html"

test.get(url=url, headers=headers)
print(test)

test.clear_url()
test.format()
soup = test.soup()

test.get_core_content(soup, create_file=True)
print(test)

content = test.get_core_content()
print(content)


