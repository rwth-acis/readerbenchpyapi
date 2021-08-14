FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev build-essential git texlive texlive-latex-extra texlive-xetex graphviz graphviz-dev libgraphviz-dev wget
RUN  wget https://github.com/jgm/pandoc/releases/download/2.14.1/pandoc-2.14.1-1-amd64.deb
RUN  dpkg -i pandoc-2.14.1-1-amd64.deb
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U numpy==1.19
RUN pip3 install networkx[default]
RUN pip3 install matplotlib
RUN pip3 install nltk
RUN pip3 install panflute
RUN pip3 install pypandoc
RUN pip3 install pygraphviz
RUN pip3 install PyPDF2
RUN python3 -m spacy download de_core_news_lg
RUN pytest --pyargs networkx
COPY . /src
WORKDIR /src

RUN chmod +x /src/docker-entrypoint.sh




EXPOSE 6006

ENTRYPOINT ["/src/docker-entrypoint.sh"]

#ENTRYPOINT [ "python3" ]
#CMD [ "rb_api_server.py" ]
