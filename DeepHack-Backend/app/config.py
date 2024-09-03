import os

from dotenv import load_dotenv

load_dotenv()

# GIGACHAIN CREDINTIALS, SETTINGS AND PROMPTS
CREDINTIALS = os.environ.get("GIGACHAT")
SCOPE = os.environ.get("SCOPE", "GIGACHAT_API_PERS")
MODEL = os.environ.get("MODEL", "GigaChat-Pro")

# GENERATE_REQ_MSG = 'Учитывая приведенный выше разговор, сгенерируй запрос для поиска информации в векторной базе данных, относящейся к разговору, . Ответь только поисковым запросом.'
GENERATE_REQ_MSG = "Учитывая приведенный выше разговор, сформулируй запрос для поиска по векторной базе данных. Запрос должен искать информацию, относящуюся к последним сообщениям в разговоре. Ответь только поисковым запросом."

QA_TEMPLATE = """Ты - генеративная языковая модель.
Ты умеешь ТОЛЬКО анализировать научные работы и отвечать на вопросы по ним.
Тебя создала команда awareteam на хакатоне Deephack.Agents.
Ниже - текст научной работы. Отвечай на вопросы пользователя используя этот текст. Если текст не содержит информации для ответа на вопрос, скажи что не знаешь ответа.

{context}
"""

SUMMARIZE_MAP_PROMPT = """input_variables: [text]
template: 'Это отрывок из научной статьи. Напиши краткое содержимое этого отрывка объемом в 2-3 предложения, оставив только самое важное.


"{text}"


Теперь напиши краткое содержимое отрывка объемом в 2-3 предложения:'
template_format: f-string
_type: prompt"""

SUMMARIZE_COMBINE_PROMPT = """input_variables: [text]
template: 'Суммаризируй части научной статьи в один текст на 10-15 предложений.


"{text}"


Теперь суммаризируй части научной статьи в один текст на 10-15 предложений.
Краткое содержимое:'
template_format: f-string
_type: prompt"""


THESES_MAP_PROMPT = """input_variables: [text]
template: 'Перед тобой отрывок из научной статьи. Выдели из него 3 основые идеи.


"{text}"


Теперь выдели из отрывка три основные идеи:'
template_format: f-string
_type: prompt"""

THESES_COMBINE_PROMPT = """input_variables: [theses_from_parts]
template: 'Ниже приведен набор фактов и мыслей. Выдели из них 5 самых важных.


"{theses_from_parts}"


Основные 5 фактов из текста:'
template_format: f-string
_type: prompt"""

THESES_ENUMERATE_PROMPT = """Ниже приведен набор фактов и мыслей. Пронумеруй их и запиши каждый факт с новой строки.

{theses}

Пронумерованные факты:"""

GENERATE_IDEAS_PROMPT = """Это краткое содержимое научного исследования. Придумай 3-4 идеи, как можно развить это исследование

{summary}

Теперь напиши 3-4 идеи, как можно развить это исследование"""

STRUCT_IDEAS_PROMPT = """Ниже приведен набор идей. Пронумеруй их и запиши каждую идею с новой строки.

{ideas}

Пронумерованные идеи:"""


RETRIEVER_SEARCH_TYPE = "mmr"
RETRIEVER_SEARCH_KWARGS = {"k": 7, "fetch_k": 20}

CHAT_DOCS_CHUNK_SIZE = 1500
CHAT_DOCS_CHUNK_OVERLAP = 300

SUMMARIZE_DOCS_CHUNK_SIZE = 5000
SUMMARIZE_DOCS_CHUNK_OVERLAP = 500

SUMMARIZE_CHAIN_TYPE = "map_reduce"
THESES_CHAIN_TYPE = "map_reduce"
