### -------------------- PROGRAM EXPLANATION
# This program helps to manage tasks assigned to different members of a team.
# User has the option to add a new task, view all tasks or tasks specific to them.
# If the user has admin access, they can perform additional functions such as 
# registering a new user, generating reports and displaying system statistics.


# Importing required modules
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d %b %Y" # Changed from %Y-%m-%d to %d %b %Y to 
                                    # overcome error in original code.

### -------------------- DEFINING TASK CLASS
# The following code defines a Class for the tasks.
# This contains methods that convert the task from a string to an object, 
# convert tasks from an object to a string, and methods that display the task 
# in a readable format to the user.
class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(", ") # Changed ";" to ", " to overcome error in
        username = tasks[0]          # original code.
        title = tasks[1]
        description = tasks[2]
        assigned_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        due_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT), 
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ", ".join(str_attrs)
    
    def display(self,task_num):
        '''
        Display object in readable format
        '''
        disp_str = f"Task {task_num}: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        disp_str += f"Task Completion Status: \n {self.completed}\n"

        return disp_str

### -------------------- READING FROM/WRITING TO FILES    
# A file called 'tasks.txt' stores each task in a string format.
# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Storing each task in string format as individual elements of list 'task_data'.
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Converting tasks into objects and storing as individual elements of list 'task_list'.
task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# A file called 'user.txt' stores each user's username & password in a string format.
# Read and parse user.txt
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';') 
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

### -------------------- DATA VALIDATION & STORING
def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))

### -------------------- SYSTEM FUNCTION
def reg_user():
    '''
    Registering New Users:
    This function allows the admin to register new users.
    It confirms whether a username already exists in the system to prevent the
    duplication of usernames.
    '''
    # Checks if user is admin, then requests them to input a new username for 
    # the new user.
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
        return
    new_username = input("New Username: ")

    # Checks if username exists in 'user.txt' file. If so, an error message is
    # displayed, and admin is prompted to try again with a different username.
    with open('user.txt','r') as file:
        for line in file:
            if new_username in line:
                print("Username already exists. Please try again with a different username.")
                return

    # Request input of a new password
    new_password = input("New Password: ")

    if not check_username_and_password(new_username, new_password):
        # Username or password is not safe for storage - continue
        return

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")

        # Add to dictionary and write to file
        username_password[new_username] = new_password
        write_usernames_to_file(username_password)

    # Otherwise you present a relevant message.
    else:
        print("Passwords do no match")        

def add_task():
    '''
    Adding Tasks:
    This function prompts a user for the following:
    - A username of the person whom the task is assigned to.
    - A title of a task.
    - A description of the task.
    - The due date of the task.
    '''

    # Ask for username
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task DD MMM YYYY (e.g. 18 Jun 2019): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Obtain and parse current date
    curr_date = date.today()
    
    # Create a new Task object and append to list of tasks
    new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False)
    task_list.append(new_task)

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")

def view_all():
    '''
    View All Tasks:
    This function allows user to view all tasks in the system in a readable
    format.
    If there are no tasks, a message stating this is shown instead.
    '''
    print("-----------------------------------")
    # If there are no tasks, a message saying 'There are no tasks' is displayed.
    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")
    # If there are tasks, they are numbered and displayed to user. 
    else:
        for task_number, task in enumerate(task_list):
                print(task.display(task_number+1))
                print("-----------------------------------")

def view_mine():
    '''
    View My Tasks:
    This function allows users to view tasks assigned specifically to them.
    It also gives them the ability to select a task and mark it as completed, 
    or change who the task is assigned to or its due date.
    '''
    print("-----------------------------------")
    has_task = False
    # Checking if user has tasks and if so, displays them in the console.
    for task_number, task in enumerate(task_list):
        if task.username == curr_user:
                has_task = True
                print(task.display(task_number+1))
                print("-----------------------------------")

    # If user has no tasks, the message 'You have no tasks' is displayed.
    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")
    
    # Requests user to select the task they would like to view.
    selected_task = input('''
    Enter the number of the task you would like to view.
    Or else, enter '-1' to go back to the main menu.
    :
    ''')
    # For the selected task, user has the option to mark task as completed 
    # or to edit the tasks details.
    for task_number in range(0,len(task_data)):
        if selected_task == f"{task_number+1}":
            
            selected_task_obj = task_list[task_number]
            
            user_option = input('''Select an option:
            edit \t Edit Task
            comp \t Mark as Complete
            : ''')
            
            if user_option == "comp":
                selected_task_obj.completed = "Yes"

            elif user_option == "edit" and getattr(task_list[task_number],'completed') != "Yes":
                updated_username = input("Enter username of who you want to assign task to?: ").lower()
                selected_task_obj.username = updated_username
                new_duedate = input("Enter the new due date in the format 'DD MMM YYYY' (e.g. 18 Jun 2019): ")
                selected_task_obj.due_date = datetime.strptime(new_duedate, DATETIME_STRING_FORMAT)
            else:
                print("Something went wrong...")
            
            # Update the original task file with new details.
            for task_number in range(0,len(task_list)):
                with open("tasks.txt","w+") as file:
                    file.write("\n".join([t.to_string() for t in task_list]))
        
        # If user enters '-1' when prompted to enter the task number, they are
        # taken back to the main menu.
        elif selected_task == "-1":
            return

def display_stats():
    '''
    Display Statistics:
    This function allows the admin to display statistics of the system such as:
    - The total number of users.
    - The total number of tasks.
    It also displays the contents of 2 files that contains more indepth stats 
    related to tasks and users on the system.
    '''

    # Calculating the total number of tasks and users and displaying this in 
    # the console. 
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")

    # Checking if 'task_overview.txt' and 'user_overview.txt' files exist.
    # If so, their contents are read and displayed in the console.
    # If these files do not exist, the function responsible for generating them
    # is executed, and their contents are then read & displayed.
    report_list = ["task_overview.txt", "user_overview.txt"]
    for report in report_list:
        if os.path.exists(report):
            print(f"\n{report} Contents: \n")
            with open(report,"r") as task_file:
                lines = task_file.read().split("\n")
                for line in lines:
                    print(line)
        else:
            generate_reports()
            print(f"\n{report} Contents: \n")
            with open(report,"r") as task_file:
                lines = task_file.read().split("\n")
                for line in lines:
                    print(line)

def generate_reports():
    '''

    Generate Reports:
    This function allows the admin to generate reports containing information
    related to system statistics. It generates 2 .txt files:
    'task_overview.txt':
    - Number of Completed Tasks.
    - Number of Incomplete Tasks.
    - Number of Overdue Tasks.
    - Percentage of Incomplete Tasks.
    - Percentage of Overdue Tasks.

    'user_overview.txt':
    - The total number of users.
    - The total number of tasks.
    And for each user:
    - Number of Tasks assigned to them.
    - Percentage of Total Number of Tasks assigned to them.
    - Percentage of Tasks assigned to them that have been completed.
    - Percentage of Tasks assigned to them that still need to be completed.
    - Percentage of Tasks assigned to them that are still incomplete and overdue.

    '''

    # Write stats to 'task_overview.txt'.
    with open('task_overview.txt','w+') as task_report:
        task_report.write(f"Total # of Tasks: \t\t {len(task_data)}\n")

        curr_date = datetime.today()

        overdue = 0
        incomplete = 0
        complete = 0

        # Checking if file is overdue and its completion status.
        for task in task_list:
            due_date = getattr(task,'due_date')
            if curr_date > due_date and getattr(task,'completed') != "Yes":
                overdue += 1
            
            if getattr(task,'completed') != "Yes":
                incomplete += 1
            elif getattr(task,'completed') == "Yes":
                complete += 1
        
        task_report.write(f"# of Completed Tasks: \t\t {complete} out of {len(task_list)} tasks.\n")
        task_report.write(f"# of Incomplete Tasks: \t\t {incomplete} out of {len(task_list)} tasks.\n")
        task_report.write(f"# of Overdue Tasks: \t\t {overdue} out of {len(task_list)} tasks.\n")
        task_report.write(f"% of Incomplete Tasks: \t\t {(incomplete/len(task_list))*100}%\n")
        task_report.write(f"% of Overdue Tasks: \t\t {(overdue/len(task_list))*100}%")
    
    # Write stats to 'user_overview.txt'.
    with open('user_overview.txt','w+') as user_report:
        user_report.write(f"Number of Users: {len(user_data)}\n")
        user_report.write(f"Number of Tasks: {len(task_data)}\n")
        user_report.write(f"-----------------------------------\n")
    
    with open('user_overview.txt','a+') as user_report:
        
        # Obtaining stats for each user in system.
        for user in dict.keys(username_password):

            user_tasks = 0
            user_completed = 0
            user_incomplete = 0
            user_overdue = 0

            for task in task_list:
                if getattr(task,'username') == user:
                    user_tasks += 1
                
                if getattr(task,'completed') == "Yes":
                    user_completed += 1
                elif getattr(task,'completed') != "Yes":
                    user_incomplete += 1
                
                due_date = getattr(task,'due_date')
                if curr_date > due_date and getattr(task,'completed') != "Yes":
                    user_overdue += 1

            user_report.write(f"{user} has {user_tasks} tasks.\n")
            user_report.write(f"{user} is assigned {(user_tasks/len(task_list))*100}% of the tasks.\n")
            if user_tasks >= 0:
                try:
                    user_report.write(f"{user} has completed {(user_completed/user_tasks)*100}% of their assigned tasks.\n")
                    user_report.write(f"{user} has {(user_incomplete/user_tasks)*100}% of their assigned tasks left to complete.\n")
                    user_report.write(f"{user} has {(user_overdue/user_incomplete)*100}% of their incomplete tasks overdue.\n")
                    user_report.write(f"-----------------------------------\n")
                except ZeroDivisionError:
                    user_report.write(f"{user} has 0 tasks assigned - cannot compute percentage of task completion.\n")
                    user_report.write(f"{user} has 0 tasks assigned - cannot compute percentage of tasks still incomplete.\n")
                    user_report.write(f"{user} has 0 tasks assigned - cannot compute percentage of incomplete tasks that are overdue.\n")
                    user_report.write(f"-----------------------------------\n")

#########################
# Main Program
######################### 

while True:
# Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds' and curr_user == 'admin':
        display_stats()
    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()
    else: # Default case
        print("You have made a wrong choice, Please Try again")