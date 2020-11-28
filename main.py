from tkinter import *
from tkinter import messagebox

class Entry_number(Entry):
    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit() or self.get() == "":
            self.old_value = self.get()
        else:
            self.set(self.old_value)

root = Tk()
root.geometry("600x600")
root.title("Minesweeper")
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

main_menu_frame = Frame(root)
main_menu_frame.grid(row = 0, column = 0, sticky = 'news')
main_menu_frame.columnconfigure(0, weight = 1)
main_menu_frame.rowconfigure(0, weight = 1)
main_menu_frame.rowconfigure(1, weight = 1)

game_name_frame = Frame(main_menu_frame)
game_name_frame.grid(row = 0, column = 0, sticky = 'news')
game_name_frame.columnconfigure(0, weight = 1)

game_name_label = Label(game_name_frame, text = "Minesweeper")
game_name_label.grid(row = 0, padx = 20, pady = 10, column = 0)
game_name_label.config(font=("Courier", 30))

game_image = PhotoImage(file = "./textures/menu_face.png")
game_image = game_image.zoom(20) #with 250, I ended up running out of memory
game_image = game_image.subsample(32)
menu_image = Label(game_name_frame, image = game_image)
menu_image.grid(row = 1, column = 0)

game_options_frame = Frame(main_menu_frame)
game_options_frame.grid(row = 1, column = 0, sticky = 'n')

group_options1_frame = Frame(game_options_frame)
group_options1_frame.grid(row = 0, column = 0)
group_options2_frame = Frame(game_options_frame)
group_options2_frame.grid(row = 0, column = 1)

table_size_label = Label(group_options1_frame, text = "Table size:")
table_size_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
table_size_label.config(font=("Arial", 15))

table_size_entry_height = Entry_number(group_options2_frame, font = "Arial 15", width = "3")
table_size_entry_height.grid(row = 0, column = 0, padx = 10, pady = 10)

table_size_x_label = Label(group_options2_frame, text = "X")
table_size_x_label.grid(row = 0, column = 1, pady = 10)
table_size_x_label.config(font=("Arial", 15))

table_size_entry_width = Entry_number(group_options2_frame, font = "Arial 15", width = "3")
table_size_entry_width.grid(row = 0, column = 2, padx = 10, pady = 10)

time_limit_label = Label(group_options1_frame, text = "Time Limit:")
time_limit_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")
time_limit_label.config(font=("Arial", 15))

time_limit_entry = Entry_number(group_options2_frame, font = "Arial 15", width = "3")
time_limit_entry.grid(row = 1, column = 0, padx = 10, pady = 10)

nr_bombs_label = Label(group_options1_frame, text = "Bombs:")
nr_bombs_label.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "w")
nr_bombs_label.config(font=("Arial", 15))

nr_bombs_entry = Entry_number(group_options2_frame, font = "Arial 15", width = "3")
nr_bombs_entry.grid(row = 2, column = 0, padx = 10, pady = 10)

start_game_frame = Frame(game_options_frame)
start_game_frame.grid(row = 1, column = 0, columnspan = 2, sticky = "we")
start_game_frame.columnconfigure(0, weight = 1)
start_game_frame.rowconfigure(0, weight = 1)

def mainMenu(itself):
    itself.grid_forget()
    main_menu_frame.grid(row = 0, column = 0, sticky = 'news')

def startGame():
    if table_size_entry_height.get() == "" and table_size_entry_width.get() != "":
        messagebox.showerror("Error", "Height has to be filled")
    elif table_size_entry_height.get() != "" and table_size_entry_width.get() == "":
        messagebox.showerror("Error", "Width has to be filled")
    elif table_size_entry_height.get() != "" and int(table_size_entry_height.get()) == 0:
        messagebox.showerror("Error", "Height has to be positive")
    elif table_size_entry_width.get() != "" and int(table_size_entry_width.get()) == 0:
        messagebox.showerror("Error", "Width has to be positive")
    else:
        main_menu_frame.grid_forget()
        placeholder = Button(root, text = "Main Menu")
        placeholder['command'] = lambda itself = placeholder: mainMenu(itself)
        placeholder.grid(row = 0, column = 0)

start_game_button = Button(start_game_frame, text = "Start", font = "Arial 15", command = startGame)
start_game_button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "we") 

root.mainloop()