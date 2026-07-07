# Task Manager CLI

A CLI program that helps you manage all you tasks.

## Description

Stores your tasks in a json file. You are able to interact with the program's functionalities through the command-line interface.

## Features
- ✏️ Add new tasks with title, description and due date
- 🗃️ Sort tasks with by title, due date or completion
- 🔎 Search for specific tasks
- 🗑️ Delete tasks
- ✅ Mark tasks as completed or incomplete
- 📌 Assign tasks for today or this week
- 🛠️ Update an existing task

## Getting Started

### Prerequisites
- Python 3.10+

### Dependencies
- tabulate
- pytest

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gonjou/task-manager-CLI.git
cd task-manager-CLI
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```


## Usage

### Running the Program
To run the program, use this command:
```bash
python -m task_manager.main
```
You will see a menu like this:
```txt
Task Manager
1. Add task
2. List tasks
3. Sort tasks
4. Search task
5. Delete task
6. Mark as completed
7. Mark as incompleted
8. Assign task for today or this week
9. Update task
10. Exit
11. Display tasks at launch
```
Enter the number of the function you want to execute.

## Running Tests
```bash
python -m pytest
```
## Example of Use
```bash
python -m task_manager.main
```
```txt
Task Manager
1. Add task
2. List tasks
3. Sort tasks
4. Search task
5. Delete task
6. Mark as completed
7. Mark as incompleted
8. Assign task for today or this week
9. Update task
10. Exit
11. Display tasks at launch
ANSWER ONLY WITH NUMBERS (e.g: 1, 2, 10...)
Enter your choice: 1
```
```txt
Enter title: Do homework
Enter description: Math and Science
Enter due date: 2026-07-07

TASK Do homework ADDED
```

## License

This project is licensed under the MIT License. Feel free to use it.



