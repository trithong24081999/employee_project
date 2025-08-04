
FROM python:3.10-slim

# Cài các package cơ bản
RUN apt-get update && apt-get install -y netcat-openbsd gcc postgresql-client

# Tạo thư mục chứa source
WORKDIR /app

# Copy toàn bộ code vào container
COPY . .

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000 5678

# Gán biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Chạy lệnh mặc định
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "employee_project.asgi:application"]
# CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "daphne", "-b", "0.0.0.0", "-p", "8000", "employee_project.asgi:application"]
CMD ["watchfiles", "--target-type", "command","--grace-period", "1000",\
     "python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m daphne -b 0.0.0.0 -p 8000 employee_project.asgi:application",\
     "/app"]
