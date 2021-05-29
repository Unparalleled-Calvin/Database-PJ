## FDU CARD

### Introduction

The project, powered by **django** with **postgre** database, is a simulator of Fudan campus card for our database course.

author：[Calvin](https://github.com/Unparalleled-Calvin/) 、 [Nimo](https://github.com/Junjie-Ye)

School of computer science and technology, Fudan University

### Dependency packages

Here are some **python dependency packages**. You can use `pip install xxx`  to install them.

- django (for web framework)
- django-apscheduler (for timed task)
- apscheduler 
- psycopg2 (for connection to postgre database)
- pyecharts (for charting)

We use postgre as the background database.

### Usage

- Create a postgre database with sql command in`\files\create.sql`
- Modify the dictionary `DATABASES` in `\mysite\setting.py` to adapt to your database
- Run the command `python manage.py runserver 0.0.0.0:8000` in the root directory to start the server
- Visit `127.0.0.1` with `admin` for `ID` and `000000` for `password` which serve as the default account to start your exploration

### Reference

The front-end design refers to https://www.vhwke.com/auth/login