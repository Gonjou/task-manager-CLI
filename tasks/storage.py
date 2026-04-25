import os
import json

class TaskStorage:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file

    def load_tasks(self):
        tasks = []
        
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as file:
                tasks = json.load(file)
        
        if not self.tasks_file:
            print("No saved data found. Starting new file.")

        return tasks

    def save_tasks(self, tasks):
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

    def add_task(self, tasks, title, description, due_date):
        task = {"title": title, "description": description, "due_date": due_date}
        tasks.append(task)

obj = TaskStorage()
obj.load_tasks()
tasks = []
obj.add_task(tasks, "hello", "a greeting", "1990")
obj.save_tasks(tasks)


