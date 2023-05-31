from http import HTTPStatus

from fastapi.exceptions import HTTPException


class AttemptsNumberExceededError(HTTPException):
    def __init__(self):
        self.detail = "There are not enough questions on jservice.io."
        self.status_code = HTTPStatus.BAD_REQUEST


class QuestionAlreadyExistsError(HTTPException):
    def __init__(self):
        self.detail = "Question already exists."
        self.status_code = HTTPStatus.BAD_REQUEST


class CrawlError(HTTPException):
    def __init__(self, exc: Exception):
        self.detail = f"jservice.io fetching data error: {exc}"
        self.status_code = HTTPStatus.BAD_REQUEST
