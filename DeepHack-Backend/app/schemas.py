from typing import Annotated

from pydantic import BaseModel, HttpUrl
from pydantic.types import StringConstraints

FILE_UUID_FIELD = Annotated[str, StringConstraints(min_length=8, max_length=8)]
PDF_FILE_URL = HttpUrl


class UploadFileResponse(BaseModel):
    file_uuid: FILE_UUID_FIELD

    model_config = {
        'json_schema_extra': {'examples': [{'file_uuid': 'xFhBohW6'}]}
    }


class Message(BaseModel):
    sender: Annotated[
        str, StringConstraints(pattern=r'^assistant|user$')
    ]
    text: str
