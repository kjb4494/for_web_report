from urllib.request import urlopen
from bs4 import BeautifulSoup


class DescAndExampleCrawler:
    def __init__(self, tag, kind='element', att=None):
        self._crawled_string = ''
        self._desc_string = ''
        if kind == 'element':
            self._url = 'https://www.w3schools.com/tags/tag_' + tag + '.asp'
        elif kind == 'attr':
            self._url = 'https://www.w3schools.com/tags/att_' + tag + '_' + att + '.asp'
        self._start_crawlering()
        self._start_desc_crawlering()

    def _start_crawlering(self):
        try:
            html = urlopen(self._url)
            bs_object = BeautifulSoup(html, "html.parser")
            div = bs_object.find("div", {"class": "w3-code notranslate htmlHigh"}).text
            div = div.encode('utf-8')
            for i in range(5):
                div = div.replace(b'\xc2\xa0\xc2\xa0', b'\xc2\xa0')
                div = div.replace(b'  ', b' ')
                div = div.replace(b'\r\n', b'')
            div = div.replace(b'\xc2\xa0', b'\n')
            div = div.decode('utf-8')
            self._crawled_string = div
        except:
            self._crawled_string = ''

    def _start_desc_crawlering(self):
        try:
            html = urlopen(self._url)
            bs_object = BeautifulSoup(html, "html.parser")
            all_tags = bs_object.find_all()
            start_recoding = False
            for tag in all_tags:
                if start_recoding:
                    if tag.name != 'p' or 'Note:' in tag.text or 'Tip:' in tag.text or 'element:' in tag.text:
                        break
                    self._desc_string += tag.text + ' '
                if tag.text == 'Definition and Usage':
                    start_recoding = True
            self._desc_string = self._desc_string.encode('utf-8')
            self._desc_string = self._desc_string.replace(b'\r\n', b' ')
            self._desc_string = self._desc_string.replace(b'<', b'\'')
            self._desc_string = self._desc_string.replace(b'>', b'\'')
            for i in range(5):
                self._desc_string = self._desc_string.replace(b'  ', b' ')
            self._desc_string = self._desc_string.decode('utf-8')
        except:
            self._desc_string = ''

    def get_crawled_string(self):
        return self._crawled_string

    def get_desc_string(self):
        return self._desc_string


if __name__ == '__main__':
    ec = DescAndExampleCrawler('area')
    print(ec.get_desc_string())
