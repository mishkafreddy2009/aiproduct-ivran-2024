# id ajedvnv574k5fnlub2tc
# key AQVNzf3-U5KFfevli6xvGXRZcoRKiR697DGC5Eqx
# project
import requests
import os
import langchain
import langchain.document_loaders
import langchain_text_splitters

""" fine tuning YandexGpt"""

from langchain.document_loaders import DirectoryLoader


from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Создание шаблона промпта
prompt_template = PromptTemplate(
    "{text} (Источник: {source_url}). Пожалуйста, переведите все имена собственные на английский."
)

# Создание цепочки LLM
chain = LLMChain(prompt_template)

# Создание промпта
prompt = chain.create_prompt(text="Ваш текст", source_url="URL источника")

# Передача промпта в модель
response = model(prompt)




DATA_PATH = "resources/example"
def load_dataset():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    dataset = loader.load()
    return dataset
# class Model():
#     def __int__(self):
#         self
#
#     # user = "shwars"
#     # chunk_size = 1024
#     # chunk_overlap = 50
#     # source_dir = "content"
#     #
#     # loader = langchain.document_loaders.DirectoryLoader(
#     #     source_dir, glob="./resources/example.txt", show_progress=True, recursive=True
#     # )
#     # splitter = langchain_text_splitters.character.RecursiveCharacterTextSplitter(
#     #     chunk_size=chunk_size, chunk_overlap=chunk_overlap
#     # )
#     # # fragments = splitter.create_documents([x.page_content for x in loader.load()])
#     #
#     # embeddings = langchain.embeddings.HuggingFaceEmbeddings(
#     #     model_name="distiluse-base-multilingual-cased-v1"
#     # )
#     # sample_vec = embeddings.embed_query("Hello, world!")
#
#
#
#
#
#
#     prompt = os.environ("./resources/symbols.json")
#
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Api-Key AQVNzf3-U5KFfevli6xvGXRZcoRKiR697DGC5Eqx"
#     }
#     url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
#     response = requests.post(url, headers=headers, json=prompt)
#     result = response.text
#     print(result)