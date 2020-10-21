from urllib.request import urlopen
from bs4 import BeautifulSoup

from enum_pack import TableEnum
from filtering_helper import strip_html_tag, remove_globals_attribute
from attributes_dict import AttributesDict

from desc_and_example_crawler import DescAndExampleCrawler
from trans_ko import google_trans_ko


excepted_elements = [
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

        ecm = DescAndExampleCrawler(striped_att_element)

        print('{}. {}\n{}\n{}'.format(
            str(index_count).zfill(3), striped_att_element, google_trans_ko(ecm.get_desc_string()), ecm.get_desc_string()
        ))
        print('- 속성', end='')
        if striped_att_attributes[0] == '':
            print(': 없음')
        else:
            print()
            for i, att_attribute in enumerate(striped_att_attributes, start=1):
                ec = DescAndExampleCrawler(striped_att_element, 'attr', att_attribute)
                print('{}. {}\n{}\n{}'.format(
                    str(i).zfill(2), att_attribute, google_trans_ko(ec.get_desc_string()), ec.get_desc_string()
                ))
                print('- 예시')
                print(ec.get_crawled_string())

        print('- 예시')
        print(ecm.get_crawled_string())
        print()

        index_count += 1
