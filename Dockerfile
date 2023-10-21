FROM python:3.10

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# RUN chmod a+x docker/*.sh

RUN alembic upgrade head

# WORKDIR src

CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker