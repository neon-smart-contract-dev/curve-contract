FROM python:3.8

# Set up code directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

# Install linux dependencies
RUN apt-get update \
 && apt-get install -y libssl-dev npm

RUN npm install n -g \
 && npm install -g npm@latest
RUN npm install -g ganache

WORKDIR /usr/src/app

RUN mv .env_docker .env
RUN pip install -r requirements.txt

CMD ["/bin/bash", "./start.sh"]
