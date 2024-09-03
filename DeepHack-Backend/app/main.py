import os
import json
import random
import string
from typing import Annotated

import requests
import uvicorn
from fastapi import APIRouter, Body, FastAPI, File, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import ai_controller
from .schemas import FILE_UUID_FIELD, Message, PDF_FILE_URL

if not os.path.isdir("files"):
    os.makedirs("files")

if not os.path.isdir("indexes/chat"):
    os.makedirs("indexes/chat")

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/files/raw", StaticFiles(directory="files"))
router = APIRouter(prefix="/api/v1")


def generate_uuid() -> str:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choices(alphabet, k=8))


def validate_uuid(uuid: str) -> bool:
    pdf_path = f"files/{uuid}.pdf"
    return os.path.isfile(pdf_path)


def get_chat_history(chat_history: str):
    messages = json.loads(chat_history)
    return [Message(**msg) for msg in messages]


def uuid_or_err(uuid: str):
    if not validate_uuid(uuid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File with this UUID not found.",
        )


@router.post("/files/")
async def upload_file(file: Annotated[bytes, File()]) -> FILE_UUID_FIELD:
    uuid = generate_uuid()
    filepath = f"files/{uuid}.pdf"
    with open(filepath, "ba") as pdf_file:
        pdf_file.write(file)
    return uuid


@router.post("/files/via_url")
async def upload_file_url(url: Annotated[PDF_FILE_URL, Body()]) -> FILE_UUID_FIELD:
    uuid = generate_uuid()
    filepath = f"files/{uuid}.pdf"
    r = requests.get(str(url))
    with open(filepath, "wb") as outfile:
        outfile.write(r.content)
    return uuid


@router.get("/files/{file_uuid}/summary")
async def get_summary(file_uuid: FILE_UUID_FIELD) -> str:
    uuid_or_err(file_uuid)
    return ai_controller.get_summarize_response(file_uuid)


@router.get("/files/{file_uuid}/theses")
async def get_theses(file_uuid: FILE_UUID_FIELD) -> list[str]:
    uuid_or_err(file_uuid)
    return ai_controller.get_theses_response(file_uuid)


@router.post("/files/{file_uuid}/chat")
async def get_chat(
    file_uuid: FILE_UUID_FIELD,
    chat_history: list[Message],
) -> str:
    uuid_or_err(file_uuid)
    return ai_controller.get_chat_response(file_uuid, chat_history)


@router.get("/files/{file_uuid}/chat/stream")
async def get_chat_stream(
    file_uuid: FILE_UUID_FIELD,
    chat_history: Annotated[list[Message], Depends(get_chat_history)],
) -> StreamingResponse:
    uuid_or_err(file_uuid)
    streamer = await ai_controller.get_chat_stream(file_uuid, chat_history)
    return StreamingResponse(streamer(), media_type="text/event-stream")


@router.post("/ideas")
async def get_ideas(summary: Annotated[str, Body()]) -> list[str]:
    return ai_controller.get_ideas_reponse(summary)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=5000,
        log_level="info",
        reload=True,
    )
