# gateway_service_python
Gateway service python using FastAPI

# version 1.0.0 - 2025-06-19

```
Requirement:
   ✨ Python == 3.12
```

# 2. Cách chạy

## Build backend

Mở terminal chỉ đến đường dẫn chưa file dự án
Sau đó gõ lệnh sau để tạo venv cho dự án

```
Tạo môi trường venv:
    python3 -m venv env

Active virtual venv:
   source env/bin/activate
```

Sau đó chạy file requirement bằng câu lệnh sau

```
pip install -r requirements.txt
```

Tạo file .env có nội dung được ví dụ trong file env-example

Cuối cùng dùng lệnh dưới để chạy start

```
python3 app/main.py

Trên docker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 3. Bảng biến môi trường

Là các thông số đầu vào để chạy

### 3.1 Các biến môi trường để cấu hình app khi chạy

| Tên biến môi trường | Giá trị    | Mô tả                               |
| ------------------- | ---------- | ----------------------------------- |
| PORT                | 8000       | Port mà server sẽ lắng nghe         |


### build bằng docker

```
docker-compose up -d

```

**Automatically create file 'requirements.txt'**

pip freeze > requirements.txt

# Format Code

https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

MacOS: command + shift + p

Windows:

Để định dạng code cho cả source
black .
