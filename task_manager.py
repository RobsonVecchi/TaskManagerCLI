import sqlite3

def display_menu():
    """Display the menu options."""
    print("\nTask Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Remove Task")
    print("5. View Database Contents")
    print("6. Exit")

def initialize_db():
    """Create the database and tasks table if they don't exist."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    
    conn.commit()
    conn.close()

def add_task():
    """Add a new task to the database."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    description = input("Enter task description: ")
    
    cursor.execute('''
        INSERT INTO tasks (description, completed)
        VALUES (?, ?)
    ''', (description, False))
    
    conn.commit()
    conn.close()
    
    print(f"Task '{description}' added.")

def view_tasks():
    """Display all tasks from the database with options to filter or sort."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    print("1. View all tasks")
    print("2. View completed tasks")
    print("3. View incomplete tasks")
    choice = input("Choose an option: ")
    
    if choice == '1':
        query = 'SELECT id, description, completed FROM tasks'
    elif choice == '2':
        query = 'SELECT id, description, completed FROM tasks WHERE completed = 1'
    elif choice == '3':
        query = 'SELECT id, description, completed FROM tasks WHERE completed = 0'
    else:
        print("Invalid choice. Showing all tasks.")
        query = 'SELECT id, description, completed FROM tasks'
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if not rows:
        print("No tasks available.")
    else:
        for row in rows:
            status = "Completed" if row[2] else "Not Completed"
            print(f"ID: {row[0]}, Description: {row[1]}, Status: {status}")
    
    conn.close()

def mark_task_completed():
    """Mark a task as completed in the database."""
    task_id = int(input("Enter task ID to mark as completed: "))
    
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
    
    if cursor.rowcount > 0:
        print(f"Task ID {task_id} marked as completed.")
    else:
        print("Task not found.")
    
    conn.commit()
    conn.close()

def remove_task():
    """Remove a task from the database."""
    task_id = int(input("Enter task ID to remove: "))
    
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    if cursor.rowcount > 0:
        print(f"Task ID {task_id} removed.")
    else:
        print("Task not found.")
    
    conn.commit()
    conn.close()

def view_database_contents():
    """View all tasks stored in the database with additional metadata."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    print("Viewing database contents:")
    
    # Show table structure
    cursor.execute('PRAGMA table_info(tasks)')
    columns = cursor.fetchall()
    print("Table Structure:")
    for column in columns:
        print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default: {column[4]}, Primary Key: {column[5]}")
    
    print()
    
    # Show task data
    cursor.execute('SELECT id, description, completed FROM tasks')
    rows = cursor.fetchall()
    
    if not rows:
        print("No tasks found in the database.")
    else:
        for row in rows:
            status = "Completed" if row[2] else "Not Completed"
            print(f"ID: {row[0]}, Description: {row[1]}, Status: {status}")
    
    conn.close()

def handle_input():
    """Handle user input and call appropriate functions."""
    initialize_db()  # Ensure the database and table are set up
    
    while True:
        display_menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_completed()
        elif choice == '4':
            remove_task()
        elif choice == '5':
            view_database_contents()
        elif choice == '6':
            print("Exiting the Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    handle_input()