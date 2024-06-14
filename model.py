import requests

def sendToGpt(msg, date_start, date_end):
    prompt = {
        "modelUri": "gpt://b1g2adn1ie6t84o9hc67/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Найди в своём ответе имена собственные, начинающиеся с заглавной буквы и продублируй их в скобках на китайском. Добавь к каждой новости ссылку на источник"
            },
            {
                "role": "user",
                "text": msg
            },
            {
                "role": "assistant",
                "text": "Найди данные за период с "+date_start+" по "+date_end
            },
            {
                "role": "user",
                "text": msg
            }
            ]
        }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN2KFHKB0JGpfcyApwYvGtP8hNRtPjQPosDU0N"
    }

    response = requests.post(url, headers=headers, json=prompt)
    return response.text