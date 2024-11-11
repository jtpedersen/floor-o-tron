FROM acockburn/appdaemon:latest
RUN apk add --no-cache bash

# Set up the working directory
WORKDIR /conf

COPY appdaemon.yaml /conf/appdaemon.yaml

# Copy the apps directory and configuration
COPY apps/ /conf/apps/

# Ensure permissions are set
RUN chmod -R 755 /conf

ENV HA_TOKEN="${HA_TOKEN}"
ENV HA_URL="${HA_URL}"

ENTRYPOINT []

CMD ["bash", "/apps/run.sh"]
