import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font
from datetime import datetime
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False

# Initialize tasks list
tasks = []
TASKS_FILE = "tasks.json"

# Color scheme
BG_COLOR = "#e6f3fa"  # Light cyan background
BUTTON_COLOR = "#0288d1"  # Vibrant blue for buttons
BUTTON_HOVER = "#01579b"  # Darker blue for hover
HIGH_PRIORITY = "#e57373"  # Soft red for high priority
MEDIUM_PRIORITY = "#ffb300"  # Amber for medium priority
LOW_PRIORITY = "#81c784"  # Soft green for low priority
TABLE_HEADER_COLOR = "#4fc3f7"  # Light blue for table headers
FOOTER_COLOR = "#b0bec5"  # Gray for footer

# Load tasks from JSON file
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
                # Ensure all tasks have required keys
                for task in tasks:
                    if "date" not in task:
                        task["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if "deadline" not in task:
                        task["deadline"] = "Not set"
                    if "priority" not in task:
                        task["priority"] = "Medium"
                    if "name" not in task:
                        task["name"] = "Untitled"
                    if "description" not in task:
                        task["description"] = ""
                    if "id" not in task:
                        task["id"] = len(tasks) + 1
        except json.JSONDecodeError:
            tasks = []
            messagebox.showerror("Error", "Failed to load tasks. Starting with an empty list.")
    else:
        tasks = []

# Save tasks to JSON file
def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save tasks: {e}")

# Add a new task
def add_task(event=None):
    name = entry_name.get().strip()
    description = description_text.get("1.0", tk.END).strip()
    priority = combo_priority.get()
    date = entry_date.get().strip()
    deadline = entry_deadline.get_date().strftime("%Y-%m-%d") if TKCALENDAR_AVAILABLE else entry_deadline.get().strip()
    
    if not name:
        messagebox.showwarning("Input Error", "Task name cannot be empty.")
        return
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not deadline or deadline == "Not set":
        deadline = "Not set"
    
    task_id = len(tasks) + 1
    tasks.append({
        "id": task_id,
        "name": name,
        "description": description,
        "priority": priority,
        "date": date,
        "deadline": deadline
    })
    save_tasks()
    entry_name.delete(0, tk.END)
    description_text.delete("1.0", tk.END)
    combo_priority.set("Medium")
    entry_date.delete(0, tk.END)
    if TKCALENDAR_AVAILABLE:
        entry_deadline.set_date(datetime.now())
    else:
        entry_deadline.delete(0, tk.END)
    update_task_table()
    messagebox.showinfo("Success", f"Task '{name[:20]}...' added!")

# Edit a selected task
def edit_task():
    try:
        selected = tree.selection()[0]
        index = tree.index(selected)
        task = tasks[index]
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Task")
        edit_window.geometry("350x350")
        edit_window.configure(bg=BG_COLOR)

        tk.Label(edit_window, text="Edit Task Name:", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        entry_new_name = tk.Entry(edit_window, width=30, font=("Arial", 10))
        entry_new_name.insert(0, task["name"])
        entry_new_name.pack(pady=5)

        tk.Label(edit_window, text="Edit Description (optional):", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        entry_new_desc = tk.Text(edit_window, width=30, height=3, font=("Arial", 10))
        entry_new_desc.insert("1.0", task["description"])
        entry_new_desc.pack(pady=5)

        tk.Label(edit_window, text="Edit Priority:", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        combo_new_priority = ttk.Combobox(edit_window, values=["High", "Medium", "Low"], state="readonly", font=("Arial", 10))
        combo_new_priority.set(task["priority"])
        combo_new_priority.pack(pady=5)

        tk.Label(edit_window, text="Edit Deadline:", bg=BG_COLOR, font=("Arial", 10)).pack(pady=5)
        if TKCALENDAR_AVAILABLE:
            entry_new_deadline = DateEntry(edit_window, width=27, font=("Arial", 10), date_pattern="yyyy-mm-dd")
            if task["deadline"] != "Not set":
                try:
                    entry_new_deadline.set_date(datetime.strptime(task["deadline"], "%Y-%m-%d"))
                except ValueError:
                    entry_new_deadline.set_date(datetime.now())
            entry_new_deadline.pack(pady=5)
        else:
            entry_new_deadline = tk.Entry(edit_window, width=30, font=("Arial", 10))
            entry_new_deadline.insert(0, task["deadline"])
            entry_new_deadline.pack(pady=5)

        def save_edit():
            new_name = entry_new_name.get().strip()
            new_desc = entry_new_desc.get("1.0", tk.END).strip()
            if not new_name:
                messagebox.showwarning("Input Error", "Task name cannot be empty.")
                return
            tasks[index]["name"] = new_name
            tasks[index]["description"] = new_desc
            tasks[index]["priority"] = combo_new_priority.get()
            tasks[index]["deadline"] = entry_new_deadline.get_date().strftime("%Y-%m-%d") if TKCALENDAR_AVAILABLE else entry_new_deadline.get().strip() or "Not set"
            save_tasks()
            update_task_table()
            messagebox.showinfo("Success", f"Task ID {task['id']} updated!")
            edit_window.destroy()

        tk.Button(edit_window, text="Save Changes", command=save_edit, bg=BUTTON_COLOR, fg="white", font=("Arial", 10)).pack(pady=10)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Delete a selected task
def delete_task():
    try:
        selected = tree.selection()[0]
        index = tree.index(selected)
        task_id = tasks[index]["id"]
        tasks.pop(index)
        for i, t in enumerate(tasks, 1):
            t["id"] = i
        save_tasks()
        update_task_table()
        messagebox.showinfo("Success", f"Task ID {task_id} deleted!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Clear all tasks
def clear_all_tasks():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        global tasks
        tasks = []
        save_tasks()
        update_task_table()
        messagebox.showinfo("Success", "All tasks cleared!")

# Export to Excel
def export_to_excel():
    if not PANDAS_AVAILABLE:
        messagebox.showerror("Error", "Pandas is not installed. Install it with 'pip install pandas openpyxl'.")
        return
    if not tasks:
        messagebox.showwarning("Warning", "No tasks to export.")
        return
    df = pd.DataFrame(tasks)
    try:
        df.to_excel("tasks.xlsx", index=False)
        messagebox.showinfo("Success", "Tasks exported to tasks.xlsx")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export to Excel: {e}")

# Sort tasks
def sort_tasks(key, reverse=False):
    if key == "date":
        tasks.sort(key=lambda x: x["date"], reverse=reverse)
    elif key == "name":
        tasks.sort(key=lambda x: x["name"].lower(), reverse=reverse)
    save_tasks()
    update_task_table()

# Update task table
def update_task_table():
    for item in tree.get_children():
        tree.delete(item)
    for task in tasks:
        date = task.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deadline = task.get("deadline", "Not set")
        priority = task.get("priority", "Medium")
        name = task.get("name", "Untitled")
        description = task.get("description", "")
        task_id = task.get("id", len(tasks) + 1)
        tree.insert("", tk.END, values=(task_id, name, description, priority, date, deadline),
                    tags=(priority,))
    tree.tag_configure("High", foreground=HIGH_PRIORITY)
    tree.tag_configure("Medium", foreground=MEDIUM_PRIORITY)
    tree.tag_configure("Low", foreground=LOW_PRIORITY)

# Drag and drop functionality
def on_drag_start(event):
    tree.drag_start_index = tree.index(tree.identify_row(event.y))

def on_drag_motion(event):
    tree.drag_to_index = tree.index(tree.identify_row(event.y))
    if tree.drag_to_index != tree.drag_start_index:
        tree.selection_set(tree.identify_row(event.y))

def on_drop(event):
    try:
        start_index = tree.drag_start_index
        end_index = tree.index(tree.identify_row(event.y))
        if start_index != end_index:
            task = tasks.pop(start_index)
            tasks.insert(end_index, task)
            for i, t in enumerate(tasks, 1):
                t["id"] = i
            save_tasks()
            update_task_table()
    except IndexError:
        pass

# Button hover effects
def on_enter(event, button):
    button.config(bg=BUTTON_HOVER)

def on_leave(event, button):
    button.config(bg=BUTTON_COLOR)

# GUI setup
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("800x700")
root.configure(bg=BG_COLOR)

# Custom fonts
title_font = font.Font(family="Arial", size=18, weight="bold")
label_font = font.Font(family="Arial", size=10)

# Title
tk.Label(root, text="To-Do List Manager", bg=BG_COLOR, font=title_font).pack(pady=10)

# Input frame
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

# Task name input
tk.Label(input_frame, text="Task Name:", bg=BG_COLOR, font=label_font).pack(anchor="w")
entry_name = tk.Entry(input_frame, width=50, font=("Arial", 10))
entry_name.pack(pady=5)
entry_name.bind("<Return>", lambda e: add_task() if not e.state & 0x0001 else None)

# Description input (optional, multi-line)
tk.Label(input_frame, text="Task Description (optional):", bg=BG_COLOR, font=label_font).pack(anchor="w")
description_text = tk.Text(input_frame, width=50, height=3, font=("Arial", 10))
description_text.pack(pady=5)

# Priority input
tk.Label(input_frame, text="Priority:", bg=BG_COLOR, font=label_font).pack(anchor="w")
combo_priority = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], state="readonly", font=("Arial", 10))
combo_priority.set("Medium")
combo_priority.pack(pady=5)

# Date input
tk.Label(input_frame, text="Date Added (YYYY-MM-DD HH:MM:SS, optional):", bg=BG_COLOR, font=label_font).pack(anchor="w")
entry_date = tk.Entry(input_frame, width=50, font=("Arial", 10))
entry_date.pack(pady=5)

# Deadline input (calendar)
tk.Label(input_frame, text="Deadline (select date):", bg=BG_COLOR, font=label_font).pack(anchor="w")
if TKCALENDAR_AVAILABLE:
    entry_deadline = DateEntry(input_frame, width=47, font=("Arial", 10), date_pattern="yyyy-mm-dd")
    entry_deadline.pack(pady=5)
else:
    entry_deadline = tk.Entry(input_frame, width=50, font=("Arial", 10))
    entry_deadline.insert(0, "YYYY-MM-DD")
    entry_deadline.pack(pady=5)
    messagebox.showwarning("Warning", "tkcalendar not installed. Using text input for deadline. Install with 'pip install tkcalendar'.")

# Button frame
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

# Add task button
btn_add = tk.Button(button_frame, text="Add Task", command=add_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_add.pack(side=tk.LEFT, padx=5)
btn_add.bind("<Enter>", lambda e: on_enter(e, btn_add))
btn_add.bind("<Leave>", lambda e: on_leave(e, btn_add))

# Edit task button
btn_edit = tk.Button(button_frame, text="Edit Task", command=edit_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_edit.pack(side=tk.LEFT, padx=5)
btn_edit.bind("<Enter>", lambda e: on_enter(e, btn_edit))
btn_edit.bind("<Leave>", lambda e: on_leave(e, btn_edit))

# Delete task button
btn_delete = tk.Button(button_frame, text="Delete Task", command=delete_task, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_delete.pack(side=tk.LEFT, padx=5)
btn_delete.bind("<Enter>", lambda e: on_enter(e, btn_delete))
btn_delete.bind("<Leave>", lambda e: on_leave(e, btn_delete))

# Export to Excel button
btn_export = tk.Button(button_frame, text="Export to Excel", command=export_to_excel, bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_export.pack(side=tk.LEFT, padx=5)
btn_export.bind("<Enter>", lambda e: on_enter(e, btn_export))
btn_export.bind("<Leave>", lambda e: on_leave(e, btn_export))

# Sort frame
sort_frame = tk.Frame(root, bg=BG_COLOR)
sort_frame.pack(pady=5)

# Sort buttons
btn_sort_latest = tk.Button(sort_frame, text="Sort by Latest", command=lambda: sort_tasks("date", reverse=True), bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_sort_latest.pack(side=tk.LEFT, padx=5)
btn_sort_latest.bind("<Enter>", lambda e: on_enter(e, btn_sort_latest))
btn_sort_latest.bind("<Leave>", lambda e: on_leave(e, btn_sort_latest))

btn_sort_oldest = tk.Button(sort_frame, text="Sort by Oldest", command=lambda: sort_tasks("date", reverse=False), bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_sort_oldest.pack(side=tk.LEFT, padx=5)
btn_sort_oldest.bind("<Enter>", lambda e: on_enter(e, btn_sort_oldest))
btn_sort_oldest.bind("<Leave>", lambda e: on_leave(e, btn_sort_oldest))

btn_sort_asc = tk.Button(sort_frame, text="Sort A-Z", command=lambda: sort_tasks("name", reverse=False), bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_sort_asc.pack(side=tk.LEFT, padx=5)
btn_sort_asc.bind("<Enter>", lambda e: on_enter(e, btn_sort_asc))
btn_sort_asc.bind("<Leave>", lambda e: on_leave(e, btn_sort_asc))

btn_sort_desc = tk.Button(sort_frame, text="Sort Z-A", command=lambda: sort_tasks("name", reverse=True), bg=BUTTON_COLOR, fg="white", font=("Arial", 10), width=12)
btn_sort_desc.pack(side=tk.LEFT, padx=5)
btn_sort_desc.bind("<Enter>", lambda e: on_enter(e, btn_sort_desc))
btn_sort_desc.bind("<Leave>", lambda e: on_leave(e, btn_sort_desc))

# Task table (Treeview)
table_frame = tk.Frame(root, bg=BG_COLOR)
table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Description", "Priority", "Date", "Deadline"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("ID", text="ID")
tree.heading("Name", text="Task Name")
tree.heading("Description", text="Description")
tree.heading("Priority", text="Priority")
tree.heading("Date", text="Date Added")
tree.heading("Deadline", text="Deadline")
tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Description", width=200)
tree.column("Priority", width=100)
tree.column("Date", width=150)
tree.column("Deadline", width=100)
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

# Style for Treeview
style = ttk.Style()
style.configure("Treeview.Heading", background=TABLE_HEADER_COLOR, font=("Arial", 10, "bold"))
style.configure("Treeview", rowheight=25)

# Drag and drop bindings
tree.bind("<Button-1>", on_drag_start)
tree.bind("<B1-Motion>", on_drag_motion)
tree.bind("<ButtonRelease-1>", on_drop)

# Clear all tasks button
btn_clear = tk.Button(root, text="Clear All Tasks", command=clear_all_tasks, bg="#e74c3c", fg="white", font=("Arial", 10))
btn_clear.pack(pady=10)
btn_clear.bind("<Enter>", lambda e: on_enter(e, btn_clear))
btn_clear.bind("<Leave>", lambda e: on_leave(e, btn_clear))

# Footer
tk.Label(root, text="Developed and designed By Mallarapu Yaswanth", bg=FOOTER_COLOR, fg="black", font=("Arial", 8, "italic")).pack(side=tk.BOTTOM, pady=5)

# Load tasks at startup
load_tasks()
update_task_table()

# Run the application
root.mainloop()