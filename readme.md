# BookStore Crawler
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Requirements](https://img.shields.io/badge/Requirements-See%20Here-orange)](https://github.com/xenups/book_scrapper/blob/9c1bb05d90333611e6d60b2081789370258e94b4/requirements.txt)

This project is responsible for the crawling book stores. The coordinator, crawler, and CLI modules work together to do the actual crawling.

This project contains crawling data's from Fidibo, Ketabrah, Taghche and Navar Websites and convert them into a database.
Scrappers are divided into two groups:
1- Selenium scrapping 
2- API scrapping

It supports Python 3.4+.
##
## Preparations:
```bash
apt-get install xvfb xserver-xephyr vnc4server
```
```bash
pip install requirements.txt
```