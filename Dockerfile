###############
### BUILDER ###
###############

FROM python:3.8-alpine AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt


##############
### RUNNER ###
##############

FROM python:3.8-alpine AS runner

LABEL authors="Pashok11"

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV APP=/app

RUN mkdir $APP
WORKDIR $APP

COPY ./static/ ./static/
COPY ./start_app.py ./
COPY src/ ./src/
COPY ./.env ./
COPY ./.env.api ./

ENTRYPOINT ["python", "start_app.py"]
