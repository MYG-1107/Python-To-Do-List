# To-Do List Application

A simple Python-based To-Do List application that allows users to manage tasks via a command-line interface or a Tkinter GUI. Tasks are stored persistently in a JSON file, making it easy to save and retrieve tasks between sessions. This project is ideal for beginners learning Python, covering concepts like lists, dictionaries, file I/O, and GUI programming.

## Table of Contents
Features
Requirements
Installation
Usage
Command-Line Version
GUI Version
File Structure
How It Works
Enhancements
Contributing

## Features

Add Tasks: Create new tasks with a description and optional priority (High, Medium, Low).

View Tasks: Display all tasks with their IDs, descriptions, and priorities.

Edit Tasks: Update the description or priority of an existing task.

Delete Tasks: Remove tasks by their ID.

Persistent Storage: Tasks are saved to a tasks.json file and loaded on startup.

### Two Interfaces:

Command-line interface for simple, text-based interaction.

Tkinter GUI for a more interactive experience (optional).

Error Handling: Handles invalid inputs and file errors gracefully.

### Requirements

Python 3.6 or higher (tested with Python 3.11+).

Tkinter (included with Python, may need installation on some Linux systems).

No external libraries required for the command-line version (uses standard json and os modules).

Tkinter is required for the GUI version.

### Installation

Follow these steps to set up the project on your local machine:
Clone the Repository:

git clone https://github.com/your-username/todo-list-app.git
cd todo-list-app

Install Python:
Download and install Python from python.org.

Ensure Python is added to your PATH.

Verify installation:
python3 --version

Verify Tkinter (for GUI):

Run python3 -m tkinter in a terminal. A small window should appear.
If missing (Linux):
sudo apt-get install python3-tk  # Ubuntu/Debian
No additional dependencies are needed, as the project uses Python’s standard library.

### Usage

Command-Line Version
Run the command-line application:

python3 todo.py
#### Follow the menu prompts:

1. Add Task: Enter a description and optional priority (High/Medium/Low).

2. View Tasks: See all tasks with their IDs, descriptions, and priorities.

3. Edit Task: Enter the task ID and new description/priority (press Enter to skip unchanged fields).

4. Delete Task: Enter the task ID to remove it.

5. Exit: Close the program.

Tasks are saved automatically to tasks.json in the project folder.

Example:

To-Do List Application
1. Add Task
2. View Tasks
3. Edit Task
4. Delete Task
5. Exit
Enter your choice (1-5): 1
Enter task description: Buy groceries
Enter priority (High/Medium/Low, default Medium): High
Task 'Buy groceries' added successfully!

GUI Version

Run the GUI application:

python3 todo_gui.py

Use the interface:

Enter a task description and optional priority in the text fields.

Click “Add Task” to add the task to the list.

Select a task in the listbox and click “Delete Selected Task” to remove it.

Tasks are displayed in the listbox with their ID, description, and priority.

Tasks are saved to tasks.json and loaded on startup.

