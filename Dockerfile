FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -y install tesseract-ocr libtesseract-dev poppler-utils gcc musl-dev libpq-dev postgresql

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

#HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

COPY wsgi-entrypoint.sh /

ENTRYPOINT ["sh", "/wsgi-entrypoint.sh"]
