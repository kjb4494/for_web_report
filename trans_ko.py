from google.cloud import translate
import os
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/sm/Desktop/hsgitlab-6bcd2067e859.json'


def google_trans_ko(text):
    while True:
        try:
            translate_client = translate.Client()
            translation = translate_client.translate(
                text,
                target_language='ko')
            result = translation['translatedText']
            result = result.replace('. ', '.\n')
            result = result.replace('&#39;', '\'')
            result = result.replace('&quot;', '"')
            break
        except:
            time.sleep(1000)
    return result
