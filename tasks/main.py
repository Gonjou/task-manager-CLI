from tasks.storage import TaskManager
import sys
import re
from tabulate import tabulate

def main():
    manager = TaskManager()
    tasks = manager.load_tasks()

    while True:
        print("\nTask Manager")
        print("1. Add task")
        print("2. List tasks")
        print("3. Search task")
        print("4. Delete task")
        print("5. Mark as completed")
        print("6. Update task")
        print("7. Exit")

        try:
            choice = input("Enter your choice: ")
            
            if choice == "1":
                title = input("Enter title: ")
                description = input("Enter description: ")
                due_date = _validate_due_date(input("Enter due date: "))

                manager.add_task(tasks, title, description, due_date)
            elif choice == "2":
                table = manager.list_tasks(tasks)
                print(f"\nTASKS\n")
                print(tabulate(table, headers=["title", "due_date", "completion"], tablefmt="github"))
            elif choice == "3":
                index = int(input("Insert index: "))
                print(manager.search_task(tasks, index))
            elif choice == "4":
                index = int(input("Insert index of task to delete: "))
                manager.delete_task(tasks, index)
            elif choice == "5":
                index = int(input("Insert index of completed task: "))
                manager.mark_as_completed(tasks, index)
            elif choice == "6":
                index = int(input("Insert index of task to update: "))
                title = input("Enter title: ")
                description = input("Enter description: ")
                due_date = input("Enter due date: ")
                manager.update_task(tasks, title, due_date, description)
            elif choice == "7":
                sys.exit("\nProgram closed")

        
            manager.save_tasks(tasks)

        except ValueError as e:
            sys.exit(f"\nError: {e}")


def _validate_due_date(due_date):
    validation = re.search(r"^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$", due_date)

    if not validation:
        raise ValueError("Invalid date format. Use YYYY-MM-DD. Example: 2026-04-12")
    
    return due_date



            










if __name__ == "__main__":
    main()