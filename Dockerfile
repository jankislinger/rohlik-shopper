FROM ubuntu:20.04

RUN apt update && \
    apt install firefox wget software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt install python3.8 python3-pip -y && \
    ln -s /usr/bin/python3 /usr/bin/python

# GECKODRIVER

ENV GECKO_VERSION="v0.30.0"
ENV GECKO_ROOT="https://github.com/mozilla/geckodriver/releases/download"
ENV GECKO_FILE="geckodriver-${GECKO_VERSION}-linux64.tar.gz"
ENV GECKO_URL="${GECKO_ROOT}/${GECKO_VERSION}/${GECKO_FILE}"

RUN wget ${GECKO_URL} && \
    tar -xvzf geckodriver* && \
    rm ${GECKO_FILE} && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/



RUN pip install --upgrade pip && pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app/

#CMD ["python", "app.py"]
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
