# Oauth2, jwt fastapi example

Simple application for showcasing basic usecases of modern token based
authorization technologies (JWT and oauth2).

Uses [Fastapi](https://fastapi.tiangolo.com) as framework and [Motor](https://motor.readthedocs.io/en/stable/) as async mongodb driver
There is also available documentation for the project! 

<br/>

Simply set route to __/docs__ . For example the project you builded
could be hosted on a url: http://localhost:5000

<br/>

Then simply use link:

http://localhost:5000/docs

---

## Installation: 

1) Clone this repository

```bash
git clone https://github.com/michalwilk123/example-auth-fastapi
```

2) Install dependencies (in project directory)

```bash
pip install pipenv
pipenv install
```
---

## Running the application:

### Bearer: Central Statistical Office App

```bash
cd bearer
python run.py
```

### Oauth Host: Communications Department App

```bash
cd data_client
python run.py
```