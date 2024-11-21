import os
import sqlite3


#main code 
class DB_Controller:
    def __init__(self):
        self.connection_obj = sqlite3.connect('data/db/records.db')
        self.cursor_obj = self.connection_obj.cursor()
    
    def new_entry(self):
        pass
    
    def close_db(self):
        self.connection_obj.close()
    


def main():
    pass

if __name__ == '__main__':
    main() 
