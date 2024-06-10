import requests
import os
from warcio.archiveiterator import ArchiveIterator
from warcio.recordloader import ArcWarcRecord
from bs4 import BeautifulSoup

WARCS_PATH = "./dataset/ja/"
YA_TRANSLATE_TOKEN = os.environ["YA_TRANSLATE_TOKEN"]

def call_api(url: str, data: dict) -> dict:
    headers = { "Authorization" : f"Api-Key {YA_TRANSLATE_TOKEN}" }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def extract_content(record: ArcWarcRecord) -> str | None:
    if record.rec_type != "response" or record.length <= 0:
        return None
    content = record.content_stream().read()
    return content.decode("utf-8", errors="ignore")

def parse_content(content: str) -> dict:
    soup = BeautifulSoup(content, "lxml")
    rows = [p.text.strip().replace("\n", " ") for p in soup.find_all("p", attrs={"class": None})]
    text = " ".join(row for row in rows if row)
    data = {}
    if soup.title and soup.title.string:
        title = soup.title.string[9::]
        data |= { "og_title": title, "og_text": text }
    else:
        data |= { "og_text": text }
    date = soup.find("p", attrs={"class":"date"}).text
    date = "".join(c for c in date if c.isdigit())[:8]
    date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    data |= { "date": date }
    return data

def translate_text(data: dict) -> dict | None:
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    og_texts = list(data.values())[:-1]
    translation_info = call_api(url, {
        "targetLanguageCode": "ru",
        "texts": og_texts
    })
    translations = translation_info["translations"]
    if not translations:
        return None
    translated_data = {}
    if len(og_texts) == 1:
        translated_text = translations[0]["text"]
        translated_data |= { "translated_text": translated_text }
    else:
        translated_title = translations[0]["text"]
        translated_text = translations[1]["text"]
        translated_data |= {
                "translated_title": translated_title,
                "translated_text": translated_text
                }
    translated_data |= { "og_lang": translations[0]["detectedLanguageCode"] }
    translated_data |= { "date": data["date"] }
    return translated_data

def main():
    with open(WARCS_PATH + "ascii.jp-2016-12.warc", "rb") as stream:
        for record in ArchiveIterator(stream):
            content = extract_content(record)
            if content:
                data = parse_content(content)
                print(translate_text(data))
                break

if __name__ == "__main__":
    main()
