
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6.5

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first


# create root directory for our project in the container
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /bookcrawler
RUN  apt-get update && apt-get -y install curl && apt-get install -y xvfb xserver-xephyr vnc4server && apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


# Set the working directory to /villastore
WORKDIR /bookcrawler

# Copy the current directory contents into the container at /villastore
ADD . /bookcrawler/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

