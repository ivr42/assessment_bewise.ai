from pydantic import AnyUrl, BaseModel


class RecordCreateResponse(BaseModel):
    audio_file_link: str


class RecordResponse(BaseModel):
    url: AnyUrl
