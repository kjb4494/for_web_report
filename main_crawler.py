from urllib.request import urlopen
from bs4 import BeautifulSoup

from enum_pack import TableEnum
from filtering_helper import strip_html_tag, remove_globals_attribute
from attributes_dict import AttributesDict

excepted_elements = [
    # header
    'Element',
    'Description',
    'Categories',
    'Parents†',
    'Children',
    'Attributes',
    'Interface',
    # except tag
    # 1
    'html', 'head', 'base', 'title', 'body',
    # 2
    'br', 'p', 'hr', 'h1, h2, h3, h4, h5, h6', 'pre', 'blockquote', 'b', 'i',
    's', 'u', 'sup', 'sub', 'small', 'cite', 'code', 'samp', 'var', 'dfn',
    'em', 'strong', 'abbr', 'address', 'kbd', 'q', 'ul', 'ol', 'li', 'dl',
    'dt', 'dd', 'div', 'span',
    # 3
    'img', 'a', 'iframe',
    # 4
    'table', 'tr', 'td', 'th', 'caption', 'thread', 'tbody', 'tfoot', 'colgroup', 'col',
    # 5
    'audio', 'source', 'video', 'track', 'embed',
    # 6
    'form', 'input', 'button', 'textarea', 'select', 'option', 'datalist', 'optgroup',
    'fieldset', 'legend', 'label'
]

if __name__ == "__main__":
    html = urlopen("https://www.w3.org/TR/html5/fullindex.html")
    bs_object = BeautifulSoup(html, "html.parser")
    tables = bs_object.find_all('table')
    table_rows = tables[TableEnum.ELEMENTS].find_all("tr")

    index_count = 1
    attr_dict = AttributesDict()

    for row in table_rows:
        th_cells = row.find_all('th')
        td_cells = row.find_all("td")
        if not td_cells:
            continue
        cells = th_cells + td_cells
        att_element, att_description, att_categories, att_parentst, att_children, att_attributes, att_interface = cells
        striped_att_element = strip_html_tag(str(att_element))
        if striped_att_element in excepted_elements:
            continue
        striped_att_attributes = remove_globals_attribute(strip_html_tag(str(att_attributes)))
        striped_att_attributes = striped_att_attributes.split('; ')
        striped_att_description = strip_html_tag(str(att_description))

        print('{}. {}: {}'.format(str(index_count).zfill(3), striped_att_element, striped_att_description))
        print('- 속성', end='')
        if striped_att_attributes[0] == '':
            print(': 없음')
        else:
            print()
            for i, att_attribute in enumerate(striped_att_attributes, start=1):
                print('\t{}. {}: {}'.format(
                    str(i).zfill(2), att_attribute, attr_dict.get_description(att_attribute, striped_att_element)
                ))
                print('\t- 예시 ')
        print('- 예시')
        print()

        index_count += 1
