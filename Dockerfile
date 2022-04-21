FROM python:3.9-buster

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update

COPY . .

WORKDIR /app/source/ta_lib
RUN tar -xvzf ta-lib-0.4.0-src.tar.gz
WORKDIR /app/source/ta_lib/ta-lib
RUN ./configure --prefix=/usr
RUN make
RUN make install
WORKDIR /app

RUN rm -r source

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

RUN python manage.py collectstatic --no-input --clear

CMD uwsgi uwsgi.ini
