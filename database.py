import sqlite3

class create_db(object):
    """Class defines method to create application database"""
	
    def __init__(self):
        
     self.table1 = "CREATE TABLE IF NOT EXISTS todo (task_id INTEGER PRIMARY KEY,task_name TEXT)"
     self.table2 = "CREATE TABLE IF NOT EXISTS doing (row_id INTEGER PRIMARY KEY,taskID)"
     self.table3 = "CREATE TABLE IF NOT EXISTS done (row_id INTEGER PRIMARY KEY,taskId)"
     
     self.connection = None
     self.cursor = None
     
    def run_script(self):

           try:
               self.connection = sqlite3.connect('kanban.db')
               self.cursor = self.connection.cursor()
               self.cursor.execute(self.table1)
               self.cursor.execute(self.table2)
               self.cursor.execute(self.table3)

           except sqlite3.Error as e:
               
               if self.connection:
                   self.connection.rollback()
                   return False
           finally:
               self.connection.close()
           
           return True


		
		