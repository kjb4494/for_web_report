from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

if __name__ == "__main__":
    html = urlopen("https://www.w3.org/TR/html5/fullindex.html#index-elements")
    bsObject = BeautifulSoup(html, "html.parser")

    except_tag_list = [
        'Element',
        'Description',
        'Categories',
        'Parents†',
        'Children',
        'Attributes',
        'Interface'
    ]
    seleted_tag = ""
    for th in bsObject.table.find_all('th'):

        seleted_tag += re.sub('<.+?>', '', str(th), 0).strip() + '\n'
    print(seleted_tag)
