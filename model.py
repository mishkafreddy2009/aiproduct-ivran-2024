import pandas as pd
import langchain
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.llms import yandex
from langchain_community.llms.yandex import YandexGPT
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA, llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import YandexGPT

model_uri = ""
api_key = ""

def send_to_gpt(msg, date_start, date_end):
    # Сохранение веркторизованного датасета
    # df = pd.read_json("documents.json", orient='records')
    # loader = DataFrameLoader(df, page_content_column='question')
    # documents = loader.load()
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    # texts = text_splitter.split_documents(documents)
    embeddings = langchain.embeddings.HuggingFaceEmbeddings(
        model_name="distiluse-base-multilingual-cased-v1"
    )
    # sample_vec = embeddings.embed_query("Hello, world!")
    # db = FAISS.from_documents(texts, embeddings)
    # db.as_retriever()
    # db.save_local('faiss')

    db = FAISS.load_local("./faiss", embeddings, allow_dangerous_deserialization=True)  #открываем сохранённую бд

    #Созданиие промпта и шаблона к нему
    prompt_template = """Используй правила для ответа
    Переводи имена собственные на китайский,
    В конце обязательно добавь ссылку на полный документ
    {date} должна быть меньше """+date_start+""" и меньше"""+date_end+"""
    {answer}
    link: {link}
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=['answer', 'link'],
    )

    # Создание цепочки из инициализации модели и промпта
    chain = LLMChain(llm=YandexGPT(temperature=0.03,
                                          model_uri=model_uri,
                                          api_key=api_key,
                                          max_tokens=700),
                     prompt=PROMPT)

    similar_answer = db.similarity_search(msg)
    doc = similar_answer[0].dict()['metadata']

    #Получение результата и извлечение ответа
    result = chain.run(doc)
    # id = data['response'][0]['id']
    return result   #TODO: Вытащить конкретный ответ

send_to_gpt('Какие новые машины выпустили китайские компании?', '2023.01.01', '2023.12.01')