import sqlite3 as lite
import time


class KanBanCommands:
    """Class defines all the required command handlers"""
       
    def __init__(self):
        
        # initialise some properties
        self.task = ''
        self.connection = None
        self.cursor = None
        self.rows = ''
        
        
    def add_task(self,task):
        """Method takes new task name from user and adds to database"""
        
        self.task = task
        try:
            self.connection = lite.connect('kanban.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute('INSERT INTO todo (task_name) VALUES (?)',(self.task,))
            self.connection.commit() 
            
            print('\n',self.task ,' was added successfully')
            
        except Exception as e:
            # rollback in case of errors
            self.connection.rollback() 
            
            print("\nPlease try again")

        finally:
            self.connection.close()            
                
                
        
    def move_to_doing(self,task_id):
        print(task_id," was added to doing")
        
    def move_to_done(self,task_id):
        print(task_id," was added to done") 

    def show_todo_tasks(self):
        """Method displays pending tasks"""
        
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM todo')
            self.rows = self.cursor.fetchall()
            
            
            print("\n\n\t\t\tTask ID\t|\tTask name")
            print('\t\t\t-------------------------------------------')
            
            for row in self.rows:
                print('\t\t\t',row['task_id'],'\t|\t',row['task_name'])
                print('\t\t\t-------------------------------------------')
        except Exception as e:
            self.connection.rollback() 
            
            print("\nPlease try again")

        finally:
            self.connection.close()
            
        
    def show_ongoing_tasks(self):
        print("Showing ongoing tasks") 

    def show_completed_tasks(self):
        print("Showing completed tasks")         

    def show_all_tasks(self):
        print("Showing all tasks") 

    def show_version(self):
        print("1.0") 
      
