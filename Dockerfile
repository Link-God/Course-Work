FROM python:3.4-alpine3.7

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt
CMD FLASK_APP=Game.py flask run --host="::"
