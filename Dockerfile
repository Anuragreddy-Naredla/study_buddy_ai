## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app
COPY . .

## Run setup.py
##--no-cache-dir all the previous cache dir will be removed
RUN pip install --no-cache-dir -e .

# Used PORTS
EXPOSE 8501

# Run the app 
#--server.address=0.0.0.0=> our application can be accessed by any IP address
#--server.headless=true=> This is the dependency to open the streamlit app
CMD ["streamlit", "run", "application.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]