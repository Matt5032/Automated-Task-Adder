import time
from tkinter import messagebox
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import HarvestTaskAdderMain as htam




version = 1.1


TASK_SUFFIX = ["Audio Order",
                "Final Draft Revisions",
                "Final File Delivery",
                "First Draft Development",
                "First Draft Revisions",
                "Internal Review",
                "Syncing Audio"]

module_prefix = []

user_email = ""
user_password = ""



def run_task_add_script():

    if user_password != "" or user_email != "":
        try:
            #Open Chrome and Go to HarvestApp.com
            driver = webdriver.Chrome("C:/Users/Matt/pycharmprojects/harvesttaskadder/chromedriver.exe")
            print("Chrome Opened")
            driver.get('https://id.getharvest.com/harvest/sign_in');
            print("Went to Harvest Sign in")
            #Enter email into login box
            email_box = driver.find_element_by_name('email')
            email_box.send_keys(user_email)
            print("Email Entered: " + user_email)
            #enter password into login box
            password_box = driver.find_element_by_name('password')
            password_box.send_keys(user_password)
            print("Password Entered: " + user_password)
            #submit email and password
            login_submit_button = driver.find_element_by_name('button')
            login_submit_button.submit()
            print("Credentials Submitted")
            #click on Yukon Learning account link
            account_link = driver.find_element_by_link_text('Yukon Learning')
            account_link.click()
            print("Account Selected")
            #click manage link
            manage_link = driver.find_element_by_link_text('Manage')
            manage_link.click()
            print("Manage Link Clicked")
            #click tasks link
            tasks_link = driver.find_element_by_link_text('Tasks')
            tasks_link.click()
            print("Tasks Link Clicked")
            #click New Task button
            new_task_button = driver.find_element_by_class_name('hui-button-icon-left')
            new_task_button.click()
            print("New Task Form Opened")
            #enter module info into input
            enter_task_name = driver.find_element_by_class_name('hui-input')
            submit_task_button = driver.find_element_by_name('commit')
            for prefix_num in range(0, len(module_prefix)):
                global module_complete
                global module_num
                module = module_prefix[prefix_num]
                entry_tally = 0
                for suffix_num in range(0, len(TASK_SUFFIX)):
                    try:
                        task = TASK_SUFFIX[suffix_num]
                        new_task_button.click()
                        enter_task_name.send_keys(module + ": " + task)
                        time.sleep(1) # Let the user actually see something!
                        submit_task_button.click()
                        print(module + ": " + task + " Added")
                        entry_tally += 1

                        driver.implicitly_wait(5)
                    except StaleElementReferenceException:
                        driver.implicitly_wait(5)
                        task = TASK_SUFFIX[suffix_num]
                        new_task_button = driver.find_element_by_class_name('hui-button-icon-left')
                        new_task_button.click()
                        enter_task_name = driver.find_element_by_class_name('hui-input')
                        submit_task_button = driver.find_element_by_name('commit')
                        enter_task_name.send_keys(module + ": " + task)
                        time.sleep(1) # Let the user actually see something!
                        submit_task_button.click()
                        print(module + ": " + task + " Added")
                        entry_tally += 1
                        driver.implicitly_wait(5)
                    htam.root.task_complete(prefix_num)

            #confirm message all tasks have been entered
            print(str(entry_tally) + " Entries Completed")
            messagebox.showinfo("Completed", "All Tasks Have Been Added!")
        except Exception as e:
            print(e)
            messagebox.showinfo("Process Canceled", ("The window was closed and interrupted the process.\n "
                                                    + "Be sure to correct or delete any data that was input into Harvest.\n "
                                                    + "Rerunning the Process with the same data will not account for entries already entered into Harvest"))
    else:
        print("Email or Password is Blank.")