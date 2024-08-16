# Final project: Task Manager

import argparse
import pickle
from datetime import datetime
import os

class Task:
    """Representation of a task
  
    Attributes:
              - created - date
              - completed - date
              - name - string
              - unique id - number
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional
    """
    def __init__(self, name, priority=1, due_date=None):
        self.name = name
        self.priority = priority
        self.id = None
        self.created = datetime.now()
        self.completed = None
        self.due_date = due_date

    def complete(self):
        self.completed = datetime.now()





class Tasks:
    """A list of `Task` objects."""
    
    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = [] 
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(".todo.pickle"):
            try:
                with open(".todo.pickle", "rb") as f:
                    self.tasks = pickle.load(f)
            except EOFError:
                print("Error: The pickle file is empty or corrupted.")
        else:
            with open(".todo.pickle", "wb") as f:
                pickle.dump(self.tasks, f)

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open(".todo.pickle", "wb") as f:
            pickle.dump(self.tasks, f)

    def add(self, name, priority=1, due_date=None):
        task = Task(name, priority, due_date)
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        self.pickle_tasks()
        print(f"Created task {task.id}")
   
    def list(self):
        incomplete = [task for task in self.tasks if task.completed == None]
        incomplete.sort(key=lambda x: (x.due_date or datetime.max, -x.priority))
        print(f"{'ID':<5}{'Age':<5}{'Due Date':<11}{'Priority':<11}{'Task'}")
        print("--   ---  --------   --------   ----")
        for task in incomplete:
            age = (datetime.now() - task.created).days
            due_date = task.due_date.strftime('%m/%d/%Y') if task.due_date else "-"
            print(f"{task.id:<5}{age:<5}{due_date:<11}{task.priority:<11}{task.name}")

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        print(f"No task with ID {task_id} found.")
        return None

    def done(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.complete()
            self.pickle_tasks()
            print(f"Completed task {task_id}")
    
    def delete(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.pickle_tasks()
            print(f"Deleted task {task_id}")
    
    def print_tasks(self, tasks):
        print(f"{'ID':<5}{'Age':<5}{'Due Date':<11}{'Priority':<11}{'Task':<30}{'Created':<30}{'Completed'}")
        print("--   ---  --------   --------   ----                          ---------------------------   -------------------------")
        for task in tasks:
            age = (datetime.now() - task.created).days
            due_date = task.due_date.strftime('%m/%d/%Y') if task.due_date else "-"
            created = task.created.strftime('%c')
            completed = task.completed.strftime('%c') if task.completed else "-"
            print(f"{task.id:<5}{age:<5}{due_date:<11}{task.priority:<11}{task.name:<30}{created:<30}{completed}")

    def report(self):
        self.print_tasks(self.tasks)

    def query(self, search_terms):
        matching_tasks = [task for task in self.tasks if any(term.lower() in task.name.lower() for term in search_terms) and task.completed == None]
        if matching_tasks:
            self.print_tasks(matching_tasks)
        else:
            print("No matching tasks found")


   

def main():
    """All the real work that drives the program"""
    parser = argparse.ArgumentParser(description='Update your ToDo list.')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument('--due', type=str, required=False, help='due date in MM/DD/YYYY format')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1 (1=low, 2=medium, 3=high)')
    parser.add_argument('--query', type=str, required=False, nargs='+', help="query tasks by keyword")
    parser.add_argument('--list', action='store_true', required=False, help="list all tasks that have not been completed")
    parser.add_argument('--done', type=int, required=False, help='mark a task as completed')
    parser.add_argument('--delete', type=int, required=False, help='delete a task')
    parser.add_argument('--report', action='store_true', required=False, help="a report of all tasks")
    # Parse the argument
    args = parser.parse_args()

    # Create instances of Tasks
    task_list = Tasks()

    # Read out arguments (note the types)
    if args.add:
        due_date = datetime.strptime(args.due, "%m/%d/%Y") if args.due else None
        print(f"We need to add {args.add} to our todo list with a priority of {args.priority}.")
        task_list.add(args.add, args.priority, due_date)
    elif args.query:
        task_list.query(args.query)
    elif args.list:
        task_list.list()
    elif args.done:
        task_list.done(args.done)
    elif args.delete:
        task_list.delete(args.delete)
    elif args.report:
        print("Print out the report")
        task_list.report()

    # Read out arguments (note the types)
    # print("Add:", args.add)
    # print("Due:", args.due)
    # print("Priority:", args.priority)
    # print("List:", args.list)
    # print("Query:", args.query)


if __name__ == "__main__":
    main()