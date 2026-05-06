from tasks.storage import TaskManager
import sys

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

        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter title: ")
            description = input("Enter description: ")
            due_date = input("Enter due date: ") # Add due_date validation

            manager.add_task(tasks, title, description, due_date)
        if choice == "2":
            print(manager.list_tasks(tasks))
        if choice == "3":
            index = int(input("Insert index: "))
            manager.search_task(tasks, index)

        
        
        
        manager.save_tasks(tasks)


def _validate_due_date():
    ...


            










if __name__ == "__main__":
    main()