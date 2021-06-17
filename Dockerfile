FROM ubuntu:20.04
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential git
WORKDIR /app
RUN pip3 install wget
RUN pip3 install nltk
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U numpy==1.19
RUN python3 -m spacy download de_core_news_lg

COPY . /src
WORKDIR /src

RUN chmod +x /src/docker-entrypoint.sh




EXPOSE 6006
ENTRYPOINT ["/src/docker-entrypoint.sh"]