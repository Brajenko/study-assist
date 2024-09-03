import re
from typing import Any, AsyncGenerator, Callable, Union

from langchain.callbacks import FinalStreamingStdOutCallbackHandler
from langchain.chat_models.gigachat import GigaChat
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage

from .chains import (
    get_chat_chain,
    get_ideas_chain,
    get_summarize_chain,
    get_theses_chain,
)
from .config import CREDINTIALS, MODEL, SCOPE
from .db import get_retriever, get_documents
from .schemas import Message

llm = GigaChat(
    credentials=CREDINTIALS,
    verify_ssl_certs=False,
    scope=SCOPE,
    model=MODEL,
    profanity_check=False,
    streaming=True,
    callbacks=[FinalStreamingStdOutCallbackHandler()],
    timeout=900,
)

embeddings = GigaChatEmbeddings(
    credentials=CREDINTIALS, verify_ssl_certs=False, scope=SCOPE
)


def _message_to_langchain(
    msg: Message,
) -> Union[AIMessage, HumanMessage, SystemMessage, None]:
    match msg.sender:
        case "assistant":
            return AIMessage(content=msg.text)
        case "user":
            return HumanMessage(content=msg.text)
    raise ValueError('msg.sender not in ["assistant", "user"]')


def _parse_numbered_list(s: str) -> list[str]:
    return [match.group(1) for match in re.finditer(r"[1-9]\. (.+)", s)]


def get_chat_response(uuid: str, history: list[Message]) -> str:
    messages = [_message_to_langchain(msg) for msg in history]
    retriever = get_retriever(uuid, embeddings)
    chain = get_chat_chain(llm, retriever)
    response = chain.invoke({"messages": messages})
    return response["answer"]


async def get_chat_stream(
    uuid: str, history: list[Message]
) -> Callable[[], AsyncGenerator[str, Any]]:
    messages = [_message_to_langchain(msg) for msg in history]
    retriever = get_retriever(uuid, embeddings)
    chain = get_chat_chain(llm, retriever)

    async def stream():
        async for text in chain.astream({"messages": messages}):
            t = text.get("answer", None)
            if t is not None:
                yield t

    return stream


def get_summarize_response(uuid: str) -> str:
    documents = get_documents(uuid)
    chain = get_summarize_chain(llm)
    return chain.invoke({"input_documents": documents})["output_text"]


def get_theses_response(uuid: str) -> list[str]:
    documents = get_documents(uuid)
    chain = get_theses_chain(llm)
    resp = chain.invoke({"input_documents": documents})
    return _parse_numbered_list(resp)


def get_ideas_reponse(summary: str) -> list[str]:
    chain = get_ideas_chain(llm)
    resp = chain.invoke({"summary": summary})
    return _parse_numbered_list(resp)


if __name__ == "__main__":
    pass
    # import asyncio

#     async def summ():
#         uuid = 'BBxzFQSF'
#         docs = get_documents(uuid)
#         chain = get_summarize_chain(llm)
#         async for text in chain.astream({'input_documents': docs}):
#             print(text)

#     async def theses():
#         uuid = 'BBxzFQSF'
#         docs = get_documents(uuid)
#         chain = get_theses_chain(llm)

#         async for text in chain.astream({'input_documents': docs}):
#             print(text)

# async def chat():
#     uuid = 'BBxzFQSF'
#     retriever = get_retriever(uuid, embeddings)
#     chain = get_chat_chain(llm, retriever)
#     async for text in chain.astream(
#         {'input': 'что такое комбайн', 'chat_history': []}
#     ):
#         print(text)

# def inf_chat():
#     uuid = 'EYAiAWUF'
#     retriever = get_retriever(uuid, embeddings)

#     query_transform_prompt = ChatPromptTemplate.from_messages(
#         [
#             MessagesPlaceholder(variable_name="messages"),
#             (
#                 "user",
#                 "Учитывая приведенный выше разговор, сгенерируй поисковый запрос для поиска информации, относящейся к разговору. Ответь только поисковым запросом.",
#             ),
#         ]
#     )


#     from langchain_core.output_parsers import StrOutputParser
#     from langchain_core.runnables import RunnableBranch
#     from langchain_core.runnables import RunnablePassthrough

#     query_transforming_retriever_chain = RunnableBranch(
#         (
#             lambda x: len(x.get("messages", [])) == 1,
#             (lambda x: x["messages"][-1].content) | retriever,
#         ),
#         query_transform_prompt | llm | StrOutputParser() | retriever,
#     ).with_config(run_name="chat_retriever_chain")

#     question_answering_prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 SYSTEM_TEMPLATE,
#             ),
#             MessagesPlaceholder(variable_name="messages"),
#         ]
#     )

#     document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

#     chain = RunnablePassthrough.assign(
#         context=query_transforming_retriever_chain,
#     ).assign(
#         answer=document_chain,
#     )


# history = []
# uuid = 'BBxzFQSF'
# while query := input('User: '):
#     history.append(Message(sender='user', text=query))
#     resp = get_chat_response(uuid, history)
#     history.append(Message(sender='assistant', text=resp))
#     print('ai:', resp)

#     async def ideas():
#         uuid = 'BBxzFQSF'
#         chain = get_ideas_chain(llm)
#         async for text in chain.astream(
#             {
#                 'summary': 'В данном отрывке описывается система работы по формированию профессиональной и личностной идентичности студентов-психологов, которая показала свою эффективность. Рекомендуется внедрить ее в практику обучения для повышения личностных и профессиональных качеств студентов-психологов. Также обсуждается необходимость создания психологической службы в вузе для помощи студентам в адаптации, преодолении проблем и формировании комфортных межличностных отношений.\n\nСтудент-психолог сталкивается с отсутствием готовой технологии взаимодействия и необходимостью построения ее на основе опыта и интуиции. Профессиональное общение возможно только в ограниченной сфере жизнедеятельности. Подготовка психологов характеризуется влиянием коммуникации "психолог-клиент", которая способствует формированию личности как социального качества.\n\nВ отрывке рассматривается профессиональное становление студентов-психологов, которое характеризуется противоречивостью и сложностью. Причины этого коренятся как во внешней среде, так и во внутреннем плане личности. Студенты-психологи на первых курсах имеют размытый образ профессионала и ориентированы на внешнюю оценку деятельности. В дальнейшем происходит переосмысление профессиональных намерений и ориентация на взаимодействие с другими людьми посредством психологических знаний, умений и навыков.\n\nОтрывок описывает процесс профессионального становления студентов-психологов, отмечая, что они начинают с принятия себя и оказания помощи клиентам, затем переходят к осознанию своей роли в обучении и построении будущего в профессии. Однако, отмечается неудовлетворенность собой среди студентов 5-го курса и различия в мотивационных, интеллектуальных и личностных характеристиках по сравнению с профессионально успешными психологами.'
#             }
#         ):
#             print(text, end='')

# asyncio.run(inf_chat())
# inf_chat()
# history = []
# while query := input('User: '):
#     history.append(Message(sender='user', text=query))
#     print('AI:', get_chat_response('BBxzFQSF', history))
