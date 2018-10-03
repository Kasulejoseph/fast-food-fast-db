import psycopg2
from flask import current_app as app

class Database(object):
    """class for app database"""

    def __init__(self):
        """initialize db connection """
        self.connection = psycopg2.connect(
        """
        dbname ='food_db' user='postgres' password ='password'
        host='127.0.0.1' port='5432'
        """
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        try:
           if app.config['TESTING']:
                self.connection = psycopg2.connect(
                """
                dbname ='test_db' user='postgres' password ='password'
                host='127.0.0.1' port='5432'
                """
                ) 
        except Exception as e:
            print(e)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """ create tables """
        create_table = """CREATE TABLE IF NOT EXISTS users
        (user_id SERIAL PRIMARY KEY, username VARCHAR(30),
        email VARCHAR(100), location VARCHAR(100), password VARCHAR(150))"""
        self.cursor.execute(create_table)

        create_table = """ CREATE TABLE IF NOT EXISTS menu(
        menu_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        meal VARCHAR(40), description VARCHAR(200),
        price INT NOT NULL, status VARCHAR(30))"""
        self.cursor.execute(create_table)

        create_table = """ CREATE TABLE IF NOT EXISTS orders(
        order_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, menu_id INTEGER NOT NULL,
        meal VARCHAR(40), description VARCHAR(200), price INT, status VARCHAR(30), 
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(menu_id) REFERENCES menu(menu_id) ON UPDATE CASCADE ON DELETE CASCADE)"""
        self.cursor.execute(create_table)     

    def insert_into_user(self,username,email,location,password):
        """
        Query to add a new user 
        :admin,user
        """
        user = """INSERT INTO users (username, email, location,password) VALUES
        ('{}','{}','{}','{}'); """.format(username,email,location,password)
        self.cursor.execute(user)
        self.connection.commit()

    def add_to_menu(self,user_id, meal,description, price):
        """
        Query to add food item to menu table in database
        :admin 
        """
        meal_query = """INSERT INTO menu(meal,description,price)
        VALUES('{}','{}','{}','{}'); """.format(user_id,meal,description,price)
        self.cursor.execute(meal_query)
        self.connection.commit()

    def insert_into_orders(self,user_id, menu_id, meal,description,price,status):
        """
        Query to add order to the database 
        :user
        """
        order_query = """INSERT INTO orders(user_id, menu_id, meal, description, price, status)
        VALUES('{}','{}','{}','{}','{}','{}'); """.format(user_id, menu_id, meal, description, price, status)
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

    def get_order_by_value(self,table_name,table_colum,value):
        """
        Function  gets items from the
        same table with similar ids 
        :admin
        """
        query = "SELECT * FROM {} WHERE {} = '{}';".format(
            table_name,table_colum,value)
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
        return  menu_list

    def get_order_history_for_a_user(self):
        """
        Select from orders where order.user_id = user.user_id
        :Admin
        """
        pass
    
    def update_order_status(self,stat, id):
        """
        update table orders set status ='' where order_id = id 
        :Admin
        """
        status = ['New','processing','complete','cancelled']
        if stat in status:
            query = "UPDATE orders SET status = '{}' WHERE order_id ='{}' ".format(stat,id)
            self.cursor.execute(query)
            self.connection.commit()
            return "Order succcessfully Updated"
        return "Invalid Update status name"

    def drop_tables(self):
        drop_query = "DROP TABLE IF EXISTS {0} CASCADE"
        tables = ["users","menu","orders"]
        for table in tables:
            self.cursor.execute(drop_query.format(table))
