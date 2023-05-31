import asyncio
from pathlib import Path
from typing import IO
from uuid import UUID

from fastapi import Depends, UploadFile

from src.core import exceptions
from src.db.models import Record
from src.repository.record_repository import RecordRepository
from src.repository.user_repository import UserRepository

# Run `lame` mp3 encoder in silent mode (`--quiet`)
# with standard VBR preset (`--preset standard`)
# lame gets it's input from stdin (`-`) and puts output to stdout (`-`)
MP3_ENCODE_COMMAND = "lame --quiet --preset standard - -"


class RecordService:
    def __init__(
        self,
        record_repository: RecordRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.__record_repository = record_repository
        self.__user_repository = user_repository

    async def __convert_wav_to_mp3(self, stdin: IO) -> bytes:
        proc = await asyncio.create_subprocess_shell(
            MP3_ENCODE_COMMAND,
            stdin=stdin,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if stderr:
            raise exceptions.Mp3ConversionError(stderr)

        return stdout

    async def add_record(
        self, user_id: UUID, access_token: UUID, data: UploadFile
    ) -> Record:

        await self.__user_repository.is_user_exists(user_id, access_token)

        record = Record(
            data=await self.__convert_wav_to_mp3(data.file),
            user_id=user_id,
            name=Path(data.filename).with_suffix(".mp3").name,
        )

        await self.__record_repository.create(record)

        return record

    async def get_record(self, record_id: UUID, user_id: UUID) -> Record:
        return await self.__record_repository.get_record(record_id, user_id)
