from fastapi import FastAPI, HTTPException, Request, Response
from httpx import AsyncClient

from app.configs.config import PORT

app = FastAPI(title="API Gateway")

# Cấu hình các service backend
SERVICE_REGISTRY = {
    "payment": "http://localhost:8000",
    "account": "http://account-service:8002",
    "product": "http://product-service:8003",
    "blogs": "http://blogs-service:8004",
}


# Async client để gửi request đến backend
async_client = AsyncClient()


@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái của API Gateway"""
    return {"status": "healthy"}


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(service: str, path: str, request: Request):
    """Điều hướng request tới service tương ứng, bao gồm header và query parameters"""
    if service not in SERVICE_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Service {service} not found")

    service_url = SERVICE_REGISTRY[service]
    full_url = f"{service_url}/{path}"

    try:
        # Lấy method, headers và query parameters từ request gốc
        method = request.method.lower()
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        body = await request.body()

        # Gửi request đến service backend
        if method == "get":
            response = await async_client.get(
                full_url, headers=headers, params=query_params
            )
        elif method == "post":
            response = await async_client.post(
                full_url,
                content=body if body else {},
                headers=headers,
                params=query_params,
            )
        elif method == "put":
            response = await async_client.put(
                full_url,
                content=body if body else {},
                headers=headers,
                params=query_params,
            )
        elif method == "delete":
            response = await async_client.delete(
                full_url, headers=headers, params=query_params
            )
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")

        # Kiểm tra Content-Type của response
        content_type = response.headers.get("content-type", "")

        # Xử lý response dựa trên Content-Type
        if "application/json" in content_type:
            return response.json()
        else:
            # Trả về nội dung nguyên bản (text, binary, v.v.)
            return Response(
                content=response.content,
                media_type=content_type,
                status_code=response.status_code,
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error forwarding request to {service}: {str(e)}"
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Đóng async client khi shutdown"""
    await async_client.aclose()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
