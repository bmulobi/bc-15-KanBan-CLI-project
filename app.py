import re
from database import create_db
from commands import KanBanCommands

commands_object = KanBanCommands()
database_object = create_db() 

class Dispatch:
    """This class contains functionality to dispatch
       commands to the correct handler"""
       
    def __init__(self):
       
        self.menu = """
               AVAILABLE COMMANDS
               
               todo <taskname>
               doing <task-id>
               done <task-id>
               list todo
               list doing
               list done
               list all
               
               help
               version
               quit

               """
               
        # holds input from user               
        self.prompt = '' 

        # flags to determine which command has been entered
        self.todo_tasks = False
        self.ongoing_tasks = False
        self.done_tasks = False
        self.list_todo_tasks = False
        self.list_ongoing_tasks = False
        self.list_done_tasks = False
        self.list_all_tasks = False
        self.show_help = False
        self.show_version = False
              

    def display_menu(self):
        """This method displays the aplication's menu"""
        print(self.menu)
         
    def create_database(self):
        """Method ensures that the required database exists
           by creating it if it doesn't exist"""    
        database_object.run_script()
        
    def filter_commands(self):
        """This method filters user commands and calls the correct
           command handler"""
           
        # loop runs until user enters q or quit
        while self.prompt != 'q' and self.prompt != 'quit':
            
            # self.prompt the user for input
            self.prompt = input('\n\nEnter a command --> ')
            
            # update all flags to false on loop entry
            # to avoid activating commands incorrectly
            todo_tasks = False
            ongoing_tasks = False
            done_tasks = False
            list_todo_tasks = False
            list_ongoing_tasks = False
            list_done_tasks = False
            list_all_tasks = False
            show_help = False
            show_version = False
            

            try:
                # if command is todo(add_task), set associated flag to true
                if re.match('^todo\s{1}\w+',self.prompt) != None:
                    todo_tasks = True
                    
                # if command is doing(add task to ongoing list), set associated flag to true    
                if re.match(r'(doing) ([1-9])+',self.prompt) != None:
                    ongoing_tasks = True 

                # if command is done(add task to done list), set associated flag to true     
                if re.match(r'(done) ([1-9])+',self.prompt) != None:
                    done_tasks = True

                # if command is list todo(show pending tasks), set associated flag to true           
                if re.match('^list todo$',self.prompt) != None:
                    list_todo_tasks = True

                # if command is list doing(show ongoing tasks), set associated flag to true      
                if re.match('^list doing$',self.prompt) != None:
                    list_ongoing_tasks = True
                
                # if command is list done(show completed tasks), set associated flag to true 
                if re.match('^list done$',self.prompt) != None:
                    list_done_tasks = True
                
                # if command is list all(show all tasks), set associated flag to true                 
                if re.match('^list all$',self.prompt) != None:
                    list_all_tasks = True  
                
                # if command is help (show help menu), set associated flag to true 
                if re.match('^help$',self.prompt) != None:
                    show_help = True
                  
                # if command is version(show app version), set associated flag to true   
                if re.match('^version$',self.prompt) != None:
                    show_version = True

                           
                         
            except re.error as e:
                print(str(e))
                self.prompt = input('\n\n\nEnter a command - > ')
                self.prompt = self.prompt.strip()
                
            # if user input does not match a valid command
            # show the help menu            
            if (
                 not todo_tasks and not ongoing_tasks and not done_tasks 
                 and not list_todo_tasks and not list_ongoing_tasks 
                 and not list_done_tasks and not list_all_tasks 
                 and not show_help and not show_version
               ):
                self.display_menu()         
            
            # call todo command handler
            if todo_tasks:
                task_name = self.prompt.split(' ',1)[1] 
                commands_object.add_task(task_name)
            
            # call doing command handler            
            if ongoing_tasks:  
                task_id = self.prompt.split()[1]    
                commands_object.move_to_doing(task_id)
             
            # call done command handler 
            if done_tasks:  
                task_id = self.prompt.split()[1]    
                commands_object.move_to_done(task_id)  

            # call list todo command handler
            if list_todo_tasks:  
                commands_object.show_todo_tasks()    

            # call list doing command handler
            if list_ongoing_tasks:  
                commands_object.show_ongoing_tasks()

            # call list done command handler    
            if list_done_tasks:  
                commands_object.show_completed_tasks() 
            
            # call list all command handler
            if list_all_tasks:  
                commands_object.show_all_tasks()
            
            # show help menu
            if show_help:  
                self.display_menu()
                
            # show app version
            if show_version:  
                commands_object.show_version()  

obj = Dispatch()
obj.display_menu()
obj.create_database()
obj.filter_commands()
    