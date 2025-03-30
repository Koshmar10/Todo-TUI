import sqlite3

DB_FILE = 'tasks.db'


def setup_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                deadline TEXT CHECK (deadline LIKE '____-__-__ __:__' OR deadline IS NULL)
                   )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE   
                   )''')
    connection.commit()
    connection.close()
if __name__ == '__main__':
    setup_database()
    print("Setup Done")