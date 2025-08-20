from fastapi import FastAPI, HTTPException, Request, Response
from httpx import AsyncClient
from configs.config import PORT
import os
from dotenv import load_dotenv
from schemas.base import AppBaseResponseError
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse

load_dotenv()

# Async client để gửi request đến backend
async_client = AsyncClient()


# Lifespan context replaces startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_client.aclose()


app = FastAPI(
    title="API Gateway",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái của API Gateway"""
    return {"status": "healthy"}


# Custom HTTPException
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(_: Request, exc: HTTPException):
    errors = exc.detail
    status_code = exc.status_code
    error_response = AppBaseResponseError(
        errors,
        status_code,
    )
    return error_response.to_json(status_code)


BASE_ROOT = "/api/v1"


@app.api_route(
    BASE_ROOT + "/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"]
)
async def route_request(service: str, path: str, request: Request):
    """Điều hướng request tới service tương ứng, hỗ trợ streaming và các loại response khác"""

    service_url = os.getenv(service)
    if service_url is None:
        raise HTTPException(status_code=404, detail=f"Service {service} not found")

    full_url = f"{service_url}/{path}"

    try:
        # Lấy method, headers và query parameters từ request gốc
        method = request.method.lower()
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        body = await request.body()

        # Gửi request đến service backend
        async with async_client.stream(
            method=method,
            url=full_url,
            headers=headers,
            params=query_params,
            content=body if body else None,
        ) as response:
            # Kiểm tra Content-Type và Transfer-Encoding của response
            content_type = response.headers.get("content-type", "")
            transfer_encoding = response.headers.get("transfer-encoding", "")

            # Xử lý response dạng stream
            if "chunked" in transfer_encoding or "text/event-stream" in content_type:

                async def stream_content():
                    async for chunk in response.aiter_raw():
                        yield chunk

                return StreamingResponse(
                    stream_content(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=content_type,
                )

            # Xử lý response không phải stream
            else:
                content = await response.aread()
                if "application/json" in content_type:
                    return response.json()
                else:
                    return Response(
                        content=content,
                        media_type=content_type,
                        status_code=response.status_code,
                    )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error forwarding request to {service}: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
