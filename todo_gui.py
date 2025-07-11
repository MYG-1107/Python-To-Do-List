import json
import os
import tkinter as tk
from tkinter import messagebox

# Initialize tasks list
tasks = []
TASKS_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []

# Save tasks to JSON file
def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save tasks: {e}")

# Add a new task
def add_task():
    description = entry_description.get()
    priority = entry_priority.get() or "Medium"
    if not description:
        messagebox.showwarning("Input Error", "Description cannot be empty.")
        return
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "priority": priority})
    save_tasks()
    entry_description.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    update_task_list()
    messagebox.showinfo("Success", f"Task '{description}' added!")

# Update task list display
def update_task_list():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, f"ID: {task['id']} | {task['description']} | Priority: {task['priority']}")

# Delete a selected task
def delete_task():
    try:
        selected = listbox_tasks.curselection()[0]
        task_id = tasks[selected]['id']
        tasks.pop(selected)
        for i, t in enumerate(tasks, 1):
            t['id'] = i
        save_tasks()
        update_task_list()
        messagebox.showinfo("Success", f"Task ID {task_id} deleted!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# GUI setup
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("400x400")

# Load tasks at startup
load_tasks()

# Description input
tk.Label(root, text="Task Description:").pack(pady=5)
entry_description = tk.Entry(root, width=40)
entry_description.pack(pady=5)

# Priority input
tk.Label(root, text="Priority (High/Medium/Low):").pack(pady=5)
entry_priority = tk.Entry(root, width=40)
entry_priority.pack(pady=5)

# Add task button
tk.Button(root, text="Add Task", command=add_task).pack(pady=10)

# Task list display
listbox_tasks = tk.Listbox(root, width=50, height=10)
listbox_tasks.pack(pady=10)
update_task_list()

# Delete task button
tk.Button(root, text="Delete Selected Task", command=delete_task).pack(pady=10)

# Run the application
root.mainloop()