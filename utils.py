import database
import sqlite3

def add_project(name, deadline):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (name, deadline) VALUES (?, ?)", (name, deadline))
    conn.commit()
    conn.close()
def add_task(project_id, title, description, completed):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (project_id, title, description, completed) VALUES (?, ?, ?, ?)", (project_id, title, description, completed))
    conn.commit()
    conn.close()

def list_projects():
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    projects = []
    cursor.execute('''
        SELECT projects.name, projects.deadline
        FROM projects''')
    for row in cursor.fetchall():
        project_name, deadline = row
        #print(project_name, deadline)
        projects.append(project_name)
    conn.close()
    return projects
def list_tasks(project_id):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    tasks = []
    cursor.execute('''
        SELECT tasks.title, tasks.description, tasks.completed
        FROM tasks
        WHERE tasks.project_id = ?''', (project_id,))
    for row in cursor.fetchall():
        task_title, task_description, task_completed = row
        status = "✔" if task_completed else "❌"
        tasks.append((task_title, task_description, task_completed))
    return tasks

def purge():
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects")
    conn.commit()
    conn.close()
if __name__ == '__main__':
    #dd_project('Fortnite sex', '2025-08-28 23:59')
    #add_project('droguri', '2026-04-01 23:59')
    #list_projects()
    #list_tasks(0)
    #purge()
    pass