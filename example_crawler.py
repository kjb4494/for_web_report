from urllib.request import urlopen
from bs4 import BeautifulSoup


class ExampleCrawler:
    def __init__(self, tag):
        self._crawled_string = ''
        self._url = 'https://www.w3schools.com/tags/tag_' + tag + '.asp'
        self._start_crawlering()

    def _start_crawlering(self):
        html = urlopen(self._url)
        bs_object = BeautifulSoup(html, "html.parser")
        example_div = bs_object.find_all("div", {"class": "w3-code notranslate htmlHigh"})[0].text
        example_div = example_div.replace('\n', '')
        example_div = example_div.replace('\r', '')
        for i in range(5):
            example_div = example_div.replace('  ', ' ')
        example_div = example_div.replace('>', '>\n')
        for i in range(5):
            example_div = example_div.replace(' <', '<')
        self._crawled_string = example_div

    def get_crawled_string(self):
        return self._crawled_string
