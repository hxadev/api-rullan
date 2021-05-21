import mysql.connector


class Connection:
    __instance = None
    @staticmethod
    def getConnection():
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        
        if Connection.__instance != None:
            raise Exception("Ya existe una instacia")
        else:
            Connection.__instance = self.__connect();

    def __connect(self):
        connection=mysql.connector.connect(
            host="192.168.0.15",
            user="developer",
            password="posihx14",
            database="presupuestos_fii"
        )
        
        print("connected...")
        
        return connection;  