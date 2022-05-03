# Task management program that can be used for a small business to manage tasks assigned to each memmber of the team

#Prompts user for username and password till correct credentials are provided
#Only admin user with correct password can log in
while True:
    default_username = "admin"
    default_password = "adm1n"
    name = input("Enter your username: ")
    password = input("Enter your password: ")

    if name == default_username and password == default_password:
        print("You have succesfully logged in")
        break
    else:
        print("Only admin is allowed to log in")

print('\n')          

#Prompts user to select an option from the menu
def print_menu():
    print('r - Registering a user')
    print('a - Adding a task')
    print('va - View all tasks')
    print('vm - view my task')
    print('gr - generate reports')
    print('ds - Display statistics')
    print('e - Exit')
    print

#Ensures usernames are not duplicated and passwords match   
def reg_user():
    with open('user.txt','r') as reg_file:
        new_username = input("Enter your username: ")
        for line in reg_file:
            default_user = line.split(",")[0]
            while new_username == default_user:
                print("Your username already exists, please try again")
                new_username = input("Enter your new username: ")
        else:
            new_password = input("Enter your new password: ")
            renter_password = input("Re-enter your password for confirmation: ")
            while new_password != renter_password:
                print("Your passwords does not match, please renter your password ")
                new_password = input("Enter your new password: ")
                renter_password = input("Re-enter your password for confirmation: ")
            with open('user.txt' , 'a+') as user_file:
                user_file.write("\n" + new_username + ", ")
                user_file.write(renter_password)
                user_file.close()
                            
#Allows user to add additional tasks
def add_task():
        username = input("\nEnter the username of the person whom the task is assigned to: ")
        title = input("Enter the title of the task: " )
        description = input("Enter the description of the task: ")
        task_date = input("Enter the date the task was assigned in the format dd-mm-yyyy: ")
        due_date = input("Enter the task's due date in the format dd-mm-yyyy: ")
        status = input("Enter a 'Yes' or 'No' to specify if the task has been completed: ")
        with open('tasks.txt' , 'a+') as task_file:
            task_file.write("\n" + username + ", " + title + ", " + description + ", " + task_date + ", " + due_date + ", " + status)
            task_file.close()

#Allows user to view all tasks
def view_all():
    read_file = open('tasks.txt' , 'r+' , encoding='utf-8')
    for line in read_file:
        field = line.strip().split(",")
        print("\nTask: " + field[1] +"\nAssigned to: " + field[0] +
            "\nDate assigned: " + field[3]+ "\nDue date: " + field[4]+
            "\nTask complete? " + field[5] + "\nTask description: " + field[2] + "\n")

    read_file.close()

#Displays user specfic task and allows for edits
def view_mine():
    username = input("Please enter the username which you want to view the tasks for?\n")
    num_task = 0
    view_more = open('tasks.txt', 'r')
    for row in view_more:
        field = row.strip().split(",")
        num_task += 1
        # Numbers each task
        if username == field[0]:
            print("Task Number: " + str(num_task) +
                  "\nTask: " + field[1] +"\nAssigned to: " + field[0] +
                  "\nDate assigned: " + field[3]+ "\nDue date: " + field[4]+
                  "\nTask complete? " + field[5] + "\nTask description: " + field[2] + "\n")

    #Allows user to edit or return back to main menu
    edit_task = input("Would you like to edit a task? (Edit) or return to the main menu (-1) ").lower()
    if edit_task == "-1":
        print_menu()

    elif edit_task == 'edit':
        task_num = int(input("Please enter your task number you want to view?\n"))
        task_num = task_num -1
        edit_file = open('tasks.txt' , 'r')
        task_file = edit_file.readlines()
        for line in task_file:
            print(task_file[task_num] + "\n")
            break

        task_complete = input("Has this task been completed?\n")
        if task_complete == "Yes":
            user_task = task_file[task_num].strip().split(",")
            user_task[5] = "Yes"

        elif task_complete == "No":
            user_task = task_file[task_num].strip().split(",")
            user_task[5] = "No"            
      
    user_task = task_file[task_num].strip().split(",")
    new_state = task_file[task_num].strip().replace(user_task[5],task_complete)
    print('Your edit was succesful')
    updated_string = line.replace(task_file[task_num].strip(),new_state)

    #Writes updated task in new file updated_tasks
    with open('updated_tasks.txt' , 'w+') as updated_file:
        updated_file.write(updated_string)

    view_more.close()
    edit_file.close()
    updated_file.close()

#Generates task_overview and user_overview reports
def generate_reports():

    import datetime

    with open('tasks.txt', 'r') as text_file:
        contents = text_file.readlines()

    num_tasks = 0
    num_complete_tasks = 0
    num_uncomplete_tasks = 0
    num_overdue_tasks = 0

    for line in contents:
        num_tasks +=1
        if 'Yes' in line:
            num_complete_tasks +=1
        if 'No' in line:
            num_uncomplete_tasks +=1

    #Converts date to yyyy-mm-dd
        line = line.split(",")
        date, month, year = line[4].split("-")
        date = int(date)
        month = int(month)
        year = int(year)
        due_date = datetime.date(year, month, date)
        today = datetime.date.today()
        line = ",".join(line)
        if today > due_date:
            num_overdue_tasks +=1

    #Calculates percentages
    uncomplete_percentage = (num_uncomplete_tasks/num_tasks)*100
    overdue_percentage = (num_overdue_tasks/num_tasks)*100

    #Converts integers to strings
    total_no_tasks = str(num_tasks)
    total_no_complete_tasks = str(num_complete_tasks)
    total_no_uncompleted_tasks = str(num_uncomplete_tasks)
    total_no_overdue = str(num_overdue_tasks)
    total_complete_percent = str(round(uncomplete_percentage,1))
    total_uncomplete_percent = str(round(overdue_percentage,1))

    #Writes outputs to task_overview file
    with open('task_overview.txt', 'w') as stats_file:
        stats_file.write("Total tasks\t\t\t:" + total_no_tasks + "\n" )
        stats_file.write("Completed tasks\t\t\t:" + total_no_complete_tasks + "\n" )
        stats_file.write("Uncompleted tasks\t\t:" + total_no_uncompleted_tasks + "\n")
        stats_file.write("Tasks overdue\t\t\t:" + total_no_overdue + "\n")
        stats_file.write("Percentage of incomplete tasks\t:" + total_complete_percent + "%\n")
        stats_file.write("Percentage of overdue tasks\t:" + total_uncomplete_percent + "%")

    stats_file.close()
    text_file.close()
    
    with open('user.txt' , 'r') as user_report_file:
        user_contents = user_report_file.readlines()

    num_users = 0
    users = ""
    for line in user_contents:
        num_users +=1
        temp = line.split(",")
        users += temp[0] + " "

    users = users.split()
    total_num_user_task_list = []
    num_user_task_list = []
    num_user_task_complete_list = []
    num_user_task_incomplete_list = []
    num_user_task_overdue_list = []

    for user in users:
        num_user_task = 0
        num_user_task_complete = 0
        num_user_task_incomplete = 0
        num_user_task_overdue = 0

        for line in contents:
            if user in line:
                num_user_task += 1
                if 'Yes' in line:
                    num_user_task_complete += 1
                elif 'No' in line:
                    num_user_task_incomplete +=1
                elif 'No' in line and date > due_date:
                    num_user_task_overdue +=1


    if num_user_task > 0:
        user_percent = (100/num_tasks) * num_user_task
        user_complete_percent = (100/num_user_task) * num_user_task_complete
        user_incomplete_percent = (100/num_user_task) * num_user_task_incomplete
        user_overdue_percent = (100/num_user_task) * num_user_task_overdue
    else:
        user_percent = 0
        user_complete_percent = 0
        user_incomplete_percent = 0
        user_overdue_percent = 0

    total_num_user_task_list.append(num_user_task)
    num_user_task_list.append(user_percent)
    num_user_task_complete_list.append(user_complete_percent)
    num_user_task_incomplete_list.append(user_incomplete_percent)
    num_user_task_overdue_list.append(user_overdue_percent)


    num_users_report = 'Total users\t\t\t:' + str(num_users) + '\n'
    num_users_tasks_report = 'Total tasks\t\t\t:' + str(num_tasks)

    each_users_output = []
    count = 0
    for user in users:
        each_users_output.append("\n" + user + "\nTasks assigned\t\t\t:" +
                                        str(total_num_user_task_list) +
                                        "\nTasks assigned of total tasks\t:" +
                                        str(num_user_task_list) +
                                        "%\nTasks assigned completed\t:" +
                                        str(num_user_task_complete_list) +
                                        "%\nTasks assigned incomplete\t:" +
                                        str(num_user_task_incomplete_list) +
                                        "%\nTasks assigned overdue\t\t:" +
                                        str(num_user_task_overdue_list) + "%\n")
        count +=1

    each_users_output_new = ' '.join(each_users_output)

    with open('user_overview.txt' , 'w') as report_file:
        report_file.write(num_users_report)
        report_file.write(num_users_tasks_report)

    with open('user_overview.txt' , 'a') as amended_file:
        amended_file.write(each_users_output_new)

#Displays statistics
def display_stats():
    tasks_overview_file = open('task_overview.txt', 'r')
    tasks_content = tasks_overview_file.readlines()
    for line in tasks_content:
        print(line)
    print('\n')

    user_overview_file = open('user_overview.txt', 'r')
    user_content = user_overview_file.readlines()
    for line in user_content:
        print(line)

    tasks_overview_file.close()
    user_overview_file.close()

#Prompts user to select an option from the menu
while True:
        print_menu()
        menu = input('Select one of the following options: ').lower()
        print('\n')

        #User registers new username and password
        #Should the password be incorrect, prompts user to enter correct password
        if menu == 'r':
                pass
                user_login = reg_user()

                print('\n')

        #Prompts user to add addtional tasks to the text file
        elif menu == 'a':
                pass
                adding_tasks = add_task()
                print('\n')

        #User can view all tasks in the text file
        elif menu == 'va':
                pass
                all_tasks = view_all()
                print('\n')    

        #User selects specific task to be viewed
        elif menu == 'vm':
                pass
                specific_task = view_mine()
        
                print('\n')

        #User generates reports
        elif menu == 'gr':
            pass
            generating = generate_reports()
            print('\n')

        #Displays the total number of tasks and users
        elif menu == 'ds':
                pass
                displaying = display_stats()
                print('\n')

        #Program exits
        elif menu == 'e':
                print('Goodbye!!!')
                exit()

        #Should the wrong option be selected prompts user to select correct options in menu
        else:
                 print("You have made a wrong choice, Please Try again\n")
