import os
import json
import re

class TaskManager:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file

    def load_tasks(self):
        tasks = []
        
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as file:
                tasks = json.load(file)
        
        if not tasks:
            return tasks

        return tasks

    def save_tasks(self, tasks):
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

    def _validate_index(self, index, tasks):
        try:
            index = int(index)
        except ValueError:
            raise ValueError("Task index must be a number.")
        
        if index < 1:
            raise ValueError("Index must be greater than 0.")
        
        if index > len(tasks):
            raise IndexError("This task does not exist.")
        
        return index

    def _validate_title(self, title):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        return title

    def _validate_due_date(self, due_date):
        validation = re.search(r"^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$", due_date)

        if not validation:
            raise ValueError("Invalid date format. Use YYYY-MM-DD. Example: 2026-04-12")
    
        return due_date
    
    def add_task(self, tasks, title, description, due_date):
        title = self._validate_title(title)
        due_date = self._validate_due_date(due_date)

        task = {"title": title, "description": description, "due_date": due_date, "completed": False, "today": False,
                "this_week": False}
        
        tasks.append(task)

    def list_tasks(self, tasks):
        return [
            [
                index,
                task["title"],
                task["due_date"],
                "Completed" if task["completed"] else "Incomplete"
            ]
            for index, task in enumerate(tasks, start=1)
            ]

    def sort_tasks(self, tasks, sort_by, reverse=False):

        sort_keys = {
            "title": lambda x: x["title"],
            "due date": lambda x: x["due_date"],
            "completion": lambda x: x["completed"]
            }
    
        if sort_by not in sort_keys:
            raise ValueError("Invalid sorting option")

        return sorted(tasks, key=sort_keys[sort_by], reverse=reverse)

    def assign_tasks(self, tasks, index, option):

        index = self._validate_index(index, tasks)
        task = tasks[index - 1]

        if option == "1":
            task["today"] = True
        elif option == "2":
            task["this_week"] = True
        elif option == "3":
            task["today"] = False
        elif option == "4":
            task["this_week"] = False
        else:
            raise ValueError("Invalid choice")


    def delete_task(self, tasks, index):
        index = self._validate_index(index, tasks)
        
        tasks.pop(index - 1)
        

    def search_task(self, tasks, index):
        index = self._validate_index(index, tasks)
        
        try:
            return tasks[index - 1] 
        except TypeError as e:
            raise TypeError(e)
 

    def mark_as_completed(self, tasks, index):
        index = self._validate_index(index, tasks)
        
        tasks[index - 1]["completed"] = True


    def mark_as_incomplete(self, tasks, index):
        index = self._validate_index(index, tasks)
        
        tasks[index - 1]["completed"] = False

    def update_task(self, tasks, index, title, due_date, description):
        index = self._validate_index(index, tasks)
        title = self._validate_title(title)
        due_date = self._validate_due_date(due_date)
        
        task = tasks[index - 1]
        task["title"] = title
        task["due_date"] = due_date
        task["description"] = description



