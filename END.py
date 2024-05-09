import tkinter as tk
from tkinter import ttk  # for better widgets
import sqlite3

# Define database functions
def connect_db():
  conn = sqlite3.connect('tasks.db')
  return conn

def create_table(conn):
  cursor = conn.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
      task text,
      completed integer
  )""")
  conn.commit()

def add_task(conn, task):
  cursor = conn.cursor()
  cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
  conn.commit()

def get_tasks(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM tasks")
  tasks = cursor.fetchall()
  return tasks

def update_task(conn, task_id, completed):
  cursor = conn.cursor()
  cursor.execute("UPDATE tasks SET completed = ? WHERE rowid = ?", (completed, task_id))
  conn.commit()

def delete_task(conn, task_id):
  cursor = conn.cursor()
  cursor.execute("DELETE FROM tasks WHERE rowid = ?", (task_id,))
  conn.commit()

# Create the main window
window = tk.Tk()
window.title("Task Manager")

# Create database connection
conn = connect_db()
create_table(conn)

# Create task entry and button
task_entry = ttk.Entry(window, width=50)
task_entry.pack(pady=10)

add_button = ttk.Button(window, text="Add Task", command=lambda: add_task(conn, task_entry.get()))
add_button.pack()

# Create listbox for tasks
task_list = tk.Listbox(window, width=50)
task_list.pack()


def update_task_list():
  tasks = get_tasks(conn)
  task_list.delete(0, tk.END)
  for task, completed in tasks:
    task_list.insert(tk.END, f"{task} {'(Completed)' if completed else ''}")

update_task_list()

# Function to handle task selection and completion
def handle_task_select(event):
  selected_index = task_list.curselection()[0]
  task_id, _ = conn.execute("SELECT rowid, completed FROM tasks WHERE rowid = ?", (selected_index + 1,)).fetchone()
  completed = not bool(completed)  # Toggle completion status
  update_task(conn, task_id, completed)
  update_task_list()

# Bind listbox selection event
task_list.bind('<<ListboxSelect>>', handle_task_select)

# Function to handle task deletion
def delete_task_selected():
  selected_index = task_list.curselection()[0]
  task_id, _ = conn.execute("SELECT rowid FROM tasks WHERE rowid = ?", (selected_index + 1,)).fetchone()
  delete_task(conn, task_id)
  update_task_list()

# Delete button
delete_button = ttk.Button(window, text="Delete Task", command=delete_task_selected)
delete_button.pack(pady=10)

window.mainloop()

# Close database connection on exit
conn.close()
