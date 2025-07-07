
FROM python:3.10-slim

# Cài các package cơ bản
RUN apt-get update && apt-get install -y netcat-openbsd gcc postgresql-client

# Tạo thư mục chứa source
WORKDIR /app

# Copy toàn bộ code vào container
COPY . .

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Gán biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Chạy lệnh mặc định
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
