FROM python:3.11 

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker