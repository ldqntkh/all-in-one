
import os
import sqlite3

SQL_PATH = "../database/db.sqlite3"

class DBHelperFunctions:
    def __init__(self):
        self.conn = None
        
    def getConnection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(SQL_PATH)
            
    def destroyConnection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            
    def getUserByUserName(self, username):
        self.getConnection()
        
        sqlCommand = 'SELECT * from auth_user WHERE username="' + username + '"'
        rows = self.conn.execute(sqlCommand)
        user = None
        for row in rows:
            user = row
            break
        self.destroyConnection()
        return user
    
    def getUserById(self, userId):
        self.getConnection()
        
        sqlCommand = 'SELECT * from auth_user WHERE id='+str(userId)
        rows = self.conn.execute(sqlCommand)
        user = None
        for row in rows:
            user = row
            break
        self.destroyConnection()
        return user