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
        print("3. Sort tasks")
        print("4. Search task")
        print("5. Delete task")
        print("6. Mark as completed")
        print("7. Mark as incompleted")
        print("8. Update task")
        print("9. Exit")

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
                print(tabulate(table, headers=["index", "title", "due_date", "completion"], tablefmt="github"))

            elif choice == "3":
                print("SORTING OPTIONS")
                print("1. By due date (earliest first)")
                print("2. By due date (latest first)")
                print("3. By title (A-Z)")
                print("4. By completion (Incomplete first)")
                print("5. Back to main menu")

                choice = input("Choose sorting method: ")

                if choice == "1":
                    sorted_tasks = manager.sort_tasks(tasks, "due date")
                elif choice == "2":
                    sorted_tasks = manager.sort_tasks(tasks, "due date", reverse=True)
                elif choice == "3":
                    sorted_tasks = manager.sort_tasks(tasks, "title")
                elif choice == "4":
                    sorted_tasks = manager.sort_tasks(tasks, "completion")

                print(tabulate(sorted_tasks, headers="keys", tablefmt="github"))

            elif choice == "4":
                index = input("Insert index: ")
                task = manager.search_task(tasks, index)
                print(f"\nTitle: {task['title']}")
                print(f"Description: {task['description']}")
                print(f"Date: {task['due_date']}")
                print(f"Completed: {task['completed']}\n")

            elif choice == "5":
                index = input("Insert index of task to delete: ")
                manager.delete_task(tasks, index)
                print(f"TASK {index} DELETED")

            elif choice == "6":
                index = input("Insert index of completed task: ")
                manager.mark_as_completed(tasks, index)
                print(f"TASK {index} COMPLETED")

            elif choice == "7":
                index = input("Insert index of incompleted task: ")
                manager.mark_as_incomplete(tasks, index)
                print(f"TASK {index} INCOMPLETE")

            elif choice == "8":
                index = input("Insert index of task to update: ")
                title = input("Enter title: ")
                description = input("Enter description: ")
                due_date = _validate_due_date(input("Enter due date: "))
                manager.update_task(tasks, index, title, due_date, description)
                print(f"TASK {index} UPDATED")

            elif choice == "9":
                sys.exit("\nPROGRAM CLOSED")

            manager.save_tasks(tasks)

        except ValueError as e:
            print(f"\nError: {e}")
        except IndexError as e:
            print(f"\nError: {e}")
        except TypeError as e:
            print(f"\nError: {e}")
        except EOFError:
            sys.exit("PROGRAM CLOSED")


def _validate_due_date(due_date):
    validation = re.search(r"^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$", due_date)

    if not validation:
        raise ValueError("Invalid date format. Use YYYY-MM-DD. Example: 2026-04-12")
    
    return due_date



            










if __name__ == "__main__":
    main()