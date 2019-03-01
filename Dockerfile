FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt --upgrade

COPY . /

RUN python crocodylia.py

EXPOSE 5042
EXPOSE 10000

CMD ["python", "crocodylia.py", "serve"]
