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
        self.current_time = 0
        self.temp_time = 0
        self.total_time = 0
        self.completed_tasks_list = []
        self.ongoing_tasks_list = []
        self.todo_tasks_list = []
        self.headers = []
        self.temp = []
        self.table = []
        self.max = 0
        self.list_all = []
        self.count = 0
        self.max_len1 = 0
        self.max_len2 = 0
        self.max_len3 = 0
        self.list_todo = []
        self.list_ongoing = []
        self.list_complete = []
        self.item1 = ''
        self.item2 = ''
        self.item3 = ''
                
        
    def get_max_len(self,alist):
            
        self.max = 0
        for item in alist:
            
            if len(item['task_name']) > self.max:
                self.max = len(item['task_name'])
        return self.max 

    def get_max_len2(self,alist,pos):
            
        self.max = 0
        for item in alist:
            
            if len(item[pos]) > self.max:
                self.max = len(item[pos])
        return self.max             
        
                
        
    def add_task(self,task):
        """Method takes new task name from user and adds to database"""
        
        self.task = task
        try:
            self.connection = lite.connect('kanban.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute('INSERT INTO todo (task_name,valid) VALUES (?,?)',(self.task,1))
            self.connection.commit() 
            
            print('\n\t',self.task ,' was added successfully')
            
        except Exception as e:
            # rollback in case of errors
            self.connection.rollback() 
            
            print("\nPlease try again")

        finally:
            self.connection.close()
         
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
        
        # if task id is valid, check whether exists in table doing   
        if self.task:
        
            try:
                self.connection = lite.connect('kanban.db')
                self.connection.row_factory = lite.Row
                self.cursor = self.connection.cursor()
                self.cursor.execute('SELECT * FROM doing WHERE taskID = ?',(self.taskID,))
                self.rows = self.cursor.fetchone()
                
                if self.rows:
                    print('\n\t',self.task ,'with ID ',self.taskID,' is already in doing list')
                    self.task = ''
            except Exception as e:
               
                print(e,"\nPlease try again")
                  
            finally:
                self.connection.close()
            
            if self.task:
            
                self.time_in = str(time.time()) 

                
                try:
                    self.connection = lite.connect('kanban.db')
                    self.cursor = self.connection.cursor()
                    self.cursor.execute('INSERT INTO doing (taskID,task_name,time_in) VALUES (?,?,?)',(self.taskID,self.task,self.time_in))
                    self.row_count = self.cursor.rowcount
                    self.connection.commit()
                    
                except Exception as e:
                   
                    print("\nPlease try again-2")

                finally:
                    self.connection.close()

                # if insertion into table doing was successfull, 
                # update task status in table todo 
                if self.row_count:
                 
                    self.row_count = 0       
                    try:
                        self.connection = lite.connect('kanban.db')
                        self.cursor = self.connection.cursor()
                        self.cursor.execute('UPDATE todo SET valid = ? WHERE task_id = ?',(0,self.taskID))
                        self.connection.commit()
                        self.row_count = self.cursor.rowcount

                    except Exception as e:
                       
                        print("\nPlease try again")
                            
                    finally:
                        self.connection.close()
                    
                    # if success, display success message            
                    if self.row_count:
                        print('\n\t',self.task, ' with id ',self.taskID,' was added to the ongoing tasks')            

                        
        
    def move_to_done(self,task_id):
        """Method takes existing task id and
           moves associated task from 
           table doing to table done
        """

        # ensure that i'm working with an int 
        self.taskID = int(str(task_id).strip())
        self.rows = None
        self.task = ''
        
        # check if the task id from user exists in table doing
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM doing WHERE taskID = ?',(self.taskID,))
            self.rows = self.cursor.fetchone() 
            
            if self.rows:
                self.task = self.rows['task_name']
                self.time_in = self.rows['time_in']
            else:
                print('\n\t\t Invalid ID - Please use list doing command to see valid task IDs')
            
        except Exception as e:
           
            print(e,"\nPlease try again")
              
        finally:
            self.connection.close()
        
        # if task id is valid, cinsert into table done   

        if self.task:
        
            self.current_time = time.time()
            
            # current timestamp - time_in timestamp
            self.total_time = self.current_time - float(self.time_in)
            self.total_time = str(self.total_time).split('.')[0]
            self.total_time = int(self.total_time)
            
            # format time taken depending on duration
            if self.total_time < 60:
                self.total_time = str(self.total_time) + ' Seconds'
            elif self.total_time > 60 and self.total_time < 3600:
                self.total_time = self.total_time//60 
                if self.total_time > 1:
                    self.total_time = str(self.total_time) + ' Minutes'                    
                else:
                    self.total_time = str(self.total_time) + ' Minute'
            else:
                self.total_time = self.total_time//3600
                if self.total_time > 1:
                    self.total_time = str(self.total_time) + ' Days'                    
                else:
                    self.total_time = str(self.total_time) + ' Day'
                
            try:
                self.connection = lite.connect('kanban.db')
                self.cursor = self.connection.cursor()
                self.cursor.execute('INSERT INTO done (taskId,task_name,time_out) VALUES (?,?,?)',(self.taskID,self.task,self.total_time))
                self.row_count = self.cursor.rowcount
                self.connection.commit()

            except Exception as e:
               
                print("\nPlease try again")

            finally:
                self.connection.close()

        # if insertion into table done was successfull, delete task from table doing 
        if self.row_count:
         
            self.row_count = 0       
            try:
                self.connection = lite.connect('kanban.db')
                self.cursor = self.connection.cursor()
                self.cursor.execute('DELETE FROM doing WHERE taskID = ?',(self.taskID,))
                self.connection.commit()
                self.row_count = self.cursor.rowcount
                
            except Exception as e:
               
                print("\nPlease try again")
                    
            finally:
                self.connection.close()
            
            # if success, display success message            
            if self.row_count:
                print('\n\t',self.task, ' with id ',self.taskID,' was added to the completed tasks list')
      

    def fetch_todo_tasks(self):
        """Method fetches all pending tasks and returns
           them in a list or False if none"""
        self.todo_tasks_list = []
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM todo WHERE valid = 1')
            self.connection.commit()
            self.rows = self.cursor.fetchall()
            
            if self.rows:
            
                for row in self.rows: 
                    self.todo_tasks_list.append( {'task_id':row['task_id'],
                                                  'task_name':row['task_name']}
                                                )
                return self.todo_tasks_list 
               
            else:
                return [] 
         
        except Exception as e:
            
            print("\nPlease try again")

        finally:
            self.connection.close()

      
                
    def fetch_ongoing_tasks(self):

        """Method fetches all ongoing tasks and returns 
           in a list or False if none"""
        self.ongoing_tasks_list = []
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM doing')
            self.rows = self.cursor.fetchall()
            
            if self.rows:
               
               for row in self.rows: 
                    self.ongoing_tasks_list.append( {'taskID':row['taskID'], 
                                                       'task_name':row['task_name'],
                                                       'time_in':row['time_in']}
                                                    )
               return self.ongoing_tasks_list                     
            else:
                return []     
                
        except Exception as e:
            
            print("\nPlease try again")

        finally:
            self.connection.close()     
                
    
    def fetch_completed_tasks(self):

        """Method fetches all completed tasks and returns in a list
           or returns False if none
        """ 
        self.completed_tasks_list = []
        try:
            self.connection = lite.connect('kanban.db')
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT * FROM done')
            self.rows = self.cursor.fetchall()
            
            if self.rows:            
                
                for row in self.rows:
                    self.completed_tasks_list.append( {'taskId':row['taskId'],
                                                       'task_name':row['task_name'],
                                                       'time_out':row['time_out']}
                                                    )
                return self.completed_tasks_list                     
            else:
                return []            
                
        except Exception as e:
            
            print("\nPlease try again")

        finally:
            self.connection.close() 
                
                

    def show_todo_tasks(self):
        """Method displays pending tasks"""
        
        # returns a list of all todo tasks or False if none
        self.rows = []
        self.rows = self.fetch_todo_tasks()
            
        if type(self.rows) is list and len(self.rows) > 0:
            
            
            print("\n\tTASK ID\t|\tTASK NAME")
            print('\t-------------------------------------------')
            
            
            for row in self.rows:
                print('\t',row['task_id'],'\t|\t',row['task_name'])
                print('\t-------------------------------------------')
              
         
          
        else:
            print('\n\tThere are no pending tasks in the todo list')
                
        self.rows.clear()
            
        
    def show_ongoing_tasks(self):
        """Method displays ongoing tasks"""

        # returns list of all ongoing tasks
        self.rows = []
        self.rows = self.fetch_ongoing_tasks()
        
        if type(self.rows) is list and len(self.rows) > 0:
            self.max = self.get_max_len(self.rows) 
        
        
            print("\n\n\tTask ID\t|\tTask name\t\t\t|\tTime taken")
            print('\t-------------------------------------------------------------------')
            
            self.current_time = time.time()
          
            for row in self.rows:

                # current timestamp - time_in timestamp
                self.temp_time = self.current_time - float(row['time_in'])
                self.temp_time = str(self.temp_time).split('.')[0]
                self.temp_time = int(self.temp_time)
                
                if self.temp_time < 60:
                    self.temp_time = str(self.temp_time) + ' Seconds'
                elif self.temp_time > 60 and self.temp_time < 3600:
                    self.temp_time = self.temp_time//60 
                    if self.temp_time > 1:
                        self.temp_time = str(self.temp_time) + ' Minutes'                    
                    else:
                        self.temp_time = str(self.temp_time) + ' Minute'
                else:
                    self.temp_time = self.temp_time//3600
                    if self.temp_time > 1:
                        self.temp_time = str(self.temp_time) + ' Hours'                    
                    else:
                        self.temp_time = str(self.temp_time) + ' Hour'
                        
                print('\t',row['taskID'],'\t|\t',row['task_name'].ljust(self.max),'\t|\t',self.temp_time)
                print('\t-------------------------------------------------------------------')
                
        
            
        else:
            print('\n\tThere are no pending tasks in the ongoing tasks list')            
                
        self.rows.clear()


    def show_completed_tasks(self):
        """Method displays all completed tasks"""
        
        # returns a list of completed tasks or False if none
        self.rows = []
        self.rows = self.fetch_completed_tasks()
        
        if self.rows:
            self.max = self.get_max_len(self.rows)
        
                   
            print("\n\n\tTask ID\t|\tTask name\t\t\t|\tTime taken")
            print('\t---------------------------------------------------------------------')
          
            for row in self.rows:

                        
                print('\t',row['taskId'],'\t|\t',row['task_name'].ljust(self.max),'\t|\t',row['time_out'])
                print('\t---------------------------------------------------------------------')
                
                
        else:
            print('\n\tThere are currently no tasks in the completed tasks list')            
        
        self.rows.clear()        
 

    def show_all_tasks(self):
        """Method displays the whole kanban board of todo
           doing and done tasks"""
        
        self.completed_tasks_list = []
        self.ongoing_tasks_list = []
        self.todo_tasks_list = []
        self.list_todo = []
        self.list_ongoing = []
        self.list_complete = []
        
        self.completed_tasks_list = self.fetch_completed_tasks()
        self.ongoing_tasks_list = self.fetch_ongoing_tasks()
        self.todo_tasks_list = self.fetch_todo_tasks()
        
        if (self.completed_tasks_list and
            self.ongoing_tasks_list and
            self.todo_tasks_list):
            
            for item in self.todo_tasks_list:
                self.list_todo.append(item['task_name'])
            
            for item in self.ongoing_tasks_list:
                self.list_ongoing.append(item['task_name'])
                
            for item in self.completed_tasks_list:
                self.list_complete.append(item['task_name'])
                
                
            # get length of largest list
            self.max = max(len(self.list_todo),len(self.list_ongoing),len(self.list_complete))
            
            # create new list of all tasks from the 3 lists
            if len(self.list_todo) < self.max:
                
                # extract from list todo
                for item in self.list_todo:
                    
                    self.list_all.append([item])
                    
                for i in range(self.max-len(self.list_todo)):
                    self.list_all.append(['none'])
                    
            else:
                for item in self.list_todo:
                    self.list_all.append([item]) 
                    

            if len(self.list_ongoing) < self.max:
                
                # extract from list doing
                self.count = 0
                for item in self.list_ongoing:
                    self.list_all[self.count].insert(1,item)
                    self.count+=1
                    
                
                for i in range(self.max-len(self.list_ongoing)):
                    self.list_all[self.count].insert(1,'none')
                    self.count+=1
            else:
                self.count = 0
                for item in self.list_ongoing:
                    self.list_all[self.count].insert(1,item)
                    self.count+=1  
                    

            if len(self.list_complete) < self.max:
                
                # extract from list done
                self.count = 0
                for item in self.list_complete:
                    self.list_all[self.count].insert(2,item)
                    self.count+=1
                    
                    
                for i in range(self.max-len(self.list_complete)):
                    self.list_all[self.count].insert(2,'none')
                    self.count+=1
                    
            else:
                self.count = 0
                for item in self.list_complete:
                    self.list_all[self.count].insert(2,item)
                    self.count+=1                 
            
            # get length of longest string in list
            # for purpooses of display
            self.max_len1 = self.get_max_len2(self.list_all,0)
            self.max_len2 = self.get_max_len2(self.list_all,1)
            self.max_len3 = self.get_max_len2(self.list_all,2) 
            
            
            
            print("\n\n\t\tTODO TASKS\t\t|\tDOING TASKS\t\t|\tDONE TASKS")
            print('\t----------------------------------------------------------------------------------') 
            
            
            
            for item in self.list_all:
                
                if item[0] == 'none':
                    self.item1 = ''
                else:
                    self.item1 = item[0]
                    
                if item[1] == 'none':
                    self.item2 = ''
                else:
                    self.item2 = item[1]    

                if item[2] == 'none':
                    self.item3 = ''
                else:
                    self.item3 = item[2]    
                    
                print('\t',self.item1.ljust(self.max_len1),'\t|',self.item2.ljust(self.max_len2),'\t|',self.item3.ljust(self.max_len3))
                print('\t----------------------------------------------------------------------------------')
                    
            self.list_all.clear()  
        else:
            print('\n\tSome lists are not populated, please populate the lists first')        
                

    def show_version(self):
        print("1.0")        
            
      