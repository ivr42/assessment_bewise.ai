from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from fastapi.responses import Response
from fastapi_restful.cbv import cbv

from src.api.response_models.record_response import RecordResponse
from src.core.tools import generate_error_responses
from src.services.record_service import RecordService

router = APIRouter(prefix="/record", tags=["Record"])


@cbv(router)
class RecordCBV:
    __record_service: RecordService = Depends()

    @router.post(
        "/",
        name="add_record",
        response_model=RecordResponse,
        status_code=HTTPStatus.CREATED,
        summary="Add audio record",
        response_description=HTTPStatus.CREATED.phrase,
        responses=generate_error_responses(
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND
        ),
    )
    async def add_record(
        self,
        request: Request,
        user_id: UUID = Form(),
        access_token: UUID = Form(),
        audio: UploadFile = File(),
    ) -> Any:

        new_record = await self.__record_service.add_record(
            user_id, access_token, audio
        )

        query_params = {"id": new_record.id, "user": new_record.user_id}

        return {
            "url": request.url_for("get_record")
            .include_query_params(**query_params)
            ._url
        }

    @router.get(
        "/",
        name="get_record",
        status_code=HTTPStatus.OK,
        summary="Get audio record",
        response_description=HTTPStatus.OK.phrase,
        responses=generate_error_responses(HTTPStatus.NOT_FOUND),
    )
    async def get_record(
        self,
        record_id: UUID = Query(..., alias="id"),
        user_id: UUID = Query(..., alias="user"),
    ) -> Any:
        record = await self.__record_service.get_record(record_id, user_id)

        return Response(
            record.data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment;filename={record.name}",
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
