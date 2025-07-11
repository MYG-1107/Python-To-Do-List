import json
import os

# Initialize an empty list to store tasks
tasks = []

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from JSON file if it exists
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
        except json.JSONDecodeError:
            print("Error loading tasks. Starting with an empty list.")
            tasks = []

# Save tasks to JSON file
def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        print(f"Error saving tasks: {e}")

# Add a new task
def add_task(description, priority="Medium"):
    task_id = len(tasks) + 1  # Simple ID based on list length
    task = {"id": task_id, "description": description, "priority": priority}
    tasks.append(task)
    save_tasks()
    print(f"Task '{description}' added successfully!")

# View all tasks
def view_tasks():
    if not tasks:
        print("No tasks found.")
        return
    print("\nYour Tasks:")
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Priority: {task['priority']}")
    print()

# Edit a task
def edit_task(task_id, new_description=None, new_priority=None):
    for task in tasks:
        if task['id'] == task_id:
            if new_description:
                task['description'] = new_description
            if new_priority:
                task['priority'] = new_priority
            save_tasks()
            print(f"Task ID {task_id} updated successfully!")
            return
    print(f"Task ID {task_id} not found.")

# Delete a task
def delete_task(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            # Update IDs to maintain sequential order
            for i, t in enumerate(tasks, 1):
                t['id'] = i
            save_tasks()
            print(f"Task ID {task_id} deleted successfully!")
            return
    print(f"Task ID {task_id} not found.")

# Main menu
def main():
    load_tasks()
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter priority (High/Medium/Low, default Medium): ") or "Medium"
            add_task(description, priority)
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to edit: "))
                new_description = input("Enter new description (press Enter to skip): ")
                new_priority = input("Enter new priority (High/Medium/Low, press Enter to skip): ")
                edit_task(task_id, new_description or None, new_priority or None)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main()