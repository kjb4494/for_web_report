# 각 요소는 1번부터 번호를 매겨 정리한다.
# 각 요소에 대해서 정리할 내용으로 요소의 기능, 주요 속성, 그리고 간단한 활용 예시는 반드시 포함해야 한다.
# 속성이 없는 경우에는 속성 설명은 생략된다.
# 활용 예시에는 해당 요소와 주요 속성들의 사용 방법을 간단한 설명하는 정도의 예시를 포함한다.
# 요소의 속성 설명에는 기본적으로 전역 속성은 포함하지 않는다.

import crawler
import data_processor
from enums import Index
from w3school import W3School

TARGET_ELEMENTS_LIST = ['a', 'img', 'br', 'address']


def get_reports():
    soup = crawler.get_parsed_html()
    tables = soup.find_all('table')
    elements_table = tables[Index.ELEMENTS.value]
    elements_dictionary = crawler.get_elements_dictionary(elements_table, TARGET_ELEMENTS_LIST)

    target_attributes_list = data_processor.combine_list(
        *[element_info['attributes'] for element_name, element_info in elements_dictionary.items()]
    )

    attributes_table = tables[Index.ATTRIBUTES.value]
    attributes_dictionary = crawler.get_attributes_dictionary(attributes_table, target_attributes_list)

    for idx, element in TARGET_ELEMENTS_LIST:
        pass


def test_code():
    test_tag = W3School('datalist')
    print(test_tag.description)
    print('---')
    print(test_tag.example)
    print('---')
    print(test_tag.attribute)


if __name__ == '__main__':
    # get_reports()
    test_code()
