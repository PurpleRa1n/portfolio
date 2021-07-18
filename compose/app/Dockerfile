FROM python:3.8.3-alpine

LABEL maintainer='Artem F'

ENV APP_USER=portfolio
ENV APP_DIR=portfolio
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIPENV_VENV_IN_PROJECT=1

RUN mkdir -p ${APP_DIR} \
    && apk update -qq\
    && apk add build-base gcc libffi-dev libressl-dev openssl-dev postgresql-dev bash -qq\
    && addgroup --gid 1984 $APP_USER \
    && adduser --uid 1984 --ingroup $APP_USER --disabled-password --gecos "" $APP_USER

WORKDIR ${APP_DIR}
USER ${APP_USER}

COPY requirements/ .
RUN pip3 install -r dev.txt

COPY ./compose/app/entrypoint.sh /usr/local/bin/

COPY . $APP_DIR
ENTRYPOINT ["entrypoint.sh"]
CMD ["runserver"]
