class KanBanCommands():

    def __init__(self):
        pass
        
    def add_task(self,task):
        print(task," was added succesfully")
        
    def move_to_doing(self,task_id):
        print(task_id," was added to doing")
        
    def move_to_done(self,task_id):
        print(task_id," was added to done") 

    def show_todo_tasks(self):
        print("Showing todo tasks")        
        
    def show_ongoing_tasks(self):
        print("Showing ongoing tasks") 

    def show_completed_tasks(self):
        print("Showing completed tasks")         

    def show_all_tasks(self):
        print("Showing all tasks") 

    def show_version(self):
        print("1.0")        
            
      