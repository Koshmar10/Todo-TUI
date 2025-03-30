import curses
from datetime import datetime
import utils

menuWindow = None
previewWindow = None
cmdWindow = None
projects= []
filtr=''
appWindows = {
    'menu' : menuWindow,
    'preview' : previewWindow,
    'cmd' : cmdWindow, 
}

def safe_addstr(window, y, x, string, *args):
    max_y, max_x = window.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        try:
            window.addstr(y, x, string, *args)
        except curses.error:
            pass

def display_projects(window, preview_window, focused_project, filtr=''):
    global projects
    window.clear()
    safe_addstr(window, 1, 1, "Projects")
    startOffset = 1
    for i, project in enumerate(projects):
        if i == focused_project:
            safe_addstr(window, startOffset + i * 2 + 2, 2, f'📌 {project[0]}', curses.color_pair(1))
            preview_window.clear()
            safe_addstr(preview_window, 1, 1, f"Project Tasks - Due: {project[1]}")

            tasks = utils.list_tasks(i)
            if len(tasks):
                for j, task in enumerate(tasks):
                    status = "✔" if task[2] else "❌"
                    string = f"{task[0]} {status}"
                    safe_addstr(preview_window, startOffset + j * 2 + 2, 2, string)
            else:
                safe_addstr(preview_window, startOffset + 2, 2, "No tasks added for this project")
        else:
            safe_addstr(window, startOffset + i * 2 + 2, 2, f'📌 {project[0]}', curses.color_pair(2))
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
    global projects
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
        if not tasks:
            return curr_elem
        if key_code == curses.KEY_DOWN:
            curr_elem += 1
        elif key_code == curses.KEY_UP:
            curr_elem -= 1
        if curr_elem < 0:
            curr_elem = 0
        curr_elem %= len(tasks)

        display_task_info(window, tasks, curr_elem)
    return curr_elem

def decode_cmd(cmdWindow, cmd):
    global projects
    if cmd is '':
        return 1
    arguments = cmd.split()
    
    cmd_name = arguments[0] #identify witch command is being used
    has_args = True if len(arguments) > 1 else False
    if has_args:
        #name chack
        if cmd_name == 'add' and len(arguments) == 3:
            pass
        else:
            if arguments[1] == 'project':
                display_cmdWindow()
                #need to probvide title and deadline
                title = take_input(cmdWindow, '', 'Project tilte')
                cmdWindow.clear()
                cmdWindow.addstr(1,1, f'Title set to: {title}')
                cmdWindow.refresh()
                curses.napms(800)
                display_cmdWindow()
                cmdWindow.refresh()
                deadline = take_input(cmdWindow, '', 'Project deadline( YYYY-MM-DD hh:mm )')
                while not utils.is_valid_deadline(deadline):
                    deadline = take_input(cmdWindow, '', 'Incorect format try again( YYYY-MM-DD hh:mm )')
                cmdWindow.clear()
                cmdWindow.addstr(1,1, f'Deadline set to: {deadline}')
                cmdWindow.refresh()
                curses.napms(800)
                display_cmdWindow()
                cmdWindow.refresh()
                utils.add_project(title, deadline)
                                    

                
            elif arguments[1] == 'projects':
                pass
            elif arguments[1] == 'task':
                pass
            elif arguments[1] == 'tasks':
                pass
            else:
                display_cmdWindow()
                cmdWindow.addstr(1, 2, 'Unrecognized command')
                cmdWindow.refresh()
                curses.napms(500)
                display_cmdWindow()
                return 1
            
    else:
        if cmd_name == 'today':
            filtr ='today'
            projects = utils.list_projects(filtr)
            display_projects(menuWindow, previewWindow, 0)
            return 0
        elif cmd_name == 'reset':
            filtr = ''
            projects = utils.list_projects()
            display_projects(menuWindow, previewWindow, 0)
            return 0
        elif cmd_name == 'priority':
            filtr = 'priority'
            projects = utils.list_projects(filtr)
            display_projects(menuWindow, previewWindow, 0)
            return 0
            
        else:
            display_cmdWindow()
            cmdWindow.addstr(1, 2, 'Unrecognized command')
            cmdWindow.refresh()
            curses.napms(500)
            display_cmdWindow()
            return 1

def handle_cmd(cmd, cmdwindow, menuWindow, previewWindow):
    cmd = cmd.strip()
    display_cmdWindow()
    return decode_cmd(cmdwindow, cmd)

def display_cmdWindow():
    global cmdWindow
    cmdWindow.clear()
    max_y, max_x = cmdWindow.getmaxyx()
    if max_y > 1 and max_x > 1:  # Ensure the window is large enough
        try:
            cmdWindow.addch(1, 1, ':')
        except curses.error:
            pass
    cmdWindow.addch(1,1, ':')
    cmdWindow.border(' ', ' ', 0, ' ', curses.ACS_LLCORNER, curses.ACS_LRCORNER, ' ', ' ')
    cmdWindow.refresh()

def take_input(window, cmd, custom_msg=''):
    window.clear()
    window.addstr(1, 1, f'{custom_msg}:')
    window.border(' ', ' ', 0, ' ', curses.ACS_LLCORNER, curses.ACS_LRCORNER, ' ', ' ')
    window.refresh()
    while (ch := window.getch()) not in (10, curses.KEY_ENTER):  # Check for Enter key
        if ch == 27:
            return True
        if ch in (8, 127, curses.KEY_BACKSPACE):
            cmd = cmd[:-1]  # Remove the last character from the string
        else:
            cmd += chr(ch)
        window.clear()
        window.addstr(1, 1, f'{custom_msg}: {cmd}')
        window.border(' ', ' ', 0, ' ', curses.ACS_LLCORNER, curses.ACS_LRCORNER, ' ', ' ')
        window.refresh()
    return cmd
    


def main():
    global menuWindow, previewWindow, cmdWindow, projects, filtr
    app = curses.initscr()
    projects = utils.list_projects()
    filtr=''

    curses.noecho()
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    app.attron(curses.color_pair(1))

    max_y, max_x = app.getmaxyx()

    menuWindow = curses.newwin(max_y - 1, int(max_x / 3))
    previewWindow = curses.newwin(max_y - 1, int(max_x * 2 / 3))
    cmdWindow = curses.newwin(3, max_x - 1)
            
    focused_panel = menuWindow
    focused_porject = 0
    focused_task = 0

    display_projects(menuWindow, previewWindow, 0)

    menuWindow.border()
    previewWindow.border()

    app.clear()
    app.refresh()

    menuWindow.mvwin(0, 0)
    previewWindow.mvwin(0, max_x // 3 - 1)
    cmdWindow.mvwin(max_y - 4, 0)

    cmdWindow.refresh()
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
            exit_code=1
            firsIter=True
            display_cmdWindow()
            end_key = cmdWindow.getch()
            while end_key != 27 and end_key not in (10, curses.KEY_ENTER):
                cmd = ''
                escaped=False
                cmd+=chr(end_key)
                cmdWindow.clear()
                cmdWindow.addstr(1, 1, f': {cmd}')
                cmdWindow.border(' ', ' ', 0, ' ', curses.ACS_LLCORNER, curses.ACS_LRCORNER, ' ', ' ')
                cmdWindow.refresh()
                inpt = take_input(cmdWindow, cmd)
                if  type(inpt) == type(True):
                    escaped = inpt
                elif type(inpt) == type('a'):
                    cmd+=inpt
                    cmdWindow.clear()
                    if cmd:
                        cmdWindow.addstr(1, 1, f': {cmd}')
                    cmdWindow.border(' ', ' ', 0, ' ', curses.ACS_LLCORNER, curses.ACS_LRCORNER, ' ', ' ')
                    cmdWindow.refresh()
                if not escaped:
                    exit_code =handle_cmd(cmd, cmdWindow, menuWindow, previewWindow)
                else:
                    break
                if exit_code == 0:
                    cmdWindow.clear()
                    previewWindow.refresh()
                    menuWindow.refresh()
                    break
                #display_projects(menuWindow, previewWindow, focused_porject)
                # Process the user input (if needed)
                display_cmdWindow()
                end_key = cmdWindow.getch()
                firsIter=False
            cmdWindow.clear()
            cmdWindow.refresh()
            display_projects(menuWindow, previewWindow, focused_porject, filtr)
        app.refresh()

curses.wrapper(lambda screen: main())