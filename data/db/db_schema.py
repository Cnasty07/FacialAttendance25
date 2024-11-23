import os
import sqlite3

#main code 
class DBSchema:
    """_summary_
    This class is used to create the database schema for the records.db database.
    """
    
    def __init__(self):
        """_summary_
        This is the constructor method for the DBSchema class.
        """
        self.connection_obj = sqlite3.connect('./data/db/records.db')
        self.cursor_obj = self.connection_obj.cursor()
        self.cursor_obj.execute("PRAGMA foreign_keys = ON;")
        
        
    def create_db(self):
        """_summary_ 
        This method creates the database schema for the records.db database.
        """
        
        Class_table = '''
            CREATE TABLE IF NOT EXISTS Class (
            CLASS_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ROOM_NUM INTEGER NOT NULL,
            CLASS_NAME CHAR(30),
            CLASS_DESCRIPTION CHAR(30),
            START_DATE TEXT,
            END_DATE TEXT,
            SCHEDULE CHAR(30)
            ); '''
            
        Student_table = """ 
            CREATE TABLE IF NOT EXISTS Student (
            STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CLASS_ID INTEGER,
            STUDENT_NAME TEXT,
            FOREIGN KEY (CLASS_ID)
                REFERENCES Class(CLASS_ID)
            
            ); """
            
        Attendance_table = """CREATE TABLE IF NOT EXISTS Attendance (
            ATTENDANCE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENT_ID INTEGER,
            CLASS_ID INTEGER,
            ATTENDANCE_DATE TEXT NOT NULL,
            ATTENDANCE_STATUS TEXT NOT NULL,
            FOREIGN KEY (CLASS_ID) REFERENCES Class(CLASS_ID),
            FOREIGN KEY (STUDENT_ID) REFERENCES Student(STUDENT_ID)
            ); """
            
        self.cursor_obj.execute(Class_table)
        self.cursor_obj.execute(Student_table)
        self.cursor_obj.execute(Attendance_table)
        print("Database created successfully", self.cursor_obj.fetchall())
        self.close_db()
        

    # just in case needed for later
    def close_db(self):
        """_summary_
        This method closes the connection to the database.
        """
        self.connection_obj.close()
    



def main():
    new_init_db = DBSchema()
    new_init_db.create_db()
    

if __name__ == '__main__':
    main() 
