FROM python:3.10-alpine as builder-api

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add build-base
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.10-alpine
WORKDIR /project
COPY --from=builder-api /install /usr/local
ADD . /project

ENTRYPOINT ["python", "app.py"]