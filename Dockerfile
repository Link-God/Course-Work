FROM python:2.7.14-alpine

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt
CMD FLASK_APP=Game.py flask run --host="::"
