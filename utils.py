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

def list_projects(filtr=''):
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    projects = []
    if filtr == '':
        cursor.execute('''
            SELECT projects.name, projects.deadline
            FROM projects''')
    elif filtr == 'today':
        cursor.execute(
            '''
            SELECT projects.name, projects.deadline
            FROM projects
            WHERE DATE(projects.deadline) = DATE('now')
            '''
        )
    elif filtr == 'priority':
        cursor.execute(
            '''
            SELECT projects.name, projects.deadline
            FROM projects
            ORDER BY projects.deadline ASC
            '''
        )
    for row in cursor.fetchall():
        project_name, deadline = row
        #print(project_name, deadline)
        projects.append((project_name, deadline))
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
    #add_project('wqeq', '2025-03-32 23:59')
    #add_project('qweqw', '2025-03-38 23:59')
    #list_projects()
    #list_tasks(0)
    #purge()
    pass