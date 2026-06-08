import os
import json

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

    def add_task(self, tasks, title, description, due_date):
        task = {"title": title, "description": description, "due_date": due_date, "completed": False}
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
        
        task = tasks[index - 1]
        task["title"] = title
        task["due_date"] = due_date
        task["description"] = description








