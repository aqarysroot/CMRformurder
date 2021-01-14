FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile  ./Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy --system

COPY . code
WORKDIR code

EXPOSE 8000
