import re


def strip_html_tag(contents):
    return re.sub('<.+?>', '', contents, 0).strip()


def remove_globals_attribute(contents):
    contents = contents.replace('globals; ', '')
    contents = contents.replace('globals', '')
    return typo_process(contents)


def typo_process(contents):
    edited_typo = contents.replace('crossorigin nonce', 'crossorigin; nonce')
    return edited_typo
