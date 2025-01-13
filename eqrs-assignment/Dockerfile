FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install flask psycopg2

WORKDIR /app
COPY . /app/
EXPOSE 5000
CMD ["python", "app.py"]
