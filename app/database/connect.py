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
        menu_id SERIAL PRIMARY KEY, meal VARCHAR(40), description VARCHAR(200),
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

    def add_to_menu(self):
        """
        Query to add food item to menu table in database
        :admin 
        """
        order_query = """INSERT INTO menu(meal,description,price)
        VALUES('{}','{}','{}'); """.format(meal,description,price)
        self.cursor.execute(order_query)
        self.connection.commit()

    def insert_into_orders(self,meal,description,price):
        """
        Query to add order to the database 
        :user
        """
        order_query = """INSERT INTO orders(meal,description,price)
        VALUES('{}','{}','{}'); """.format(meal,description,price)
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

    def get_order_by_id(self,table_name,table_colum,order_id):
        """
        Function  gets items from the
        same table with similar ids 
        :admin
        """
        self.cursor.execute("SELECT FROM {} WHERE {} = '{}'").format(
            table_name,table_colum,order_id)
        results = self.cursor.fetchall()
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
    
    def update_order_status(self,id):
        """
        update table orders set status ='' where order_id = id 
        :Admin
        """
        status = ['New','processing','complete','cancelled']
        if stat in status:
            self.cursor.execute("UPDATE orders SET status = {} WHERE order_id ={} ").format(stat,id)


