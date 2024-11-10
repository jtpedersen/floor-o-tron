FROM acockburn/appdaemon:latest
RUN apk add --no-cache bashio

# Set up the working directory
WORKDIR /conf

# Copy the main AppDaemon configuration
COPY appdaemon.yaml /conf/appdaemon.yaml

# Copy the apps directory and configuration
COPY apps/ /conf/apps/
COPY apps.yaml /conf/apps.yaml

# Ensure permissions are set
RUN chmod -R 755 /conf

ENV HA_TOKEN="${HA_TOKEN}"
ENV HA_URL="${HA_URL}"
