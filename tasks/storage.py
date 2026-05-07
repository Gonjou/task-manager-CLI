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
            return "No saved data found. Starting new file."

        return tasks

    def save_tasks(self, tasks):
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

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
        tasks.pop(index - 1)

    def search_task(self, tasks, index):
        found_task = tasks[index - 1]
        return f"{found_task['title']} - {found_task['description']} - {found_task['due_date']} - {'Completed' if found_task['completed'] else 'Incomplete'}"

    def mark_as_completed(self, tasks, index):
        tasks[index - 1]["completed"] = True

    def update_task(self, tasks, index, title, due_date, description):
        if 0 < index <= len(tasks):
            task = tasks[index - 1]
            task["title"] = title
            task["due_date"] = due_date
            task["description"] = description






