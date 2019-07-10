FROM python:3.7-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install gcc python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++ git

RUN pip install --no-cache-dir flask uwsgi

#Clone newspaper project and checkout specific commit
RUN git clone https://github.com/codelucas/newspaper.git && \
    cd newspaper \
    && pip install -r requirements.txt

COPY . .
ENV NEWSPAPER_PORT 38765
EXPOSE $NEWSPAPER_PORT
CMD ["uwsgi", "--ini", "./src/wsgi.ini"]
