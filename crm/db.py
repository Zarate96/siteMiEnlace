import mysql.connector
from django.conf import settings

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.connection
        except mysql.connector.Error as err:
            print(err)
            return False
        
    def cursor(self):
        db = self.connect()
        return db.cursor()
    
    def excute_query(self, query):
        mycursor = self.cursor()
        try:
            mycursor.execute(query)
            return mycursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            return False
        
    
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

