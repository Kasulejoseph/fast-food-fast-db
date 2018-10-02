# fast-food-fast-db
Database to back end the fast food fast api
# Build status
[![Build Status](https://travis-ci.com/Kasulejoseph/fast-food-fast-db.svg?branch=ft-roles-assign-roles-160914769)](https://travis-ci.com/Kasulejoseph/fast-food-fast-db)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0259c2b03a263108f0ac/test_coverage)](https://codeclimate.com/github/Kasulejoseph/fast-food-fast-db/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/Kasulejoseph/fast-food-fast-db/badge.svg)](https://coveralls.io/github/Kasulejoseph/fast-food-fast-db)

## Prerequisites
``` - Python3.6 
   - Flask
   - Flask_restful
   - Virtualenv - A tool to create isolated virtual environment
   - Pytest - python web testing frame work
   ```
   ## Installation
   Clone this repo to your local machine
   ```
      - $ https://github.com/Kasulejoseph/fast-food-fast-db.git
      - $ cd fast-food-fast-db
   ```
   Install virtual environment
   ```
     - On linux
      $ virtualenv env -to create virtual environment
      $ source env/bin/activate -- to activate the virtual environment
     - On windows
       https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/
    - In the virtual environment install the requirement
      $ pip freeze -r requirements.txt
   ```
**Install all the necessary dependencies by**
```
$ Install PostgreSQL
$ sudo -i -u postgres
$ CREATE DATABASE food_db
$ CREATE TABLE users
$ CREATE TABLE menu
$ CREATE TABLE orders
```
   Start the server
   ```
   - $ python run.py
   ```
## Running the tests
To run tests run this command below in your terminal
```
coverage run --source=. -m unittest discover
```
## API End Points
