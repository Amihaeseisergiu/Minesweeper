PEP: 9999
Title: Minesweeper - Documentation
Author: Amihaesei Sergiu <amihaeseisergiu@gmail.com>
Status: Draft
Type: Informational
Content-Type: text/x-rst
Created: 29-Nov-2020
Post-History:


Abstract
========

This PEP contains the documentation for the project "Minesweeper", including
all the implementation details.


Rationale
=========

For the interaction with the user, the GUI library "tkinter" was used.
Aditionally, the "messagebox" class was imported from tkinter in order
to show error messages.

The other libraries that were used are decribed as follows:

* Time : for the sleep function in order to create a countdown timer.

* Threading : to create and launch a daemon thread for the timer.

* Random : to generate random numbers in order to place the bombs.


Application Arhitecture
=======================

Main Menu
---------

When the user first launches the application the Main Menu will be displayed.
Here he can customize the different aspects of the game:

* Table size : the first Entry Box represents the number of rows that
  the Game Grid will have, while the second Entry Box represents the number
  of columns.
  
* Time limit : the time limit (in seconds) in which the user needs to solve
  the board.
  
* Bombs : the number of bombs that the Table will include.

If a field is left empty, then the respective modifier will take a default
value as follows:

* Table size : the default will be a grid with 10 rows and 10 columns.

* Time limit : the time limit will be 60 seconds.

* Bombs : the number of bombs will be 10.

After choosing some modifiers the user can start the Game by pressing the
"Start" button.  Before starting the Game every field is tested so that it
has a valid value and will display an error message accordingly:

* Table size : if the row field is filled, the column field has to be filled
  aswell, and vice-versa.

* Bombs : the number of bombs is not allowed to surpass the number of
  cells in the Grid minus one position (to allow the first move of the
  player to not contain a bomb).
  
The Entry Boxes don't accept other characters besides digits.


Game Screen
-----------

At the top of the screen there is an auto updating text that will show the
user the remaining time he has available to solve the board.

Below lays the Grid, where the user can perform the following actions:

* Left click : will discover that particular cell.  If there are bombs around
  then the cell will show the number of bombs in its vicinity.  Otherwise it
  expand and check the nearby cells recursively.  If there is a bomb in that
  cell, the Game will end.  The first left click the user performs will never
  open into a bomb.
  
* Right click : to place and remove flags.  A flag is an assumption that in
  that cell there is a bomb.  It will stop the expansions of the cells if
  they want to discover a flagged cell.  Another right click on a flagged
  cell will remove the flag.
  
If the user clicks on a bomb or he visited all the cells the Game will end 
and will display the final board. The board legend is the following:

* Red bomb : the cell in which the player clicked.

* Crossed bomb : a flagged bomb.

* Normal bomb : the position of an undiscovered bomb.

* The rest of the board remain unchanged.

When the game ended another button will appear in place of the countdown
timer. By pressing it, the user can return to the Main Menu.


Implementation Details
======================

Main Menu
---------

In the Main Menu screen a class was created in order to make Entry Boxes
that don't accept invalid inputs (other characters other than digits).

::
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

The widgets are aligned in a grid.  The tkinter class "Frame" was used in 
order to align multiple elements.  When the screen is resized, the widgets
will change their position accordingly.


Game Screen
-----------

When the user starts a game, firstly the program will check if the given
inputs are valid.  Otherwise an error message will be shown using the
"messagebox" class from tkinter:

::
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
			
If all the inputs are valid, the game will generate a matrix where it will
place the bombs.  First all the grid positions will be added to a list then
the program iterate over that list, picking a random position then removing
that coordonates from the list.  This method was used in order to eliminate
the posibility that two bombs can be placed in the same position:

::
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

Then the program will create a grid of buttons representing the cells, then
add left click and right click events, aswell as images, to it:

::
    for i in range(table_height):
        for j in range(table_width):
            button_matrix[i][j] = Button(game_frame,
                                        image=image_unpressed)
            button_matrix[i][j]['command'] =\
                lambda button = button_matrix[i][j]: click(button)
            button_matrix[i][j].bind("<Button-2>", right_click)
            button_matrix[i][j].bind("<Button-3>", right_click)
            button_matrix[i][j].grid(row=i, column=j)
			
When the left clicks a button, it will trigger the left click event that will
call a function to recursively walk the board in order to expand cells.
After every walk the program checks the number of discovered cells in order
to see if the user has won:

::
    def click(button):
        global free_cells
        global total_free_cells
        x = button.grid_info()['row']
        y = button.grid_info()['column']
        walk(x, y)
        if free_cells == total_free_cells and total_free_cells != 0:
            finalTable(x, y, 'won')
			
To walk the board, first the program checks if the cell the player has clicked
on contains a bomb.  If it does indeed contain a bomb, then the final board
will be shown and the game will end.  An extra check will be performed to move
the bomb in another cell if its the player's first move.  If the cell does not
contain a bomb then the program will verify the number of neighbouring bombs.
If the number of bombs is higher than 0, then the recursive function will stop
and only update the current position with the number of bombs.  If it is 0,
then the recursive function will be called for every neighbour:

::
    def walk(x, y):
        global free_cells
        global first_move

        if bomb_matrix[x][y] == 1:
            if first_move:
                first_move = False
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

When the game has ended the program will display the final board.  It verifies
the buttons grid against the bomb matrix and the flag matrix in order to
correcly place the images.  An additional button will be placed instead of the
countdown timer to allow the user to return to the Main Menu:

::
    def finalTable(x, y, reason):
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

In order to display the time, a daemon thread is launched that sleeps every
one second and afterwards updates a global variable and the timer label:

::
    def countdown():
        global time_limit
        global stop_event
        while time_limit > 0 and not stop_event:
            time.sleep(1)
            time_limit -= 1
            time_limit_label['text'] = 'Time: {:02}:{:02}'.format(
                time_limit % 3600//60, time_limit % 60)
        if not stop_event:
            finalTable(0, 0, 'time')

Bibliography
============

.. [1] For the Entry Class, slightly modified
   (https://bit.ly/2VgCRN2)


Copyright
=========

This document is placed in the public domain or under the
CC0-1.0-Universal license, whichever is more permissive.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End: