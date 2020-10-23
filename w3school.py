import requests
import re
from bs4 import BeautifulSoup


class W3School:
    def __init__(self, element):
        url = 'https://www.w3schools.com/tags/tag_' + element + '.asp'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # example code
        example_div = soup.find('div', {'class': 'w3-example'})
        example_div = example_div.find('div', {'class': 'w3-code notranslate htmlHigh'})
        self.example = example_div.text.strip()

        # definition and usage
        is_crawling_mode = False
        description_parts = []
        for tag in soup.find_all():
            if is_crawling_mode and tag.name == 'p':
                description_part = self.remove_space_str(tag.text)
                description_parts.append(description_part)
            if is_crawling_mode and tag.name == 'hr':
                break
            if tag.name == 'h2' and tag.text == 'Definition and Usage':
                is_crawling_mode = True
        self.description = ' '.join(description_parts)

        # attribute
        self.attribute = {}
        is_crawling_mode = False
        for tag in soup.find_all():
            if is_crawling_mode and tag.name == 'table':
                trs = tag.find_all('tr')[1:]
                for tr in trs:
                    tds = tr.find_all('td')
                    attribute = tds[0].text
                    self.attribute.update({
                        attribute: {
                            'value': self.remove_space_str(tds[1].text).replace(' ', '|'),
                            'description': tds[2].text,
                            'example': self.get_attribute_example(attribute)
                        }
                    })
                break
            if tag.name == 'h2' and tag.text == 'Attributes':
                is_crawling_mode = True

    @staticmethod
    def remove_space_str(string):
        result = string.replace('\r', '').replace('\n', '')
        result = re.sub(' +', ' ', result)
        return result

    @staticmethod
    def get_attribute_example(attribute):
        url = 'https://www.w3schools.com/tags/att_' + attribute + '.asp'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        example_div = soup.find('div', {'class': 'w3-example'})
        example_div = example_div.find('div', {'class': 'w3-code notranslate htmlHigh'})

        return example_div.text.strip()
