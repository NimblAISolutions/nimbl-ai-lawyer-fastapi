FROM python:3.10.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]