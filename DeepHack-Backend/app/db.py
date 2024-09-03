import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

from .config import (
    CHAT_DOCS_CHUNK_OVERLAP,
    CHAT_DOCS_CHUNK_SIZE,
    RETRIEVER_SEARCH_KWARGS,
    RETRIEVER_SEARCH_TYPE,
    SUMMARIZE_DOCS_CHUNK_OVERLAP,
    SUMMARIZE_DOCS_CHUNK_SIZE,
)


def create_db(uuid: str, embeddings: Embeddings) -> FAISS:
    pdf_path = f"files/{uuid}.pdf"
    pdf_loader = PyPDFLoader(pdf_path)
    document = pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHAT_DOCS_CHUNK_SIZE,
        chunk_overlap=CHAT_DOCS_CHUNK_OVERLAP,
    )
    documents = text_splitter.split_documents(document)
    db = FAISS.from_documents(documents, embeddings)
    db_path = f"indexes/chat/{uuid}"
    db.save_local(db_path)
    return db


def get_db(uuid: str, embeddings: Embeddings) -> FAISS:
    db_path = f"/indexes/chat/{uuid}"
    if os.path.isdir(db_path):
        return FAISS.load_local(
            db_path, embeddings, allow_dangerous_deserialization=True
        )
    return create_db(uuid, embeddings)


def get_retriever(uuid: str, embeddings: Embeddings) -> VectorStoreRetriever:
    db = get_db(uuid, embeddings)
    retriever = db.as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs=RETRIEVER_SEARCH_KWARGS,
    )
    return retriever


def get_documents(uuid: str) -> list[Document]:
    pdf_path = f"files/{uuid}.pdf"
    pdf_loader = PyPDFLoader(pdf_path)
    document = pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=SUMMARIZE_DOCS_CHUNK_SIZE,
        chunk_overlap=SUMMARIZE_DOCS_CHUNK_OVERLAP,
    )
    return text_splitter.split_documents(document)
