FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

RUN groupadd -r web && useradd -d /opt/app -r -g web web \
    && chown web:web -R /opt/app

USER web

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
