FROM python:3.7-slim

RUN apt-get update && \
    apt-get -y install gcc git

RUN pip install --no-cache-dir flask uwsgi

#Clone newspaper project and checkout specific commit
RUN git clone https://github.com/codelucas/newspaper.git && \
    cd newspaper \
    && pip install -r requirements.txt

COPY . .
ENV NEWSPAPER_PORT 38765
EXPOSE $NEWSPAPER_PORT
CMD ["uwsgi", "--ini", "./src/wsgi.ini"]
