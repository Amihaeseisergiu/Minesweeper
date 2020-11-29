from tkinter import *
from tkinter import messagebox
import time
import threading
import random

time_limit = 0
stop_event = False
free_cells = 0
total_free_cells = 0

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

image_face_happy = PhotoImage(file = "./textures/face_happy.png")
image_face_happy = image_face_happy.zoom(20)
image_face_happy = image_face_happy.subsample(32)
image_face_dead = PhotoImage(file = "./textures/face_dead.png")
image_face_dead = image_face_dead.zoom(10)
image_face_dead = image_face_dead.subsample(32)
image_unpressed = PhotoImage(file = "./textures/unpressed.png")
image_pressed = PhotoImage(file = "./textures/pressed.png")
image_numbers = [
    PhotoImage(file = "./textures/1.png"),
    PhotoImage(file = "./textures/2.png"),
    PhotoImage(file = "./textures/3.png"),
    PhotoImage(file = "./textures/4.png"),
    PhotoImage(file = "./textures/5.png"),
    PhotoImage(file = "./textures/6.png"),
    PhotoImage(file = "./textures/7.png"),
    PhotoImage(file = "./textures/8.png"),
]
image_flag = PhotoImage(file = "./textures/flag.png")

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

menu_image = Label(game_name_frame, image = image_face_happy)
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

def gameOver(itself, reason):
    itself.grid_forget()

    global stop_event
    stop_event = True
    root.geometry("600x600")
    final_screen_frame = Frame(root)
    final_screen_frame.grid(row = 0, column = 0, sticky = 'we')
    final_screen_frame.columnconfigure(0, weight = 1)

    final_screen_label = Label(final_screen_frame, font = "Courier 20")
    final_screen_image = Label(final_screen_frame)

    if reason == 'time':
        final_screen_label['text'] = "You lost! Time ran down"
        final_screen_image['image'] = image_face_dead
    elif reason == 'bomb':
        final_screen_label['text'] = "You lost! You hit a bomb"
        final_screen_image['image'] = image_face_dead
    elif reason == 'won':
        final_screen_label['text'] = "You won!"
        final_screen_image['image'] = image_face_happy
    
    final_screen_label.grid(row = 0, column = 0)
    final_screen_image.grid(row = 1, column = 0)

    main_menu_button = Button(final_screen_frame, font = "Arial 15", text = "Main Menu")
    main_menu_button['command'] = lambda itself = final_screen_frame: mainMenu(itself)
    main_menu_button.grid(row = 2, column = 0, pady = 10)

def startGame():
    if table_size_entry_height.get() == "" and table_size_entry_width.get() != "":
        messagebox.showerror("Error", "Height has to be filled")
    elif table_size_entry_height.get() != "" and table_size_entry_width.get() == "":
        messagebox.showerror("Error", "Width has to be filled")
    elif table_size_entry_height.get() != "" and int(table_size_entry_height.get()) == 0:
        messagebox.showerror("Error", "Height has to be positive")
    elif table_size_entry_width.get() != "" and int(table_size_entry_width.get()) == 0:
        messagebox.showerror("Error", "Width has to be positive")
    elif table_size_entry_height.get() == "" and table_size_entry_width.get() == "" and nr_bombs_entry.get() != "" and int(nr_bombs_entry.get()) > 10 * 10:
            messagebox.showerror("Error", "Nr of bombs exceeds table size")
    elif table_size_entry_height.get() != "" and table_size_entry_width.get() != "" and nr_bombs_entry.get() != "" and int(nr_bombs_entry.get()) > int(table_size_entry_height.get()) * int(table_size_entry_width.get()):
            messagebox.showerror("Error", "Nr of bombs exceeds table size")
    elif table_size_entry_height.get() != "" and table_size_entry_width.get() != "" and nr_bombs_entry.get() == "" and 10 > int(table_size_entry_height.get()) * int(table_size_entry_width.get()):
            messagebox.showerror("Error", "Nr of bombs exceeds table size")
    else:
        main_menu_frame.grid_forget()

        nr_bombs = 10
        table_height = 10
        table_width = 10
        global time_limit
        global stop_event
        global free_cells
        global total_free_cells
        stop_event = False
        time_limit = 60
        if table_size_entry_height.get() != "" and table_size_entry_width.get() != "":
            table_height = int(table_size_entry_height.get())
            table_width = int(table_size_entry_width.get())
        if nr_bombs_entry.get() != "":
            nr_bombs = int(nr_bombs_entry.get())
        if time_limit_entry.get() != "":
            time_limit = int(time_limit_entry.get())

        total_free_cells = (table_height * table_width) - nr_bombs
        free_cells = 0

        available_positions = []
        for i in range(table_height):
            for j in range(table_width):
                available_positions.append([i, j])

        bomb_matrix = [[0 for i in range(table_width)] for y in range(table_height)]
        flag_matrix = [[0 for i in range(table_width)] for y in range(table_height)]
        for i in range(nr_bombs):
            r = random.randint(0, len(available_positions) - 1)
            bomb_matrix[available_positions[r][0]][available_positions[r][1]] = 1
            del available_positions[r]

        root.geometry("")
        main_game_frame = Frame(root)
        main_game_frame.grid(row = 0, column = 0, sticky = 'news')
        main_game_frame.rowconfigure(0, weight = 1)
        main_game_frame.rowconfigure(1, weight = 1)
        main_game_frame.columnconfigure(0, weight = 1)

        top_frame = Frame(main_game_frame)
        top_frame.grid(row = 0, column = 0, sticky = 'n')

        time_limit_label = Label(top_frame, font = "Arial 20", text = 'Time: {:02}:{:02}'.format(time_limit%3600//60, time_limit%60))
        time_limit_label.grid(row = 0, column = 0, pady = 10)

        def countdown():
            global time_limit
            global stop_event
            while time_limit > 0 and not stop_event:
                time.sleep(1)
                time_limit -= 1
                time_limit_label['text'] = 'Time: {:02}:{:02}'.format(time_limit%3600//60, time_limit%60)
            if not stop_event:
                gameOver(main_game_frame, "time")

        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.daemon = True
        countdown_thread.start()

        game_frame = Frame(main_game_frame)
        game_frame.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = 'n')

        button_matrix = [[0 for i in range(table_width)] for y in range(table_height)] 

        def walk(x, y):
            global free_cells

            if bomb_matrix[x][y] == 1:
                gameOver(main_game_frame, 'bomb')
            elif button_matrix[x][y]['relief'] != 'sunken' and flag_matrix[x][y] == 0:
                free_cells += 1
                direct_x = [-1, -1, -1,  0, 0,  1, 1, 1]
                direct_y = [ 0, -1,  1, -1, 1, -1, 0, 1]
                nr_bombs = 0
                for i in range(len(direct_x)):
                    if x + direct_x[i] < table_height and x + direct_x[i] >= 0 and y + direct_y[i] < table_width and y + direct_y[i] >=0:
                        if bomb_matrix[x + direct_x[i]][y + direct_y[i]] == 1:
                            nr_bombs += 1
                
                if nr_bombs == 0:
                    button_matrix[x][y]['command'] = 0
                    button_matrix[x][y]['relief'] = 'sunken'
                    button_matrix[x][y]['image'] = image_pressed
                    for i in range(len(direct_x)):
                        if x + direct_x[i] < table_height and x + direct_x[i] >= 0 and y + direct_y[i] < table_width and y + direct_y[i] >=0:
                            walk(x + direct_x[i], y + direct_y[i])
                else:
                    button_matrix[x][y]['command'] = 0
                    button_matrix[x][y]['relief'] = 'sunken'
                    button_matrix[x][y]['image'] = image_numbers[nr_bombs - 1]


        def click(button):
            global free_cells
            global total_free_cells
            x = button.grid_info()['row']
            y = button.grid_info()['column']
            walk(x, y)
            if free_cells == total_free_cells and total_free_cells != 0:
                gameOver(main_game_frame, 'won')

        def right_click(event):
            x = event.widget.grid_info()['row']
            y = event.widget.grid_info()['column']
            
            if button_matrix[x][y]['relief'] != 'sunken':
                if flag_matrix[x][y] == 1:
                    flag_matrix[x][y] = 0
                    button_matrix[x][y]['image'] = image_unpressed
                else:
                    flag_matrix[x][y] = 1
                    button_matrix[x][y]['image'] = image_flag

        for i in range(table_height):
            for j in range(table_width):
                button_matrix[i][j] = Button(game_frame, image = image_unpressed)
                button_matrix[i][j]['command'] = lambda button = button_matrix[i][j]: click(button)
                button_matrix[i][j].bind("<Button-2>", right_click)
                button_matrix[i][j].bind("<Button-3>", right_click)
                button_matrix[i][j].grid(row = i, column = j)

start_game_button = Button(start_game_frame, text = "Start", font = "Arial 15", command = startGame)
start_game_button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "we") 

root.mainloop()