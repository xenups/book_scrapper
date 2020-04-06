# BookStore Crawler
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Requirements](https://img.shields.io/badge/Requirements-See%20Here-orange)](https://github.com/xenups/book_scrapper/blob/9c1bb05d90333611e6d60b2081789370258e94b4/requirements.txt)

This project is responsible for the crawling book stores. The coordinator, crawler, and CLI modules work together to do the actual crawling.

This project contains crawling data's from Fidibo, Ketabrah, Taghche and Navar Websites and convert them into a database.
Scrappers are divided into two groups:
- Selenium scrappers 
- API scrappers

It supports Python 3.4+.

## Install
The instructions assume that you have already installed [Docker](https://docs.docker.com/installation/) and [Docker Compose](https://docs.docker.com/compose/install/). 

In order to get started be sure to clone this project onto your Docker Host. Create a directory on your host. Please note that the demo webservices will inherit the name from the directory you create. If you create a folder named test. Then the services will all be named test-web, test-redis, test-lb. Also, when you scale your services it will then tack on a number to the end of the service you scale. 
    
    git clone https://github.com/xenups/book_scrapper.git
    
## How to get up and running
Once you've cloned the project to your host we can now start the Crawler project. 
Easy! Navigate to the directory in which you cloned the project.
Copy and rename .env.example to .env and change the variable as project needs.
Or you can add the parameters manually into .env  file:
To generate an .env file these values are required:

| Variable Name                     | Description                    |
|-----------------------------------|--------------------------------|
| display_visibility                | Visibility screen to show selenium drivers. |
| db_user                  | your database username ,which set in docker-compose.yml|
| db_pass                  | your database password|
| db_host                  | your database host|
| db_port                  | your database port|
| fidibo_worker            | number process assigned to Fidibo crawler|

Before running the package be sure docker-compose.yml properly configured and your location is not in iran, and in the last step Run the following commands from this directory to build and run.   
 
    docker-compose up --build

The  docker-compose command will build the images from Docker file and download perquisite images from Dockerhub and then link them together based on the information inside the docker-compose.yml file. This will create ports, links between containers, and configure applications as required. After the command completes we can now view the status of our stack

    docker-compose ps

If your area is  Iran, just turn on the VPN, before using the package
