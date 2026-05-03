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
        
        if not self.tasks_file:
            print("No saved data found. Starting new file.")

        return tasks

    def save_tasks(self, tasks):
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

    def add_task(self, tasks, title, description, due_date):
        task = {"title": title, "description": description, "due_date": due_date, "completed": False}
        tasks.append(task)

    def list_tasks(self, tasks): # format this into a table
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task['title']} - Due: {task['due_date']} - {'Completed' if task['completed'] else 'Incomplete'}")

    def delete_task(self, tasks, index):
        tasks.pop(index - 1)

    def search_task(self, tasks, index):
        print(tasks[index - 1])

    def mark_as_completed(self, tasks, index):
        tasks[index - 1]["completed"] = True


obj = TaskManager()
obj.load_tasks()
tasks = []
obj.add_task(tasks, "hello", "a greeting", "1990")
obj.mark_as_completed(tasks, 1)

obj.save_tasks(tasks)



