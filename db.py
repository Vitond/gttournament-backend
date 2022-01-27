from config import config
import mysql.connector

def getConnection():
    db = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        autocommit=True
    )
    return db