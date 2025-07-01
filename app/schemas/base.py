from typing import Generic, List, Optional, TypeVar
from http import HTTPStatus
from datetime import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class OrderDirection:
    DESC = ("DESC",)
    ASC = "ASC"


class RouterConfig(BaseModel):
    path: str
    roles: list[str] | None = None


class AppBaseResponse(Generic[T]):
    def __init__(
        self,
        data: T = None,
        success: bool = True,
        message: Optional[str] = "",
        status_code: HTTPStatus = HTTPStatus.OK,
        error_code: Optional[int] = None,
    ):
        self.data = data
        self.success = success
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.timestamp = str(datetime.now().timestamp())

    def to_dict(self):
        return {
            "data": self.data,
            "success": self.success,
            "message": self.message,
            "status_code": self.status_code,
            "error_code": self.error_code,
            "timestamp": self.timestamp,
        }

    def to_json(self):
        return JSONResponse(status_code=status.HTTP_200_OK, content=self.to_dict())

    def __repr__(self):
        return (
            f"AppBaseResponse(data={self.data}, success={self.success}, "
            f"message={self.message}, status_code={self.status_code})"
        )


class AppBasePagingRes(Generic[T]):
    def __init__(
        self,
        items: List[T] = [],
        total: int = None,
        is_full: bool = True,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ):
        self.items = items
        self.page = page
        self.page_size = page_size
        self.total = total
        self.is_full = is_full

    def to_dict(self):
        return {
            "items": self.items,
            "page": self.page,
            "page_size": self.page_size,
            "total": self.total,
            "is_full": self.is_full,
        }

    def __repr__(self):
        return (
            f"AppBasePagingRes(items={self.items}, page={self.page}, "
            f"page_size={self.page_size}, total={self.total}, is_full={self.is_full})"
        )

    def to_json(self):
        return JSONResponse(status_code=status.HTTP_200_OK, content=self.to_dict())


class AppBaseResponseError(AppBaseResponse):

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: Optional[int] = None,
    ):
        super().__init__(None, False, message, status_code, error_code)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            "data": self.data,
            "success": self.success,
            "message": self.message,
            "status_code": self.status_code,
            "error_code": self.error_code,
            "timestamp": self.timestamp,
        }

    def to_json(self, status_code: status = status.HTTP_200_OK):
        return JSONResponse(status_code=status_code, content=self.to_dict())
