FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN apt-get update -y
RUN apt-get install -y python3-flask
RUN pip3 install -r requirements.txt

RUN flask db migrate -m "Creating database"
RUN flask db upgrade

RUN FLASK_APP=good_energy_tariff_calc flask import_prices location_prices.csv

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app


