FROM python:3.10.12-slim-bookworm

ARG REQUIREMENTS_FILE

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN set -x && \
	apt-get update && \
	apt -f install	&& \
	apt-get -qy install netcat-traditional wget && \
	rm -rf /var/lib/apt/lists/* && \
	wget -O /wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && \
	chmod +x /wait-for

COPY ./docker ./docker
COPY ./backend ./

# COPY ./pre-commit.example ./
RUN pip install -r ./${REQUIREMENTS_FILE}

EXPOSE 8000
