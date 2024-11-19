FROM acockburn/appdaemon:latest
RUN apk add --no-cache bash

# Set up the working directory
WORKDIR /conf

COPY appdaemon.yaml /conf/appdaemon.yaml

COPY apps/ /conf/apps/
COPY run.py /run.py

RUN chmod -R 755 /conf
RUN mkdir -p /data
ENTRYPOINT []

CMD ["python", "/run.py"]
