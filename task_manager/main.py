from task_manager.storage import TaskManager
import sys
from tabulate import tabulate

def main():
    """The main() function calls all of the storage.py functions and prints the output."""
    manager = TaskManager()
    tasks = manager.load_tasks()
    settings = manager.load_settings()

    while True:
        print("\nTask Manager")
        print("1. Add task")
        print("2. List tasks")
        print("3. Sort tasks")
        print("4. Search task")
        print("5. Delete task")
        print("6. Mark as completed")
        print("7. Mark as incompleted")
        print("8. Assign task for today or this week")
        print("9. Update task")
        print("10. Exit")
        print("11. Display tasks at launch")
        print("ANSWER ONLY WITH NUMBERS (e.g: 1, 2, 10...)")

        table = manager.list_tasks(tasks)

        if settings.get("display_tasks_at_launch"):
            print(f"\n----TASKS----\n")
            print(tabulate(table, headers=["index", "title", "due_date", "completion"], tablefmt="github"))
            print("\n")


        try:
            choice = input("Enter your choice: ")
            
            if choice == "1":
                title = get_valid_input("Enter title: ", manager.validate_title)
                description = input("Enter description: ")
                due_date = get_valid_input("Enter due date: ", manager.validate_due_date)

                manager.add_task(tasks, title, description, due_date)
                print(f"\nTASK {title} ADDED")

            elif choice == "2":
                table = manager.list_tasks(tasks)
                print(f"\n----TASKS----\n")
                print(tabulate(table, headers=["index", "title", "due_date", "completion"], tablefmt="github"))

            elif choice == "3":
                print("SORTING OPTIONS")
                print("1. By due date (earliest first)")
                print("2. By due date (latest first)")
                print("3. By title (A-Z)")
                print("4. By completion (Incomplete first)")
                print("5. Back to main menu")

                choice = get_valid_input("Choose sorting method: ", manager.validate_sort_option)

                if choice == "1":
                    sorted_tasks = manager.sort_tasks(tasks, "due date")
                elif choice == "2":
                    sorted_tasks = manager.sort_tasks(tasks, "due date", reverse=True)
                elif choice == "3":
                    sorted_tasks = manager.sort_tasks(tasks, "title")
                elif choice == "4":
                    sorted_tasks = manager.sort_tasks(tasks, "completion")
                elif choice == "5":
                    sorted_tasks = None
                    print("Going back to main menu...")

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
                print(f"\nTASK {index} DELETED")

            elif choice == "6":
                index = input("Insert index of completed task: ")
                manager.mark_as_completed(tasks, index)
                print(f"\nTASK {index} COMPLETED")

            elif choice == "7":
                index = input("Insert index of incompleted task: ")
                manager.mark_as_incomplete(tasks, index)
                print(f"\nTASK {index} INCOMPLETE")

            elif choice == "8":
                today = [dict_task for dict_task in tasks if dict_task.get("today") is True]
                week = [dict_task for dict_task in tasks if dict_task.get("this_week") is True]

                print("----TODAY----".center(80))
                print(tabulate(today, headers="keys", tablefmt="github"))
                print("\n")
                print("----THIS WEEK----".center(80))
                print(tabulate(week, headers="keys", tablefmt="github"))
                print("\n")

                print("1. Assign for today")
                print("2. Assign for this week")
                print("3. Unassign for today")
                print("4. Unassign for this week")

                assign_option = get_valid_input("Choose an option: ", manager.validate_assign_option)
                assign_task_index = get_valid_input("Enter task index: ", lambda index: manager.validate_index(index, tasks))
                
                manager.assign_tasks(tasks, assign_task_index, assign_option)

                assign_task = manager.search_task(tasks, assign_task_index)

                print(f"\n{assign_task['title']} {'assigned' if assign_option in ['1', '2'] else 'unassigned'} for {'today' if assign_option in ['1', '3'] else 'this week'}")


            elif choice == "9":
                index = get_valid_input("Insert index of task to update: ", lambda index: manager.validate_index(index, tasks))
                title = get_valid_input("Enter title: ", manager.validate_title)
                description = input("Enter description: ")
                due_date = get_valid_input("Enter due date: ", manager.validate_due_date)
                manager.update_task(tasks, index, title, due_date, description)
                print(f"TASK {index} UPDATED")

            elif choice == "10":
                sys.exit("\nPROGRAM CLOSED")

            elif choice == "11":
                user_choice = input("Display tasks at launch? [yes/no]: ").strip().lower()

                if user_choice == "yes":
                    settings["display_tasks_at_launch"] = True
                if user_choice == "no":
                    settings["display_tasks_at_launch"] = False
                if user_choice not in ["yes", "no"]:
                    raise ValueError("Invalid choice. Type [yes/no]")

            
            manager.save_tasks(tasks)
            manager.save_settings(settings)

        except ValueError as e:
            print(f"\nError: {e}")
        except IndexError as e:
            print(f"\nError: {e}")
        except TypeError as e:
            print(f"\nError: {e}")
        except EOFError:
            sys.exit("PROGRAM CLOSED")

def get_valid_input(prompt, validator):
    """
    Gets the user input and validates it.
    
    Args:
    prompt (str): string that contains the user input. Example: "Enter title: Do homework"
    validator: function that validates the user input. Example: manager.validate_title

    Returns:
    str, int: validated input
    """
    while True:
        try:
            value = input(prompt)
            return validator(value)
        except ValueError as e:
            print(f"\nError: {e}")






if __name__ == "__main__":
    main()