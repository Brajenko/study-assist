from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.runnables.base import Runnable
from langchain_core.vectorstores import VectorStoreRetriever

from .config import (
    GENERATE_IDEAS_PROMPT,
    GENERATE_REQ_MSG,
    QA_TEMPLATE,
    STRUCT_IDEAS_PROMPT,
    SUMMARIZE_CHAIN_TYPE,
    SUMMARIZE_COMBINE_PROMPT,
    SUMMARIZE_MAP_PROMPT,
    THESES_CHAIN_TYPE,
    THESES_COMBINE_PROMPT,
    THESES_ENUMERATE_PROMPT,
    THESES_MAP_PROMPT,
)


def get_summarize_chain(llm: BaseChatModel) -> Runnable:
    return load_summarize_chain(
        llm=llm,
        chain_type=SUMMARIZE_CHAIN_TYPE,
        map_prompt=PromptTemplate.from_template(SUMMARIZE_MAP_PROMPT),
        combine_prompt=PromptTemplate.from_template(SUMMARIZE_COMBINE_PROMPT),
        combine_document_variable_name="text",
        map_reduce_document_variable_name="text",
    )


def get_theses_chain(llm: BaseChatModel) -> Runnable:
    summarize_chain = load_summarize_chain(
        llm,
        chain_type=THESES_CHAIN_TYPE,
        map_prompt=PromptTemplate.from_template(THESES_MAP_PROMPT),
        combine_prompt=PromptTemplate.from_template(THESES_COMBINE_PROMPT),
        combine_document_variable_name="theses_from_parts",
        map_reduce_document_variable_name="text",
    )
    enumerate_prompt = PromptTemplate(
        input_variables=["text"], template=THESES_ENUMERATE_PROMPT
    )
    chain = {"theses": summarize_chain} | enumerate_prompt | llm | StrOutputParser()
    return chain


def get_ideas_chain(llm: BaseChatModel) -> Runnable:
    generate_ideas_prompt = PromptTemplate(
        input_variables=["summary"], template=GENERATE_IDEAS_PROMPT
    )
    generate_ideas_chain = LLMChain(llm=llm, prompt=generate_ideas_prompt)

    struct_ideas_prompt = PromptTemplate(
        input_variables=["ideas"], template=STRUCT_IDEAS_PROMPT
    )
    chain = (
        {"ideas": generate_ideas_chain} | struct_ideas_prompt | llm | StrOutputParser()
    )
    return chain


def get_chat_chain(llm: BaseChatModel, retriever: VectorStoreRetriever) -> Runnable:
    query_transform_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            (
                "user",
                GENERATE_REQ_MSG,
            ),
        ]
    )

    query_transforming_retriever_chain = RunnableBranch(
        (
            lambda x: len(x.get("messages", [])) == 1,  # type: ignore
            (lambda x: x["messages"][-1].content) | retriever,
        ),
        query_transform_prompt | llm | StrOutputParser() | retriever,
    ).with_config(run_name="chat_retriever_chain")

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                QA_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

    chain = RunnablePassthrough.assign(
        context=query_transforming_retriever_chain,
    ).assign(
        answer=document_chain,
    )
    return chain
