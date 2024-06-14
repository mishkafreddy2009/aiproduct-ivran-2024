from warcio.recordloader import ArcWarcRecord
from bs4 import BeautifulSoup

def is_valid_record(record: ArcWarcRecord) -> bool:
    return record.rec_type == "response" and record.length > 0

def extract_content(record: ArcWarcRecord) -> bytes | None:
    if not is_valid_record(record):
        return None
    return record.content_stream().read()

def process_content(content: bytes) -> BeautifulSoup:
    return BeautifulSoup(content, "lxml")

def parse_article_text(processed_content: BeautifulSoup):
    text = " ".join(
            p.text.strip()
            for p in processed_content.find_all("p", attrs={"class": None})
            ).replace("\u3000", " ").replace("\xa0", " ")
    return text

def parse_article_title(processed_content: BeautifulSoup) -> str:
    title = processed_content.find("h1")
    if not title:
        return ""
    return title.text.strip()

def extract_date(record: ArcWarcRecord) -> str:
    return record.rec_headers["WARC-Date"][:10]
