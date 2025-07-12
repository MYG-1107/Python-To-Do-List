import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font

# Initialize tasks list
tasks = []
TASKS_FILE = "tasks.json"

# Color scheme
BG_COLOR = "#f0f4f8"  # Light gray-blue background
BUTTON_COLOR = "#4a90e2"  # Blue for buttons
BUTTON_HOVER = "#357abd"  # Darker blue for hover
HIGH_PRIORITY = "#51cf66"  # Red for high priority
MEDIUM_PRIORITY = "#F58024"  # Yellow for medium priority
LOW_PRIORITY = "#994FB2"  # Green for low priority

# Load tasks from JSON file
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []
            messagebox.showerror("Error", "Failed to load tasks. Starting with an empty list.")

# Save tasks to JSON file
def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save tasks: {e}")

# Add a new task
def add_task(event=None):
    description = entry_description.get().strip()
    priority = combo_priority.get()
    if not description:
        messagebox.showwarning("Input Error", "Task description cannot be empty.")
        return
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "priority": priority})
    save_tasks()
    entry_description.delete(0, tk.END)
    combo_priority.set("Medium")
    update_task_list()
    messagebox.showinfo("Success", f"Task '{description}' added!")

# Edit a selected task
def edit_task():
    try:
        selected = listbox_tasks.curselection()[0]
        task = tasks[selected]
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Task")
        edit_window.geometry("300x200")
        edit_window.configure(bg=BG_COLOR)

        tk.Label(edit_window, text="Edit Description:", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        entry_new_desc = tk.Entry(edit_window, width=30)
        entry_new_desc.insert(0, task["description"])
        entry_new_desc.pack(pady=5)

        tk.Label(edit_window, text="Edit Priority:", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        combo_new_priority = ttk.Combobox(edit_window, values=["High", "Medium", "Low"], state="readonly")
        combo_new_priority.set(task["priority"])
        combo_new_priority.pack(pady=5)

        def save_edit():
            new_desc = entry_new_desc.get().strip()
            if not new_desc:
                messagebox.showwarning("Input Error", "Description cannot be empty.")
                return
            tasks[selected]["description"] = new_desc
            tasks[selected]["priority"] = combo_new_priority.get()
            save_tasks()
            update_task_list()
            messagebox.showinfo("Success", f"Task ID {task['id']} updated!")
            edit_window.destroy()

        tk.Button(edit_window, text="Save Changes", command=save_edit, bg=BUTTON_COLOR, fg="white", font=("Arial", 10)).pack(pady=10)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Delete a selected task
def delete_task():
    try:
        selected = listbox_tasks.curselection()[0]
        task_id = tasks[selected]["id"]
        tasks.pop(selected)
        for i, t in enumerate(tasks, 1):
            t["id"] = i
        save_tasks()
        update_task_list()
        messagebox.showinfo("Success", f"Task ID {task_id} deleted!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Clear all tasks
def clear_all_tasks():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        global tasks
        tasks = []
        save_tasks()
        update_task_list()
        messagebox.showinfo("Success", "All tasks cleared!")

# Update task list display with color-coded priorities
def update_task_list():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        display_text = f"ID: {task['id']} | {task['description']} | Priority: {task['priority']}"
        listbox_tasks.insert(tk.END, display_text)
        # Color-code based on priority
        if task["priority"] == "High":
            listbox_tasks.itemconfig(tk.END, {"fg": HIGH_PRIORITY})
        elif task["priority"] == "Medium":
            listbox_tasks.itemconfig(tk.END, {"fg": MEDIUM_PRIORITY})
        else:
            listbox_tasks.itemconfig(tk.END, {"fg": LOW_PRIORITY})

# Button hover effects
def on_enter(event, button):
    button.config(bg=BUTTON_HOVER)

def on_leave(event, button):
    button.config(bg=BUTTON_COLOR)

# GUI setup
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("500x600")
root.configure(bg=BG_COLOR)

# Custom fonts
title_font = font.Font(family="Arial", size=16, weight="bold")
label_font = font.Font(family="Arial", size=10)

# Title
tk.Label(root, text="To-Do List Application", bg=BG_COLOR, font=title_font).pack(pady=10)

# Frame for input fields
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

# Description input
tk.Label(input_frame, text="Task Description:", bg=BG_COLOR, font=label_font).pack(anchor="w")
entry_description = tk.Entry(input_frame, width=40, font=("Arial", 10))
entry_description.pack(pady=5)
entry_description.bind("<Return>", add_task)  # Add task on Enter key

# Priority input (Combobox)
tk.Label(input_frame, text="Priority:", bg=BG_COLOR, font=label_font).pack(anchor="w")
combo_priority = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], state="readonly", font=("Arial", 10))
combo_priority.set("Medium")
combo_priority.pack(pady=5)

# Frame for buttons
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

# Add task button
btn_add = tk.Button(button_frame, text="Add Task", command=add_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=15)
btn_add.pack(side=tk.LEFT, padx=5)
btn_add.bind("<Enter>", lambda e: on_enter(e, btn_add))
btn_add.bind("<Leave>", lambda e: on_leave(e, btn_add))

# Edit task button
btn_edit = tk.Button(button_frame, text="Edit Task", command=edit_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=15)
btn_edit.pack(side=tk.LEFT, padx=5)
btn_edit.bind("<Enter>", lambda e: on_enter(e, btn_edit))
btn_edit.bind("<Leave>", lambda e: on_leave(e, btn_edit))

# Delete task button
btn_delete = tk.Button(button_frame, text="Delete Task", command=delete_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=15)
btn_delete.pack(side=tk.LEFT, padx=5)
btn_delete.bind("<Enter>", lambda e: on_enter(e, btn_delete))
btn_delete.bind("<Leave>", lambda e: on_leave(e, btn_delete))

# Task list display with scrollbar
listbox_frame = tk.Frame(root, bg=BG_COLOR)
listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tasks = tk.Listbox(listbox_frame, width=60, height=15, font=("Arial", 10), yscrollcommand=scrollbar.set)
listbox_tasks.pack(pady=5, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_tasks.yview)

# Clear all tasks button
btn_clear = tk.Button(root, text="Clear All Tasks", command=clear_all_tasks, bg="#e74c3c", fg="white", font=("Arial", 10))
btn_clear.pack(pady=10)
btn_clear.bind("<Enter>", lambda e: on_enter(e, btn_clear))
btn_clear.bind("<Leave>", lambda e: on_leave(e, btn_clear))

# Load tasks at startup
load_tasks()
update_task_list()

# Run the application
root.mainloop()