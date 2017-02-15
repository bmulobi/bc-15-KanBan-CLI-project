import sqlite3 as lite
import time


class KanBanCommands:
    """Class defines all the required command handlers"""
       
    def __init__(self):
        
        # initialise some properties
        self.task = ''
        self.taskID = ''
        self.connection = None
        self.cursor = None
        self.rows = None
        self.time_in = ''
        self.row_count = 0
        
        
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
            
    """       self.table1 = "CREATE TABLE IF NOT EXISTS todo (task_id INTEGER PRIMARY KEY,task_name TEXT)"
     self.table2 = "CREATE TABLE IF NOT EXISTS doing (row_id INTEGER PRIMARY KEY,taskID INT,task_name TEXT,time_in TEXT)"
     self.table3 = "CREATE TABLE IF NOT EXISTS done (row_id INTEGER PRIMARY KEY,taskId INT,task_name TEXT,time_out TEXT)"
    """     
                
        
    def move_to_doing(self,task_id):
        """Method takes existing task id and
           moves associated task from 
           table todo to table doing
        """

        # ensure that i'm working with an int 
        self.taskID = int(str(task_id).strip())
        
        # check if the task id from user exists in table 
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM todo WHERE task_id = ?',(self.taskID,))
            self.rows = self.cursor.fetchone()
            
            if self.rows:
                self.task = self.rows['task_name']
            else:
                print('\n\t\t Invalid ID - Please use list todo command to see valid task IDs')
            
        except Exception as e:
           
            print(e,"\nPlease try again-1")
              
        finally:
            self.connection.close()
        
        # if task id is valid, insert task into table doing   
        if self.task:
            
            self.time_in = time.time()    
            try:
                self.connection = lite.connect('kanban.db')
                self.cursor = self.connection.cursor()
                self.cursor.execute('INSERT INTO doing (taskID,task_name,time_in) VALUES (?,?,?)',(self.taskID,self.task,self.time_in))
                self.row_count = self.cursor.rowcount
            except Exception as e:
               
                print("\nPlease try again-2")

            finally:
                self.connection.close()

        # if insertion into table doing was successfull, delete task from table todo 
        if self.row_count:
         
            self.row_count = 0       
            try:
                self.connection = lite.connect('kanban.db')
                self.cursor = self.connection.cursor()
                self.cursor.execute('DELETE FROM todo WHERE task_id = ?',(self.taskID,))
                self.connection.commit()
                self.row_count = self.cursor.rowcount

            except Exception as e:
               
                print("\nPlease try again")
                    
            finally:
                self.connection.close()
            
            # if success, display success message            
            if self.row_count:
                print('\n',self.task, ' with id ',self.taskID,' was added to the ongoing tasks')            

                        
        
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
      
