FROM python:3.10.12-slim-bookworm

ARG REQUIREMENTS_FILE

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app

RUN set -eux && \
	apt-get update && \
	apt -f install	&& \
	apt-get install -qy netcat-traditional wget make time procps \
    libauthen-ntlm-perl      \
    libcgi-pm-perl           \
    libcrypt-openssl-rsa-perl   \
    libdata-uniqid-perl         \
    libencode-imaputf7-perl      \
    libfile-copy-recursive-perl  \
    libfile-tail-perl         \
    libio-socket-inet6-perl   \
    libio-socket-ssl-perl    \
    libio-tee-perl           \
    libhtml-parser-perl      \
    libjson-webtoken-perl    \
    libmail-imapclient-perl  \
    libparse-recdescent-perl  \
    libproc-processtable-perl  \
    libmodule-scandeps-perl  \
    libreadonly-perl          \
    libregexp-common-perl    \
    libsys-meminfo-perl      \
    libterm-readkey-perl     \
    libtest-mockobject-perl  \
    libtest-pod-perl         \
    libunicode-string-perl   \
    liburi-perl              \
    libwww-perl              \
    libtest-nowarnings-perl  \
    libtest-deep-perl        \
    libtest-warn-perl        \
    cpanminus && \
    rm -rf /var/lib/apt/lists/* && \
	wget -O /wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && \
	chmod +x /wait-for

RUN wget -N https://raw.githubusercontent.com/imapsync/imapsync/master/imapsync
RUN chmod +x imapsync && \
    cp imapsync /usr/bin && \
    /usr/bin/imapsync -version

COPY ./docker ./docker
COPY ./backend ./

# COPY ./pre-commit.example ./
RUN pip install -r ./${REQUIREMENTS_FILE}

EXPOSE 8000
