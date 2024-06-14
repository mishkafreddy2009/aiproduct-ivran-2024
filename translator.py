from utils import call_api

def translate(text: str):
    # rewrite for texts list to prevent multiply api requests
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    response = call_api(url=url, data={
        "targetLanguageCode": "ru",
        "texts": text
        })
    return response["translations"][0]["text"]
