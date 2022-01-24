FROM ubuntu:20.04

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install wget software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python3.8 python3-pip -y && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip install --upgrade pip && pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app/

#CMD ["python", "app.py"]
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
