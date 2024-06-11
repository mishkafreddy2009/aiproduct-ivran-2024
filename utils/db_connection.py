import clickhouse_connect
from datetime import datetime
import os
import requests
from warcio.archiveiterator import ArchiveIterator
from warcio.recordloader import ArcWarcRecord
from bs4 import BeautifulSoup
from os import walk, remove
import shutil
import gzip
from uuid import uuid4

""" Подключение к бд """

class Db_Connection():
    global client  # pylint:  disable=global-statement
    client = clickhouse_connect.get_client(
        host=os.environ['client_host'],
        user='default',
        password=os.environ['client_password'],
        secure=True
    )
    # пример query на макете raw_data таблицы
    # client.query('CREATE TABLE original_data ("data_id" UUID PRIMARY KEY, "marked_data" String) ENGINE MergeTree')

    # пример добавления данных в таблицу raw_data на clickhouse
    # column_names = ['data_id', 'marked_data', 'date', 'language', 'link']

    # rows при подаче в clickhouse (client.insert) должен иметь тип list(list())
    # rows = [[uuid.uuid4(), 'こんにちは、親愛なる友人たち', datetime.strptime('2014-12-04', '%Y-%m-%d').date(), 'ja', 'testfile.warc.gz']]

    # пример client.insert(<table_name>, data=list(list()), column_names=list(str))
    # client.insert('raw_data', rows, column_names=column_names)
    # client.query('DROP TABLE test_table')

    WARCS_PATH = "./archive/"


    def decompress_gz(gz_file_path, warc_out_path):
        # Decompress the .gz file
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(warc_out_path, 'wb+') as f_out:
                shutil.copyfileobj(f_in, f_out)


    def get_file_names(files_path):
        return next(walk(files_path), (None, None, []))[2]  # [] if no file


    def call_api(url: str, data: dict) -> dict:
        headers = {"Authorization": f"Api-Key AQVNxDjsG_WBJvlAVaBFe8Fv2agI-O4GhF39G9GA"}
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
            data |= {"og_title": title, "og_text": text}
        else:
            data |= {"og_text": text}
        # date = soup.find("p", attrs={"class":"date"}).text
        # date = "".join(c for c in date if c.isdigit())[:8]
        # date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        # data |= { "date": date }
        return data


    def insert_clickhouse_row(text):
        column_names = ['data_id', 'marked_data']
        rows = [[uuid4(), text]]
        client.insert('original_data', rows, column_names=column_names)


    def translate_text(self, data: dict) -> dict | None:
        url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
        og_texts = list(data.values())[:-1]
        translation_info = self.call_api(url, {
            "targetLanguageCode": "ru",
            "texts": og_texts
        })
        translations = translation_info["translations"]
        if not translations:
            return None
        translated_data = {}
        if len(og_texts) == 1:
            translated_text = translations[0]["text"]
            translated_data |= {"translated_text": translated_text}
        else:
            translated_title = translations[0]["text"]
            translated_text = translations[1]["text"]
            translated_data |= {
                "translated_title": translated_title,
                "translated_text": translated_text
            }
        translated_data |= {"og_lang": translations[0]["detectedLanguageCode"]}
        translated_data |= {"date": data["date"]}
        return translated_data


    def main(self):
        files_path = "dataset/train/zh_unpacked"
        for file_name in self.get_file_names(files_path):
            full_path = files_path + "/" + file_name
            with open(full_path, "rb") as stream:
                print(file_name)
                for record in ArchiveIterator(stream):
                    content = self.extract_content(record)
                    if content:
                        data = self.parse_content(content)
                        extracted_text = data['og_title'] + '\n' + data['og_text']
                        self.insert_clickhouse_row(extracted_text)


    # def main():
    #     gzs_path = "dataset/train/zh"
    #     warc_path = "dataset/train/zh_unpacked/"
    #     # print(os.listdir(gzs_path))
    #     print(get_file_names(gzs_path))
    #     for file_name in get_file_names(gzs_path):
    #         gzs_path_full = gzs_path + '/' + file_name
    #         warc_path_full = warc_path + file_name[:-3]
    #         decompress_gz(gzs_path_full, warc_path_full)
    #         remove(gzs_path_full)
    #         print(f"The file {gzs_path_full} has been deleted.")

    if __name__ == "__main__":
        main()