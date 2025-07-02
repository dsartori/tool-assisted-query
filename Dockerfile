FROM python:3.10-slim

WORKDIR /app

# Install the tool-assisted-query package
COPY setup.py .
COPY src/ src/
RUN pip install --no-cache-dir .


# Set entrypoint to run the query
ENTRYPOINT ["tool-query"]
