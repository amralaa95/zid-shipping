FROM python:3.10

EXPOSE 9000

WORKDIR /zid

RUN apt-get update \
    && apt-get install -y wkhtmltopdf xvfb python3-dev libffi-dev libxslt-dev libxml2-dev gcc musl-dev mariadb-client g++ \
    && apt-get install -y ca-certificates

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD ["./run.sh shipment"]
