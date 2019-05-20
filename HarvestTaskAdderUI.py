'''TODO
-Add tkinter to all tkinter imports
'''
#General tkinter import
import tkinter
import HarvestTaskAdderScript as htas
#importing ttk wrapper for tkinter
from tkinter import ttk as ttk
#importing messagebox because tkinter.messagebox doesnt work for some reason
from tkinter import messagebox

import pickle


def start_up():
    load_data()

def save_data():

    save_list = [htas.user_email, htas.user_password, htas.module_prefix]

    pickle.dump(save_list, open("save.p", "wb"))

    print(pickle.load(open("save.p", "rb")))

def load_data():
    #global user_email
    #global user_password
    #global module_prefix

    load_list = pickle.load(open("save.p", "rb"))
    htas.user_email = load_list[0]
    htas.user_password = load_list[1]
    for i in load_list[2]:
        htas.module_prefix.append(i)







class Main_Window:
    def __init__(self):
        #ROOT SETTINGS___________________________________________________
        self.root = tkinter.Tk()
        self.root.configure(bg="lightgrey")
        #self.root_geometry = self.root.geometry('500x300')
        self.root.resizable(False, False)
        self.root.title("Harvest Auto Task Adder V" + str(htas.version))
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
        self.user_email_entry.insert(0, htas.user_email)
        self.user_password_entry = tkinter.Entry(self.credentials_frame, width=30, justify="center", show="*")
        self.user_password_entry.insert(0, htas.user_password)
        self.submit_credentials = tkinter.Button(self.credentials_frame, text="Save", command=self.save_credentials)

        #self.options_frame = Frame(self.tab2)
        #self.options_label = Label(self.options_frame,  text="Options", width=19, font=self.label_font)
        #self.clear_on_startup_checkbox = Checkbutton(self.options_frame, variable=self.clear_prefixes_on_startup, text="Clear Prefixes on Startup")


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

            del htas.module_prefix[selected[0]]
            print(htas.module_prefix)
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

        #self.options_frame.grid()
        #self.options_label.grid(pady=(15, 0))
        #self.clear_on_startup_checkbox.grid()

        self.update_listboxes()



    #BUTTON FUNCTIONS_______________________________________________________________________________________________
    def submit_text_entry(self):
        string = self.text_entry.get()
        new_string = string.title()
        if new_string in htas.module_prefix or new_string == "":
            messagebox.showinfo("Error", "This Module Name Already Exists Or Nothing The Was Entered")
            self.text_entry.delete(0, 'end')
            return
        self.entry_box_text = new_string
        htas.module_prefix.append(self.entry_box_text)
        self.update_listboxes()
        self.text_entry.delete(0, 'end')
        print(htas.module_prefix)

    def clear_module_prefixes(self):
        if len(htas.module_prefix) >= 1:
            del htas.module_prefix[0:len(htas.module_prefix)]
        self.update_listboxes()
        print(htas.module_prefix)

    def update_listboxes(self):
        global user_email
        global user_password
        self.module_prefix_list.delete(0, 'end')
        self.task_suffix_list.delete(0, 'end')

        for i in htas.TASK_SUFFIX:
            self.task_suffix_list.insert(tkinter.END, i)
        for i in htas.module_prefix:
            self.module_prefix_list.insert(tkinter.END, i)

        self.user_email_entry.insert(0, htas.user_email)
        self.user_password_entry.insert(0, htas.user_password)

        save_data()

    def run_confirm_dialog(self):

        if len(htas.module_prefix) <= 0:
            messagebox.showinfo("Error", "You Do Not Have Any Tasks")
        else:
            run_confirm = messagebox.askokcancel("Are You Sure You Want to Add Tasks?", "You Are About to Create "
                                                 + str(len(htas.module_prefix))
                                                 + " Module(s) for a total of " +
                                                 (str(len(htas.module_prefix) * (len(htas.TASK_SUFFIX))))
                                                 + " Tasks"
                                                 + " as                             " + htas.user_email)
            print(htas.module_prefix)
            if run_confirm is True:
                htas.run_task_add_script()
            else:
                return



    #SETTINGS BUTTONS_____________________________________________________
    def save_credentials(self):
        #global user_email
        #global user_password
        if self.user_email_entry.get() == "" or self.user_password_entry.get() == "":
            messagebox.showinfo("Error", "Please Fill in All Fields to Save Credentials")
        else:
            new_user_email = self.user_email_entry.get()
            new_user_password = self.user_password_entry.get()
            htas.user_email = new_user_email
            htas.user_password = new_user_password
            print("New User Name: " + new_user_email)
            print("New Password: " + new_user_password)
            save_data()









