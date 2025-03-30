import datetime
import database
import sqlite3

db_querys = {
    'add_project': "INSERT INTO projects (name, deadline) VALUES (?, ?)",
    'add_task': "INSERT INTO tasks (project_id, title, description, completed) VALUES (?, ?, ?, ?)",
    'list_projects': '''
        SELECT projects.name, projects.deadline
        FROM projects
    ''',
    'list_projects_today': '''
        SELECT projects.name, projects.deadline
        FROM projects
        WHERE DATE(projects.deadline) = DATE('now')
    ''',
    'list_projects_priority': '''
        SELECT projects.name, projects.deadline
        FROM projects
        ORDER BY projects.deadline ASC
    ''',
    'list_tasks': '''
        SELECT tasks.title, tasks.description, tasks.completed
        FROM tasks
        WHERE tasks.project_id = ?
    ''',
    'purge_projects': "DELETE FROM projects",
    'delete_project': "DELETE FROM projects WHERE name = ?"
}

def add_project(name, deadline):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute(db_querys['add_project'], (name, deadline))
    conn.commit()
    conn.close()
def delete_project(name):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute(db_querys['delete_project'], (str(name).strip(),))
    conn.commit()
    conn.close()
def add_task(project_id, title, description, completed):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute(db_querys['add_task'], (project_id, title, description, completed))
    conn.commit()
    conn.close()

def list_projects(filtr=''):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    projects = []
    if filtr == '':
        cursor.execute(db_querys['list_projects'])
    elif filtr == 'today':
        cursor.execute(db_querys['list_projects_today'])
    elif filtr == 'priority':
        cursor.execute(db_querys['list_projects_priority'])
    for row in cursor.fetchall():
        project_name, deadline = row
        projects.append((project_name, deadline))
    conn.close()
    return projects

def list_tasks(project_id):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    tasks = []
    cursor.execute(db_querys['list_tasks'], (project_id,))
    for row in cursor.fetchall():
        task_title, task_description, task_completed = row
        tasks.append((task_title, task_description, task_completed))
    conn.close()
    return tasks

def is_valid_deadline(deadline):
    try:
        # Try to parse the deadline with the expected format
        datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        # If parsing fails, the format is incorrect
        return False

def purge():
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute(db_querys['purge_projects'])
    conn.commit()
    conn.close()

if __name__ == '__main__':
    pass