# fast-food-fast-db
Database to hold data the api

The app is hosted here on [heroku](https://fast-food-fast-db.herokuapp.com/api/v1/menu/)
# Build status
[![Build Status](https://travis-ci.com/Kasulejoseph/fast-food-fast-db.svg?branch=develop)](https://travis-ci.com/Kasulejoseph/fast-food-fast-db)
[![Maintainability](https://api.codeclimate.com/v1/badges/0259c2b03a263108f0ac/maintainability)](https://codeclimate.com/github/Kasulejoseph/fast-food-fast-db/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Kasulejoseph/fast-food-fast-db/badge.svg?=develop)](https://coveralls.io/github/Kasulejoseph/fast-food-fast-db)
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

|           End Point                      |     Resource Accessed    |   Access   | Requirements|
|   -------------------------------------- |-----------------------|------------|-------------|
|     api/v1/auth/signup      POST             | Register a user   |   PUBLIC   | username, email, password
|     api/v1/auth/login   POST       | Login a user   |   PUBLIC | username, password, role |
|     api/v1/users/orders     POST   | Place an order for food.  |   PUBLIC |user_id, menu_id
|     api/v1/users/orders    GET      | Get the order history for a particular user.    |    PUBLIC  |user_id
|     api/v1/orders       GET | Get all orders    |   ADMIN  |user_id, menu_id, order_id
|    api/v1/orders/order_id GET   | Fetch a specific order  |   ADMIN |order_id
|    api/v1/orders/order_id  PUT  | Update the status of an order   |   ADMIN   | order_id
|     api/v1/menu GET  | Get available menu    |   PUBLIC   | menu_id
|     api/v1/menu POST | Add a meal option to the menu.    |   ADMIN   | menu_id

![swagger](https://user-images.githubusercontent.com/32167860/46521345-49bd9b80-c84d-11e8-9049-7c37d04d5cd5.png)
