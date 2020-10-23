from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from enums import ELEMENTS, ATTRIBUTES


# JS로 동적 렌더링 하는듯... 로딩을 위해 selenium 사용
DRIVER_PATH = './chromedriver'
URL = 'https://html.spec.whatwg.org/multipage/indices.html'


def get_parsed_html() -> BeautifulSoup:
    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument('headless')

    print('web page loading... wait until parsing is completed...')
    driver = webdriver.Chrome(DRIVER_PATH, options=driver_option)
    driver.implicitly_wait(10)
    driver.get(URL)
    req = driver.page_source
    print('parsing complete.')

    soup = BeautifulSoup(req, 'html.parser')
    print('html code is translated by bs4.')

    driver.quit()
    print('quit chrome driver.')

    return soup


def get_elements_dictionary(table: Tag, targets: list) -> dict:
    elements = {}
    for tr in table.tbody.find_all('tr'):
        element = tr.th.text

        if element not in targets:
            continue

        tds = tr.find_all('td')
        elements.update({
            element: {
                'description': tds[ELEMENTS.DESCRIPTION.value].text.strip(),
                'categories': [category.text for category in tds[ELEMENTS.CATEGORIES.value].find_all('a')],
                'parents': [parent.text for parent in tds[ELEMENTS.PARENTS.value].find_all('a')],
                'children': [child.text for child in tds[ELEMENTS.CHILDREN.value].find_all('a')],
                'attributes': [attribute.text for attribute in tds[ELEMENTS.ATTRIBUTES.value].find_all('a')
                               if attribute.text != 'globals'],
                'interface': [interface.text for interface in tds[ELEMENTS.INTERFACE.value].find_all('a')]
            }
        })
    return elements


def get_attributes_dictionary(table: Tag, targets: list) -> dict:
    attributes = {}
    for tr in table.tbody.find_all('tr'):
        attribute = tr.th.code.text

        if attribute not in targets:
            continue

        tds = tr.find_all('td')
        attributes.update({
            attribute: {
                'elements': [element.text for element in tds[ATTRIBUTES.ELEMENTS.value].find_all('a')],
                'description': tds[ATTRIBUTES.DESCRIPTION.value].text.strip()
            }
        })
    return attributes
