import psycopg2
from flask import current_app as app
import os


class Database(object):
    """class for app database"""

    def __init__(self):
        """initialize db connection """
        try:
            if os.getenv("APP_SETTINGS") == "testing":
                self.connection = psycopg2.connect(
                    str(os.getenv("DATABASE_URL2"))
                )
            elif os.getenv("APP_SETTINGS") == "development":
                self.connection = psycopg2.connect(
                    str(os.getenv("DATABASE_URL1"))
                )
            else:

                self.connection = psycopg2.connect(
                    str(os.getenv("DATABASE_URL"))
                )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)

    def create_tables(self):
        """ create tables """
        create_table = """CREATE TABLE IF NOT EXISTS users
        (user_id SERIAL PRIMARY KEY, username VARCHAR(30),
        email VARCHAR(100), location VARCHAR(100), password VARCHAR(150),
        role VARCHAR(100) DEFAULT 'user')"""
        self.cursor.execute(create_table)

        create_table = """ CREATE TABLE IF NOT EXISTS menu(
        menu_id SERIAL PRIMARY KEY,
        meal VARCHAR(40), description VARCHAR(200),
        price INT NOT NULL)"""
        self.cursor.execute(create_table)

        create_table = """ CREATE TABLE IF NOT EXISTS orders(
        order_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
        menu_id INTEGER NOT NULL, meal VARCHAR(40), description
        VARCHAR(200), price INT, status VARCHAR(30), FOREIGN KEY(user_id)
        REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(menu_id) REFERENCES menu(menu_id) ON UPDATE CASCADE ON
        DELETE CASCADE)"""
        self.cursor.execute(create_table)     

    def insert_into_user(self, username, email, location, password):
        """
        Query to add a new user
        :admin,user
        """
        user = """INSERT INTO users
            (username, email, location, password)
            VALUES ('{}','{}','{}','{}');
            """.format(username, email, location, password)
        self.cursor.execute(user)
        self.connection.commit()

    def add_to_menu(self, meal, description, price):
        """
        Query to add food item to menu table in database
        """
        meal_query = """INSERT INTO menu(meal,description,price)
        VALUES('{}','{}','{}'); """.format(meal, description, price)
        self.cursor.execute(meal_query)
        self.connection.commit()

    def insert_into_orders(
            self, user_id, menu_id, meal, description, price, status
            ):
        """
        Query to add order to the database : user
        """
        order_query = """INSERT INTO orders(
                user_id, menu_id, meal, description, price, status)
                VALUES('{}','{}','{}','{}','{}','{}'); """.format(
                user_id, menu_id, meal, description, price, status)
        self.cursor.execute(order_query)
        self.connection.commit()

    def get_all_orders(self):
        """
        Query gets all that are recently available
        :admin
        """
        self.cursor.execute("SELECT * FROM orders")
        all_orders = self.cursor.fetchall()
        order_list = []
        for order in all_orders:
            order_list.append(order)
        return order_list

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        user_list = []
        for user in users:
            user_list.append(user)
        return user_list

    def get_order_by_value(self, table_name, table_colum, value):
        """
        Function  gets items from the
        same table with similar ids :admin
        """
        query = "SELECT * FROM {} WHERE {} = '{}';".format(
            table_name, table_colum, value)
        self.cursor.execute(query)
        results = self.cursor.fetchone()
        return results

    def fetch_menu(self):
        """
        Query gets all that are recently available food item on the menu
        :user
        """
        self.cursor.execute("SELECT * FROM menu")
        menu = self.cursor.fetchall()
        menu_list = []
        for item in menu:
            menu_list.append(item)
        return menu_list

    def get_order_history_for_a_user(self, user_id):
        """
        Select from orders where order.user_id = user.user_id
        :Admin
        """
        query = "SELECT * FROM  orders WHERE user_id = '{}';".format(user_id)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            return results
        return "you haven't ordered yet"

    def update_order_status(self, stat, id):
        """
        update table orders set status ='' where order_id = id 
        :Admin
        """
        status = ['New', 'processing', 'complete', 'cancelled']
        if stat in status:
            query = """UPDATE orders SET status = '{}'
                WHERE order_id ='{}' """.format(stat, id)
            self.cursor.execute(query)
            self.connection.commit()
            return "Order succcessfully Updated"
        return "Invalid Update status name"

    def update_role(self, role, email):
        query = """UPDATE users SET role = '{}'
            WHERE email ='{}' """.format(role, email)
        self.cursor.execute(query)
        self.connection.commit()

    def delete_table_column(self, table_name, table_colum, id):
        delete_query = "DELETE from {} WHERE {} = '{}';".format(
             table_name, table_colum, id)
        self.cursor.execute(delete_query)
        self.connection.commit()

    def drop_tables(self):
        drop_query = "DROP TABLE IF EXISTS {0} CASCADE"
        tables = ["users", "menu", "orders"]
        for table in tables:
            self.cursor.execute(drop_query.format(table))