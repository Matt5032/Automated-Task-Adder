import time
from tkinter import messagebox
import tkinter
from tkinter import ttk as ttk
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import pickle

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


def on_close():
    try:
        if len(module_prefix) > 0:
            clear_before_close = messagebox.askyesno("Clear Tasks",
                                                     "Would you like to clear your current tasks before you go?")
        else:
            root.root.destroy()
        if clear_before_close is True:
            root.clear_module_prefixes()
            save_data()
            root.root.destroy()
        else:
            root.root.destroy()
    except:
        return


def start_up():
    load_data()


def save_data():

    save_list = [user_email, user_password, module_prefix]

    pickle.dump(save_list, open("save.p", "wb"))

    print(pickle.load(open("save.p", "rb")))


def load_data():
    global user_email
    global user_password
    global module_prefix

    load_list = pickle.load(open("save.p", "rb"))
    user_email = load_list[0]
    user_password = load_list[1]
    for i in load_list[2]:
        module_prefix.append(i)


class Main_Window:
    def __init__(self):
        #ROOT SETTINGS___________________________________________________
        self.root = tkinter.Tk()
        self.root.configure(bg="lightgrey")
        #self.root_geometry = self.root.geometry('500x300')
        self.root.resizable(False, False)
        self.root.title("Harvest Auto Task Adder V" + str(version))
        self.positionRight = int(self.root.winfo_screenwidth() / 2 - self.root.winfo_reqwidth() / 2)
        self.positionDown = int(self.root.winfo_screenheight() / 2 - self.root.winfo_reqheight() / 2)
        self.root.geometry("500x350+{}+{}".format(self.positionRight, self.positionDown))
        self.root.grid_columnconfigure(1, weight=1)

        #TABS_____________________________________________________________
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="lightgrey")
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Modules")
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Settings")
        self.tab_control.grid(pady=5)

        #FONT SETTINGS____________________________________________________
        self.text_font = "Helvetica", 10, "bold italic"
        self.label_font = "Arial", 12, "bold"
        self.button_font = "Arial", 8, "bold"

        self.entry_box_text = str()

        #CHECKBOX VARIABLES_______________________________________________
        self.clear_prefixes_on_startup = tkinter.IntVar()

        #WIDGET DEFINITIONS
            #MODULES TAB WIDGETS__________________________________________
        self.task_suffix_frame = tkinter.Frame(self.tab1,
                                       padx=35,
                                       bg="lightgrey")
        self.task_suffix_list_label = tkinter.Label(self.task_suffix_frame,
                                            text="Module Suffixs",
                                            font=self.label_font,
                                            bg="lightgrey")
        self.task_suffix_list = tkinter.Listbox(self.task_suffix_frame,
                                        width=25,
                                        justify=tkinter.CENTER,
                                        font=self.text_font)

        self.module_prefix_frame = tkinter.Frame(self.tab1,
                                         padx=35,
                                         bg="lightgrey")
        self. module_prefix_list_label = tkinter.Label(self.module_prefix_frame,
                                               text="Module Prefixs",
                                               font=self.label_font,
                                               bg="lightgrey")
        self. module_prefix_list = tkinter.Listbox(self.module_prefix_frame,
                                           width=25, justify=tkinter.CENTER,
                                           font=self.text_font)


        self.text_entry_frame = tkinter.Frame(self.tab1,
                                      padx=10,
                                      pady=10,
                                      bg="lightgrey")
        self.text_entry = tkinter.Entry(self.text_entry_frame)
        self.text_submit_button = tkinter.Button(self.text_entry_frame,
                                         text="Submit",
                                         command=self.submit_text_entry,
                                         font=self.button_font,
                                         width=7)
        self.clear_list_button = tkinter.Button(self.text_entry_frame,
                                        text="Clear",
                                        command=self.clear_module_prefixes,
                                        font=self.button_font,
                                        width=7)

        self.run_button = tkinter.Button(self.tab1,
                                 text="Run",
                                 width=10,
                                 height=2,
                                 font=self.button_font,
                                 command=self.run_confirm_dialog)

            #SETTINGS TAB WIDGETS_________________________________________________
        self.credentials_frame = tkinter.Frame(self.tab2)
        self.user_credentials_label = tkinter.Label(self.credentials_frame, text="Harvest User")
        self.user_email_entry = tkinter.Entry(self.credentials_frame, width=30, justify="center")
        self.user_email_entry.insert(0, user_email)
        self.user_password_entry = tkinter.Entry(self.credentials_frame, width=30, justify="center", show="*")
        self.user_password_entry.insert(0, user_password)
        self.submit_credentials = tkinter.Button(self.credentials_frame, text="Save", command=self.save_credentials)


    #POPUP MENU______________________________________________________________________________________________________
        self.popup_menu = tkinter.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_selected)
        self.module_prefix_list.bind("<Button-3>", self.popup)

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        try:
            selected = self.module_prefix_list.curselection()
            print(selected)
            self.module_prefix_list.delete(selected)

            del module_prefix[selected[0]]
            print(module_prefix)
        except:
            return
    #MAIN WIDGET PACKING______________________________________________________________________________________________
    def main_widgets(self):
        #SUFFIX LISTBOX
        self.task_suffix_frame.grid(row=0, column=1)
        self.task_suffix_list_label.grid()
        self.task_suffix_list.grid()


        #PREFIX LIST BOX
        self.module_prefix_frame.grid(row=0, column=0)
        self.module_prefix_list_label.grid()
        self.module_prefix_list.grid()


        #Entry Box and Submit Button
        self.text_entry_frame.grid(row=1, column=0)
        self.text_entry.grid(pady=3)
        self.text_submit_button.grid(pady=5)
        self.clear_list_button.grid()

        self.run_button.grid(row=1, column=1, pady=30)

        #SETTINGS_____________________
        self.credentials_frame.grid(padx=150)
        self.user_credentials_label.grid(padx=5, pady=5)
        self.user_email_entry.grid(padx=5, pady=5)
        self.user_password_entry.grid(padx=5, pady=5)
        self.submit_credentials.grid(padx=5, pady=5)

        self.update_listboxes()



    #BUTTON FUNCTIONS_______________________________________________________________________________________________
    def submit_text_entry(self):
        string = self.text_entry.get()
        new_string = string.title()
        if new_string in module_prefix or new_string == "":
            messagebox.showinfo("Error", "This Module Name Already Exists Or Nothing The Was Entered")
            self.text_entry.delete(0, 'end')
            return
        self.entry_box_text = new_string
        module_prefix.append(self.entry_box_text)
        self.update_listboxes()
        self.text_entry.delete(0, 'end')
        print(module_prefix)

    def clear_module_prefixes(self):
        if len(module_prefix) >= 1:
            del module_prefix[0:len(module_prefix)]
        self.update_listboxes()
        print(module_prefix)

    def update_listboxes(self):
        self.module_prefix_list.delete(0, 'end')
        self.task_suffix_list.delete(0, 'end')

        for i in TASK_SUFFIX:
            self.task_suffix_list.insert(tkinter.END, i)
        for i in module_prefix:
            self.module_prefix_list.insert(tkinter.END, i)

        self.user_email_entry.insert(0, user_email)
        self.user_password_entry.insert(0, user_password)

        save_data()

    def run_confirm_dialog(self):

        if len(module_prefix) <= 0:
            messagebox.showinfo("Error", "You Do Not Have Any Tasks")
        else:
            run_confirm = messagebox.askokcancel("Are You Sure You Want to Add Tasks?", "You Are About to Create "
                                                 + str(len(module_prefix))
                                                 + " Module(s) for a total of " +
                                                 (str(len(module_prefix) * (len(TASK_SUFFIX))))
                                                 + " Tasks"
                                                 + " as                             " + user_email)
            print(module_prefix)
            if run_confirm is True:
                run_task_add_script()
            else:
                return

    def task_complete(self, prefix_num):
        self.module_prefix_list.itemconfig(prefix_num, {'bg':'lightgreen'})
        print("Color Changed")





    #SETTINGS BUTTONS_____________________________________________________
    def save_credentials(self):
        if self.user_email_entry.get() == "" or self.user_password_entry.get() == "":
            messagebox.showinfo("Error", "Please Fill in All Fields to Save Credentials")
        else:
            new_user_email = self.user_email_entry.get()
            new_user_password = self.user_password_entry.get()
            user_email = new_user_email
            user_password = new_user_password
            print("New User Name: " + new_user_email)
            print("New Password: " + new_user_password)
            save_data()


root = Main_Window()


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
                    root.task_complete(prefix_num)

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
        

try:
    start_up()
except:
    pass
root.main_widgets()
root.root.protocol("WM_DELETE_WINDOW", on_close)
root.root.mainloop()