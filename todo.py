import curses
import utils

menuWindow = None
previewWindow = None

def safe_addstr(window, y, x, string, *args):
    max_y, max_x = window.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        try:
            window.addstr(y, x, string, *args)
        except curses.error:
            pass

def display_projects(window, preview_window, focused_project):
    projects = utils.list_projects()
    window.clear()
    safe_addstr(window, 1, 1, "Projects")
    startOffset = 1
    for i, project in enumerate(projects):
        if i == focused_project:
            safe_addstr(window, startOffset + i * 2 + 2, 2, f'📌 {project}', curses.color_pair(1))
            preview_window.clear()
            safe_addstr(preview_window, 1, 1, "Project Tasks")

            tasks = utils.list_tasks(i)
            if len(tasks):
                for j, task in enumerate(tasks):
                    status = "✔" if task[2] else "❌"
                    string = f"{task[0]} {status}"
                    safe_addstr(preview_window, startOffset + j * 2 + 2, 2, string)
            else:
                safe_addstr(preview_window, startOffset + 2, 2, "No tasks added for this project")
        else:
            safe_addstr(window, startOffset + i * 2 + 2, 2, f'📌 {project}', curses.color_pair(2))
    preview_window.border()
    window.border()
    preview_window.refresh()
    window.refresh()

def display_task_info(window, tasks, curr_elem):
    window.clear()
    safe_addstr(window, 1, 1, "Project Tasks")
    for i, task in enumerate(tasks):
        status = "✔" if task[2] else "❌"
        task_string = f"{task[0]} {status}"
        if i == curr_elem:
            safe_addstr(window, 3+i*2, 2, task_string, curses.color_pair(1))
            task_overview = window.derwin(12, window.getmaxyx()[1] // 2, 0, window.getmaxyx()[1] // 2)
            task_overview.clear()
            safe_addstr(task_overview, 2, 1, f"Task: {task[0]}")
            safe_addstr(task_overview, 4, 1, f"Description: \n {task[1]}")
            safe_addstr(task_overview, 7, 1, f"Status: {'✔' if task[2] else '❌'}")
            task_overview.border()
            task_overview.refresh()
        else:
            safe_addstr(window, 3+i*2, 2, task_string, curses.color_pair(2))
    window.border()
    window.refresh()
def handle_selection_change(window, preview_window, curr_elem, key_code, project_id):
    projects = utils.list_projects()

    # Debugging: Log the projects and current element
    '''
    with open("debug.log", "a") as debug_file:
        debug_file.write(f"Projects: {projects}\n")
        debug_file.write(f"Number of Projects: {len(projects)}\n")
        debug_file.write(f"Current Element Before: {curr_elem}\n")
    '''

    if window.getmaxyx() == menuWindow.getmaxyx():
        if key_code == curses.KEY_DOWN:
            curr_elem += 1
        elif key_code == curses.KEY_UP:
            curr_elem -= 1
        if curr_elem < 0:
            curr_elem = 0
        curr_elem %= len(projects)  # Wrap around using the length of projects

        # Debugging: Log the updated current element
        '''
        with open("debug.log", "a") as debug_file:
            debug_file.write(f"Current Element After: {curr_elem}\n")
        '''

        display_projects(window, preview_window, curr_elem)
    if window.getmaxyx() == previewWindow.getmaxyx():
        tasks = utils.list_tasks(project_id)
        if key_code == curses.KEY_DOWN:
            curr_elem += 1
        elif key_code == curses.KEY_UP:
            curr_elem -= 1
        if curr_elem < 0:
            curr_elem = 0
        curr_elem %= len(tasks)

        display_task_info(window, tasks, curr_elem)
    return curr_elem

def handle_cmd(cmd, cmdwindow, menuWindow, previewWindow):
    cmd = cmd.strip()
    max_y, max_x = previewWindow.getmaxyx()
    save = previewWindow.derwin(max_y - 2, max_x, 0, 0)  # Adjust size and position to avoid overlap
    if cmd == 'today':
        save.clear()
        safe_addstr(save, 1, 2, "Due Today")
        save.border()
        save.refresh()
        cmdwindow.refresh()
        while cmdwindow.getch() != ord('b'):
            pass
        save.clear()
        save.refresh()

def main():
    global menuWindow, previewWindow
    app = curses.initscr()
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    app.attron(curses.color_pair(1))

    max_y, max_x = app.getmaxyx()

    menuWindow = curses.newwin(max_y - 1, int(max_x / 3))

    focused_panel = menuWindow
    focused_porject = 0
    focused_task = 0
    previewWindow = curses.newwin(max_y - 1, int(max_x * 2 / 3))

    display_projects(menuWindow, previewWindow, 0)

    menuWindow.border()
    previewWindow.border()

    app.clear()
    app.refresh()

    menuWindow.mvwin(0, 0)
    previewWindow.mvwin(0, max_x // 3 - 1)

    menuWindow.refresh()
    previewWindow.refresh()

    app.refresh()
    while True:
        key = app.getch()
        if key == ord('q'):
            break
        if key == curses.KEY_DOWN or key == curses.KEY_UP:
            focused_element = focused_porject if focused_panel.getmaxyx() == menuWindow.getmaxyx() else focused_task
            focused_element = handle_selection_change(focused_panel, previewWindow, focused_element, key, focused_porject)
            if focused_panel.getmaxyx() == menuWindow.getmaxyx():
                focused_porject =focused_element
            else:
                focused_task=focused_element
        if key == curses.KEY_RIGHT:
            focused_panel = previewWindow
            tasks = utils.list_tasks(focused_porject)
            focused_task = 0
            display_task_info(focused_panel, tasks, focused_task)
        if key == curses.KEY_LEFT:
            focused_panel = menuWindow
            display_projects(focused_panel, previewWindow, focused_porject)
        if key == ord(':'):
            cmd_line = curses.newwin(3, max_x - 1)
            cmd_line.mvwin(max_y - 4, 0)
            cmd_line.addch(1, 1, ':')
            cmd_line.border(' ', ' ', 0, 0, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
            cmd_line.hline(2, 0, ' ', max_x - 1)
            cmd_line.refresh()
            cmd_line.move(1, 2)  # Move cursor to allow writing after the colon

            curses.echo()  # Enable echoing of characters typed by the user
            cmd = ''
            while (ch := cmd_line.getch()) not in (10, curses.KEY_ENTER):  # Check for Enter key
                cmd += chr(ch)
                cmd_line.addch(1, len(cmd) + 1, ch)
                cmd_line.refresh()

            handle_cmd(cmd, cmd_line, menuWindow, previewWindow)
            cmd_line.clear()
            cmd_line.refresh()
            curses.noecho()  # Disable echoing after input is captured
            display_projects(menuWindow, previewWindow, focused_porject)
            # Process the user input (if needed)
            app.refresh()

curses.wrapper(lambda screen: main())