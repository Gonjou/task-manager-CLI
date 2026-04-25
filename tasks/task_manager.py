import os
import json

class TaskManager:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file

    def load_tasks(self):
        tasks_file = []
        
        if os.path.exists(tasks_file):
            with open(tasks_file, "r") as file:
                tasks_file = json.load(file)
        
        if not tasks_file:
            print("No saved data found. Starting new file.")

        return tasks_file

    def save_tasks(tasks, tasks_file):
        with open(tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

    def add_task(self, task):
        ...