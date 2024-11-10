# Use an official AppDaemon image as a base
FROM acockburn/appdaemon:latest

# Set up the working directory
WORKDIR /app

# Copy AppDaemon configuration and your app code
COPY apps/ /conf/apps/
COPY appdaemon.yaml /conf/appdaemon.yaml
COPY apps.yaml /conf/apps.yaml

# Run AppDaemon when the container starts
CMD ["appdaemon", "-c", "/conf"]
