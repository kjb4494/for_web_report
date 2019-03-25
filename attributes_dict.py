from urllib.request import urlopen
from bs4 import BeautifulSoup

from enum_pack import TableEnum
from filtering_helper import strip_html_tag

search_limit_count = 10

class AttributesDict:
    def __init__(self):
        self._attr_dict = {}
        self._create_attr_dict()

    def _create_attr_dict(self):
        html = urlopen("https://www.w3.org/TR/html5/fullindex.html")
        bs_object = BeautifulSoup(html, "html.parser")
        tables = bs_object.find_all('table')
        table_rows = tables[TableEnum.ATTRIBUTES].find_all("tr")
        overlap_index = 2
        for row in table_rows:
            th_cells = row.find_all('th')
            td_cells = row.find_all('td')
            if not td_cells:
                continue
            cells = th_cells + td_cells
            att_attributes, att_elements, att_description, att_value = cells
            striped_att_attributes = strip_html_tag(str(att_attributes))
            if striped_att_attributes in self._attr_dict:
                striped_att_attributes += str(overlap_index)
                overlap_index += 1
            else:
                overlap_index = 2
            self._attr_dict.update({
                striped_att_attributes: {
                    'elements': strip_html_tag(str(att_elements)).split('; '),
                    'description': strip_html_tag(str(att_description)),
                    'value': strip_html_tag(str(att_value))
                }
            })

    def get_description(self, attr_name, element):
        if element in self._attr_dict.get(attr_name).get('elements'):
            return self._attr_dict.get(attr_name).get('description')
        else:
            for i in range(2, search_limit_count):
                indexed_attr_name = attr_name + str(i)
                if element in self._attr_dict.get(indexed_attr_name).get('elements'):
                    return self._attr_dict.get(indexed_attr_name).get('description')
