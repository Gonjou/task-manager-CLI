import os
import json
import re

class TaskManager:
    """
    A class that contains all the Task Manager methods.

    Attributes:
    tasks_file = a json file that contains a list with all the tasks (dicts).
    settings_file = a json file that contains a dict with some settings, like set_display_tasks_at_launch.
    """
    def __init__(self, tasks_file="tasks.json", settings_file="settings.json"):

        self.tasks_file = tasks_file
        self.settings_file = settings_file
      
    def load_tasks(self):
        """Load tasks.json. If this file doesn't exist, initialize the file with an empty list."""
        tasks = []
        
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as file:
                tasks = json.load(file)

        return tasks


    def save_tasks(self, tasks):
        """
        Save all the tasks.json changes once modified.

        Parameters:
        tasks: the tasks.json file
        
        """
        with open(self.tasks_file, "w") as file:
            json.dump(tasks, file, indent=2)

    def load_settings(self):
        """
        Load settings.json. If this file doesn't exist, initialize it with the default setting.

        default = {"display_tasks_at_launch": True}
        """
        settings = {"display_tasks_at_launch": True}

        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file: 
                settings = json.load(file) 
        return settings
    
    def save_settings(self, settings):
        """
        Save all changes in settings.json once modified.

        Parameters:
        settings: the settings.json file
        
        """
        with open(self.settings_file, "w") as file: 
            json.dump(settings, file, indent=2)

    def validate_index(self, index, tasks):
        """
        Validate task index. 

        Parameters:
        index (str, int): number (integer) to be validated
        tasks: the tasks.json file

        Returns:
        int: validated task index

        Raises:
        ValueError:
        - If task index is not a number, like 1, 2, 3, etc...
        - If task index is equal or less than 0
        - If task index targets a task that does not exist. For example, index = 6 when there are only 3 tasks
        """
        try:
            index = int(index)
        except ValueError:
            raise ValueError("Task index must be a number.")
        
        if index < 1:
            raise ValueError("Index must be greater than 0.")
        
        if index > len(tasks):
            raise IndexError("This task does not exist.")
        
        return index

    def validate_title(self, title):
        """
        Validate task title.

        Parameters:
        title (str): task title to be validated

        Returns:
        str: validated and stripped task title

        raises:
        Valuerror - if the user enters an empty title
        """
        if not title.strip():
            raise ValueError("Title cannot be empty")
        return title.strip()

    def validate_due_date(self, due_date):
        """
        Validates task due_date.

        Parameters:
        due_date (str): due_date string in YYYY-MM-DD format.

        Returns:
        str: validated due_date

        Raises:
        ValueError - When the user enters anything that is not a date in YYYY-MM-DD format.
        """
        validation = re.search(r"^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$", due_date)

        if not validation:
            raise ValueError("Invalid date format. Use YYYY-MM-DD. Example: 2026-04-12")
    
        return due_date
    
    def add_task(self, tasks, title, description, due_date):
        """
        Add new task to tasks.json. 

        Parameters:
        tasks: tasks.json file
        title (str): task title
        description (str): task description
        due_date (str): task due date in YYYY-MM-DD format

        Returns:
        dict: with all the task data. It is then appended to the list in tasks.json.
        """
        task = {"title": title, "description": description, "due_date": due_date, "completed": False, "today": False,
                "this_week": False}
        
        tasks.append(task)

    def list_tasks(self, tasks):
        """
        Lists all the tasks in tasks.json.

        Parameters:
        tasks: the tasks.json file.

        Returns:
        list: a list containing lists with all the tasks data. It enumerates all the tasks starting from 1.
        
        """
        return [
            [
                index,
                task["title"],
                task["due_date"],
                "Completed" if task["completed"] else "Incomplete"
            ]
            for index, task in enumerate(tasks, start=1)
            ]
    
    def validate_sort_option(self, choice):
        """
        Validates the sorting option for the sort_tasks() method.

        Parameters:
        choice (str): a number from 1 to 5.

        Returns:
        str: validated choice

        raises:
        ValueError - when choice is not a number from 1 to 5
        """
        valid_choices = ["1", "2", "3", "4", "5"]
        if choice not in valid_choices:
            raise ValueError("Invalid sorting option.")
        return choice
    
    def sort_tasks(self, tasks, choice, reverse=False):
        """
        Sorts tasks by title, due date or completion.

        Parameters:
        tasks: tasks.json file
        choice: sorting option, a number from 1 to 5
        
        Returns:
        list: another list containing all the tasks (dicts), now sorted depending on the user choice.
        """

        sort_keys = {
            "title": lambda x: x["title"],
            "due date": lambda x: x["due_date"],
            "completion": lambda x: x["completed"]
            }

        return sorted(tasks, key=sort_keys[choice], reverse=reverse)

    def validate_assign_option(self, option):
        """
        Validates the assign option for the assign_tasks() function.

        Parameters:
        option (str): a number from 1 to 4

        Returns:
        str: validated option

        Raises:
        ValueError - if option isn't a number from 1 to 4.
        """
        if option not in ["1", "2", "3", "4"]:
            raise ValueError("Invalid choice")
        return option
    
    def assign_tasks(self, tasks, index, option):
        """
        Assigns tasks for today or this week.
        
        Parameters:
        tasks: tasks.json file
        index (int): task index
        option (str): assign option
        """

        task = tasks[index - 1]
    
        if option == "1":
            task["today"] = True
        elif option == "2":
            task["this_week"] = True
        elif option == "3":
            task["today"] = False
        elif option == "4":
            task["this_week"] = False

    def delete_task(self, tasks, index):
        """
        Deletes a task from tasks.json

        Parameters:
        tasks: tasks.json file
        index (int): task index
        
        """
        index = self.validate_index(index, tasks)
        
        tasks.pop(index - 1)
        

    def search_task(self, tasks, index):
        """
        Search a task in tasks.json

        Parameters:
        tasks: tasks.json file
        index (int): task index
        
        """
        index = self.validate_index(index, tasks)
        
        try:
            return tasks[index - 1] 
        except TypeError as e:
            raise TypeError(e)
 

    def mark_as_completed(self, tasks, index):
        """
        Mark a task as completed.

        Parameters:
        tasks: tasks.json file
        index (int): task index
        
        """
        index = self.validate_index(index, tasks)
        
        tasks[index - 1]["completed"] = True


    def mark_as_incomplete(self, tasks, index):
        """
        Mark a task as incomplete.

        Parameters:
        tasks: tasks.json file
        index (int): task index
        
        """
        index = self.validate_index(index, tasks)
        
        tasks[index - 1]["completed"] = False

    def update_task(self, tasks, index, title, due_date, description):
        """
        Update an existing task.

        Parameters:
        tasks: tasks.json file
        index (int): task index
        title (str): task title
        description (str): task description
        due_date (str): task due date in YYYY-MM-DD format

        """    
        task = tasks[index - 1]
        task["title"] = title
        task["due_date"] = due_date
        task["description"] = description



