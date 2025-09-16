FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

COPY . .
ENV MYSQL_USER=root MYSQL_PASSWORD=root MYSQL_HOST=mysql-db MYSQL_PORT=3306 MYSQL_DB=shop
EXPOSE 5000
CMD ["gunicorn","-w","3","-b","0.0.0.0:5000","app:app"]
