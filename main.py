from warcio.archiveiterator import ArchiveIterator

from config import DATASET_PATH
from translator import translate
from parser import (
        extract_content,
        extract_date,
        parse_article_title,
        parse_article_text,
        process_content
        )

import os

def get_warc_files(path: str) -> list[str]:
    files = [path + file for file in os.listdir(path)]
    for file in files:
        if not file.endswith(".warc"):
            files.remove(file)
    return files

def main():
    for warc_file in get_warc_files(DATASET_PATH):
        with open(warc_file, "rb") as stream:
            for record in ArchiveIterator(stream):
<<<<<<< HEAD
                content = extract_content(record)
                article_date = extract_date(record)

                if not content:
                    print("[ERR] record is not valid.")
                    return

                processed_content = process_content(content)

                article_title = parse_article_title(processed_content)
                article_text = parse_article_text(processed_content)

=======
                parser = Parser()
                parser.extract_content(record)
                content = extract_content(record)
                article_date = extract_date(record)
                
                if not content:
                    print("[ERR] record is not valid.")
                    return
                
                processed_content = process_content(content)
                
                article_title = parse_article_title(processed_content)
                article_text = parse_article_text(processed_content)
                
>>>>>>> 8ba2ddea1459fcf736965a92aeafeb0abd14ed2e
                og_data = {
                        "og_title": article_title,
                        "og_text": article_text,
                        "date": article_date,
                        }
<<<<<<< HEAD

=======
                
>>>>>>> 8ba2ddea1459fcf736965a92aeafeb0abd14ed2e
                translated_data = {
                        "translated_title": translate(article_title),
                        "translated_text": translate(article_text),
                        "date": article_date,
                        }

if __name__ == "__main__":
    main()
