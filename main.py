from tkinter import *
from tkinter import messagebox
import time
import threading
import random

time_limit = 0
stop_event = False
free_cells = 0
total_free_cells = 0
first_move = True


class Entry_number(Entry):
    """
    A class that was used in the Main Menu in order to make Entry Boxes
    that don't accept invalid inputs (other characters other than digits).
    """
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

"""
The main scope was used to initialize all the widgets and to place them
inside frames to be easier to access later on.

The widgets are aligned in a grid.  The tkinter class Frame was used in
order to align multiple elements.  When the screen is resized, the widgets
will change their position accordingly.
"""

root = Tk()
root.geometry("600x600")
root.title("Minesweeper")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

image_face_happy = PhotoImage(file="./textures/face_happy.png")
image_face_happy = image_face_happy.zoom(20)
image_face_happy = image_face_happy.subsample(32)
image_face_dead = PhotoImage(file="./textures/face_dead.png")
image_face_dead = image_face_dead.zoom(10)
image_face_dead = image_face_dead.subsample(32)
image_unpressed = PhotoImage(file="./textures/unpressed.png")
image_pressed = PhotoImage(file="./textures/pressed.png")
image_numbers = [
    PhotoImage(file="./textures/1.png"),
    PhotoImage(file="./textures/2.png"),
    PhotoImage(file="./textures/3.png"),
    PhotoImage(file="./textures/4.png"),
    PhotoImage(file="./textures/5.png"),
    PhotoImage(file="./textures/6.png"),
    PhotoImage(file="./textures/7.png"),
    PhotoImage(file="./textures/8.png"),
]
image_flag = PhotoImage(file="./textures/flag.png")
image_bombpressed = PhotoImage(file="./textures/bombpressed.png")
image_bombred = PhotoImage(file="./textures/bombred.png")
image_bombx = PhotoImage(file="./textures/bombx.png")
image_win_button = PhotoImage(file="./textures/win_button.png")
image_lose_button = PhotoImage(file="./textures/lose_button.png")

main_menu_frame = Frame(root)
main_menu_frame.grid(row=0, column=0, sticky='news')
main_menu_frame.columnconfigure(0, weight=1)
main_menu_frame.rowconfigure(0, weight=1)
main_menu_frame.rowconfigure(1, weight=1)

game_name_frame = Frame(main_menu_frame)
game_name_frame.grid(row=0, column=0, sticky='news')
game_name_frame.columnconfigure(0, weight=1)

game_name_label = Label(game_name_frame, text="Minesweeper")
game_name_label.grid(row=0, padx=20, pady=10, column=0)
game_name_label.config(font=("Courier", 30))

menu_image = Label(game_name_frame, image=image_face_happy)
menu_image.grid(row=1, column=0)

game_options_frame = Frame(main_menu_frame)
game_options_frame.grid(row=1, column=0, sticky='n')

group_options1_frame = Frame(game_options_frame)
group_options1_frame.grid(row=0, column=0)
group_options2_frame = Frame(game_options_frame)
group_options2_frame.grid(row=0, column=1)

table_size_label = Label(group_options1_frame, text="Table size:")
table_size_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
table_size_label.config(font=("Arial", 15))

table_size_entry_height = Entry_number(group_options2_frame,
                                       font="Arial 15", width="3")
table_size_entry_height.grid(row=0, column=0, padx=10, pady=10)

table_size_x_label = Label(group_options2_frame, text="X")
table_size_x_label.grid(row=0, column=1, pady=10)
table_size_x_label.config(font=("Arial", 15))

table_size_entry_width = Entry_number(group_options2_frame,
                                      font="Arial 15", width="3")
table_size_entry_width.grid(row=0, column=2, padx=10, pady=10)

time_limit_label = Label(group_options1_frame, text="Time Limit:")
time_limit_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
time_limit_label.config(font=("Arial", 15))

time_limit_entry = Entry_number(group_options2_frame,
                                font="Arial 15", width="3")
time_limit_entry.grid(row=1, column=0, padx=10, pady=10)

nr_bombs_label = Label(group_options1_frame, text="Bombs:")
nr_bombs_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
nr_bombs_label.config(font=("Arial", 15))

nr_bombs_entry = Entry_number(group_options2_frame,
                              font="Arial 15", width="3")
nr_bombs_entry.grid(row=2, column=0, padx=10, pady=10)

start_game_frame = Frame(game_options_frame)
start_game_frame.grid(row=1, column=0, columnspan=2, sticky="we")
start_game_frame.columnconfigure(0, weight=1)
start_game_frame.rowconfigure(0, weight=1)


def mainMenu(itself):
    """
    A function that gets called in order to return to the main
    menu.

    The Main Menu Frame is kept in memory and readded once the
    user clicks the Main Menu Button.
    """
    itself.grid_forget()
    root.geometry("600x600")
    main_menu_frame.grid(row=0, column=0, sticky='news')


def startGame():
    """
    The function that is called when the user click the Start Game button.

    When the user starts a game, firstly the program will check if the given
    inputs are valid.  Otherwise an error message will be shown using the
    "messagebox" class from tkinter.

    If all the inputs are valid, the game will generate a matrix where it will
    place the bombs.  First all the grid positions will be added to a list then
    the program iterate over that list, picking a random position then removing
    that coordinates from the list.  This method was used in order to eliminate
    the posibility that two bombs can be placed in the same position.

    Then the program will create a grid of buttons representing the cells, then
    add left click and right click events, aswell as images, to it.
    """
    if table_size_entry_height.get() == ""\
            and table_size_entry_width.get() != "":

            messagebox.showerror("Error", "Height has to be filled")
    elif table_size_entry_height.get() != ""\
            and table_size_entry_width.get() == "":

            messagebox.showerror("Error", "Width has to be filled")
    elif table_size_entry_height.get() != ""\
            and int(table_size_entry_height.get()) == 0:

            messagebox.showerror("Error", "Height has to be positive")
    elif table_size_entry_width.get() != ""\
            and int(table_size_entry_width.get()) == 0:

            messagebox.showerror("Error", "Width has to be positive")
    elif table_size_entry_height.get() == ""\
            and table_size_entry_width.get() == ""\
            and nr_bombs_entry.get() != ""\
            and int(nr_bombs_entry.get()) > 10 * 10 - 1:

            messagebox.showerror("Error", "Nr of bombs exceeds table size")
    elif table_size_entry_height.get() != ""\
            and table_size_entry_width.get() != ""\
            and nr_bombs_entry.get() != ""\
            and int(nr_bombs_entry.get()) >\
            int(table_size_entry_height.get()) *\
            int(table_size_entry_width.get()) - 1:

            messagebox.showerror("Error", "Nr of bombs exceeds table size")
    elif table_size_entry_height.get() != ""\
            and table_size_entry_width.get() != ""\
            and nr_bombs_entry.get() == ""\
            and 10 > int(table_size_entry_height.get()) *\
            int(table_size_entry_width.get()) - 1:

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
        global first_move
        first_move = True
        stop_event = False
        time_limit = 60
        if table_size_entry_height.get() != ""\
                and table_size_entry_width.get() != "":

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

        bomb_matrix = [[0 for i in range(table_width)]
                       for y in range(table_height)]
        flag_matrix = [[0 for i in range(table_width)]
                       for y in range(table_height)]
        for i in range(nr_bombs):
            r = random.randint(0, len(available_positions) - 1)
            bomb_matrix[
                         available_positions[r][0]
                       ][available_positions[r][1]] = 1
            del available_positions[r]

        root.geometry("")
        main_game_frame = Frame(root)
        main_game_frame.grid(row=0, column=0, sticky='news')
        main_game_frame.rowconfigure(0, weight=1)
        main_game_frame.rowconfigure(1, weight=1)
        main_game_frame.columnconfigure(0, weight=1)

        top_frame = Frame(main_game_frame)
        top_frame.grid(row=0, column=0, sticky='n')

        time_limit_label = Label(top_frame, font="Arial 20",
                                 text='Time: {:02}:{:02}'.format(
                                     time_limit % 3600//60, time_limit % 60
                                    ))
        time_limit_label.grid(row=0, column=0, pady=10)

        game_frame = Frame(main_game_frame)
        game_frame.grid(row=1, column=0, padx=20, pady=20, sticky='n')

        button_matrix = [[0 for i in range(table_width)]
                         for y in range(table_height)]

        def finalTable(x, y, reason):
            """
            The function that displays the final board after the game has
            ended.

            When the game has ended the program will display the final board.
            It verifies the buttons grid against the bomb matrix and the flag
            matrix in order to correcly place the images.  An additional
            button will be placed instead of the countdown timer to allow the
            user to return to the Main Menu.
            """
            global stop_event
            stop_event = True

            time_limit_label.grid_forget()
            reset_button = Button(top_frame)
            reset_button.grid(row=0, column=0, pady=14)
            reset_button['command'] = \
                lambda itself = main_game_frame: mainMenu(itself)

            if reason == 'lost' or reason == 'time':
                reset_button['image'] = image_lose_button
            elif reason == 'won':
                reset_button['image'] = image_win_button

            for i in range(table_height):
                for j in range(table_width):
                    button_matrix[i][j]['relief'] = 'sunken'
                    button_matrix[i][j]['command'] = 0
                    if bomb_matrix[i][j] == 1 and flag_matrix[i][j] == 1:
                        button_matrix[i][j]['image'] = image_bombx
                    elif bomb_matrix[i][j] == 1 and flag_matrix[i][j] == 0:
                        button_matrix[i][j]['image'] = image_bombpressed
            if bomb_matrix[x][y] == 1 and reason != 'time':
                button_matrix[x][y]['image'] = image_bombred

        def countdown():
            """
            The function for the daemon thread.

            In order to display the time, a daemon thread is launched that
            sleeps every one second and afterwards updates a global variable
            and the timer label.
            """
            global time_limit
            global stop_event
            while time_limit > 0 and not stop_event:
                time.sleep(1)
                time_limit -= 1
                time_limit_label['text'] = 'Time: {:02}:{:02}'.format(
                    time_limit % 3600//60, time_limit % 60)
            if not stop_event:
                finalTable(0, 0, 'time')

        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.daemon = True
        countdown_thread.start()

        def walk(x, y):
            """
            The function that walks the board recursively to reveal
            positions.

            To walk the board, first the program checks if the cell
            the player has clicked on contains a bomb.  If it does
            indeed contain a bomb, then the final board will be shown
            and the game will end.  An extra check will be performed
            to move the bomb in another cell if its the player's first
            move.  If the cell does not contain a bomb then the program
            will verify the number of neighbouring bombs.  If the number
            of bombs is higher than 0, then the recursive function will
            stop and only update the current position with the number of
            bombs.  If it is 0, then the recursive function will be
            called for every neighbour
            """
            global free_cells
            global first_move

            if bomb_matrix[x][y] == 1:
                if first_move:
                    bomb_matrix[x][y] = 0
                    r = random.randint(0, len(available_positions) - 1)
                    bomb_matrix[
                         available_positions[r][0]
                       ][available_positions[r][1]] = 1
                    walk(x, y)
                else:
                    finalTable(x, y, 'lost')
            elif button_matrix[x][y]['relief'] != 'sunken'\
                    and flag_matrix[x][y] == 0:

                free_cells += 1
                direct_x = [-1, -1, -1,  0, 0,  1, 1, 1]
                direct_y = [0, -1,  1, -1, 1, -1, 0, 1]
                nr_bombs = 0
                for i in range(len(direct_x)):
                    if x + direct_x[i] < table_height\
                            and x + direct_x[i] >= 0\
                            and y + direct_y[i] < table_width\
                            and y + direct_y[i] >= 0:

                        if bomb_matrix[x + direct_x[i]][y + direct_y[i]] == 1:
                            nr_bombs += 1

                if nr_bombs == 0:
                    button_matrix[x][y]['command'] = 0
                    button_matrix[x][y]['relief'] = 'sunken'
                    button_matrix[x][y]['image'] = image_pressed
                    for i in range(len(direct_x)):
                        if x + direct_x[i] < table_height\
                                and x + direct_x[i] >= 0\
                                and y + direct_y[i] < table_width\
                                and y + direct_y[i] >= 0:
                            walk(x + direct_x[i], y + direct_y[i])
                else:
                    button_matrix[x][y]['command'] = 0
                    button_matrix[x][y]['relief'] = 'sunken'
                    button_matrix[x][y]['image'] = image_numbers[nr_bombs - 1]

        def click(button):
            """
            The function that gets called when the user left clicks on a
            button.

            When the left clicks a button, it will trigger the left click
            event that will call a function to recursively walk the board
            in order to expand cells.  After every walk the program checks
            the number of discovered cells in order to see if the user has
            won.
            """
            global free_cells
            global total_free_cells
            global first_move
            x = button.grid_info()['row']
            y = button.grid_info()['column']
            walk(x, y)
            first_move = False
            if free_cells == total_free_cells and total_free_cells != 0:
                finalTable(x, y, 'won')

        def right_click(event):
            """
            The function that gets called when the user right clicks on
            a button.

            When the user right clicks a button, that cell will be marked
            with a flag. If a flag is already present, it will be removed.
            Flags stop the propagation of the walk function on that
            respective cell.
            """
            x = event.widget.grid_info()['row']
            y = event.widget.grid_info()['column']

            if button_matrix[x][y]['relief'] != 'sunken':
                if flag_matrix[x][y] == 1:
                    flag_matrix[x][y] = 0
                    button_matrix[x][y]['image'] = image_unpressed
                    button_matrix[x][y]['command'] = \
                        lambda button = button_matrix[x][y]: click(button)
                else:
                    flag_matrix[x][y] = 1
                    button_matrix[x][y]['image'] = image_flag
                    button_matrix[x][y]['command'] = 0

        for i in range(table_height):
            for j in range(table_width):
                button_matrix[i][j] = Button(game_frame,
                                             image=image_unpressed)
                button_matrix[i][j]['command'] =\
                    lambda button = button_matrix[i][j]: click(button)
                button_matrix[i][j].bind("<Button-2>", right_click)
                button_matrix[i][j].bind("<Button-3>", right_click)
                button_matrix[i][j].grid(row=i, column=j)

start_game_button = Button(start_game_frame, text="Start",
                           font="Arial 15", command=startGame)
start_game_button.grid(row=2, column=0, padx=10, pady=10, sticky="we")

root.mainloop()
