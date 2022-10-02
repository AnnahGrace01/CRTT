import tkinter as tk
import random

### Experiment Configuration ###################################################
# Customise variables and text messages here, for ease of use.
################################################################################
# Number of rounds to play
NUM_ROUNDS = 3

# Maximum number of seconds to wait during game
MAX_WAIT = 8

# Minimum number of seconds to wait during game
MIN_WAIT = 1

# Time to wait after the blast (in seconds)
BLAST_TIME_DELAY = 4

# Set the keys for each player
KEY1 = "Shift_L"
KEY2 = "Shift_R"

# Window Dimensions
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300

# Set font details
FONT_TYPE = "Times New Roman"
FONT_SIZE = 15
FONT_COLOUR = "white"
BG_COLOUR = "black"

### Text Strings ###############################################################
# Configurable text strings to be used during the experiment.
# '{}' characters can be replaced dynamically using the .format() function.
# NOTE: Editing any strings with '{}' in them MAY REQUIRE editing the .format()
# 		function where they are implemented (You can use CTRL+F to find them).
################################################################################

text_welcome = "Welcome!"
text_space_continue = "Press Space to continue..."
text_p1_name = "Player 1, type name then hit Enter:"
text_p2_name = "Player 2, type name then hit Enter:"

text_keys = "{} is using the '{}' key.\n{} is using the '{}' key."
text_instructions = "When you see GO!!, hit your key before your opponent."

text_round = "Round {}"

text_get_ready = "Ready..."
text_get_set = "Set..."
text_go = "GO!!"

text_win = "{} wins!\n\n{}, what blast level do you want to deliver?\nSelect 1-10 then hit Enter:"
text_blast = "{} chose blast level {}\n\n{}, standby for blast..."

text_game_over = "Game Over\nThanks for playing!"

### Setting Up GUI #############################################################
# Set up the Tkinter GUI that the players will use.
################################################################################

root = tk.Tk()
root.title("Competitive Reaction Time Game")
root.configure(bg=BG_COLOUR)

# Set the window size

root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialise global variables
player_names = {}
win_num = None
game_round = 0
game_data = {}

display_text = tk.StringVar()
display_label = tk.Label(
                    root,
                    fg=FONT_COLOUR,
                    bg=BG_COLOUR,
                    justify="center",
                    textvariable=display_text,
                    font=(FONT_TYPE, FONT_SIZE)
                )

entry_label = tk.Entry(
                    root,
                    fg=FONT_COLOUR,
                    bg=BG_COLOUR,
                    insertbackground=FONT_COLOUR,
                    disabledbackground=BG_COLOUR,
                    justify="center",
                    borderwidth=0,
                    highlightthickness=0,
                    font=(FONT_TYPE, FONT_SIZE),
                    state="disabled"
                )

display_label.grid(row=1, column=1)
entry_label.grid(row=2, column=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

### Text Functions  ############################################################
# Manipulate the text of the Label object in the window
################################################################################

# Adds text to the window, after a new line
def update_text(*new_text):
	display_text.set("".join(new_text))

def bind_keypress(func):
	root.unbind("<Return>")
	root.unbind("<space>")
	root.bind("<KeyPress>", func)

def bind_return(func):
	root.unbind("<space>")
	root.unbind("<KeyPress>")
	root.bind("<Return>", func)

def bind_space(func):
	root.unbind("<Return>")
	root.unbind("<KeyPress>")
	root.bind("<space>", func)

def unbind_all():
	root.unbind("<Return>")
	root.unbind("<space>")
	root.unbind("<KeyPress>")

def allow_typing():
	entry_label.configure(state="normal")
	entry_label.focus_set()

def disable_typing():
	entry_label.configure(state="disabled")
	root.focus_set()

def clear_entry():
	entry_label.configure(state="normal")
	entry_label.delete(0, 'end')
	entry_label.configure(state="disabled")

### Stage Functions ############################################################
# These control the flow of the experiment
################################################################################

# Function that sets the key for player 1
def ask_player_1(e):
	update_text(text_p1_name)
	bind_return(set_player_1)
	allow_typing()

def set_player_1(e):
	global player_names
	disable_typing()
	player_names[1] = entry_label.get()
	clear_entry()
	ask_player_2()

def ask_player_2():
	update_text(text_p2_name)
	bind_return(set_player_2)
	allow_typing()

def set_player_2(e):
	global player_names
	disable_typing()
	player_names[2] = entry_label.get()
	clear_entry()
	initiate_game()


def initiate_game():
	update_text(text_keys.format(player_names[1], KEY1.upper(),
	                             player_names[2], KEY2.upper()),
				"\n\n",
				text_instructions,
				"\n\n",
				text_space_continue
				)
	bind_space(check_game)


def check_game(e=None):
	global game_round
	game_round += 1

	if game_round > NUM_ROUNDS:
		end_game()

	else:
		update_text(text_round.format(game_round),
		            "\n\n",
		            text_space_continue
		            )
		bind_space(start_round)

# Starts the game when the Space Bar is pressed.
def start_round(e):
	# Unbind <KeyPress> so that pressing a key won't do anything
	unbind_all()
	update_text(text_get_ready)

	# Print "Get Set..." after 1 second (1000ms)
	root.after(1000, update_text, text_get_set)

	# Call the 'start_timer' function after a randomised delay (in Milliseconds)
	random_delay = 1000 + random.randint(MIN_WAIT, MAX_WAIT)*1000
	root.after(random_delay, start_timer)

# Print GO text, and record pressed keys
def start_timer():
	update_text(text_go)
	bind_keypress(record_game)

# Check keypresses to see if one of them was a player.
# If yes, initiate final stage accordingly.
def record_game(e):
	global KEY1, KEY2, game_data, game_round, win_num

	if e.keysym not in (KEY1, KEY2):
		return
	elif e.keysym == KEY1:
		win_num = 1
	else:
		win_num = 2

	unbind_all()

	# Add a small delay after the key is pressed, so that users don't 
	# accidentally type in the blast text.
	root.after(200, ask_blast)

# Declare the winner, and get the level of the blast
def ask_blast():
	global win_num
	update_text(text_win.format(player_names[win_num], player_names[win_num]))
	allow_typing()
	bind_return(set_blast)

def set_blast(e):
	global game_data, game_round, win_num, player_names
	disable_typing()
	blast_level = entry_label.get()

	game_data[game_round] = {
		"winner": player_names[win_num],
		"blast_level": blast_level
	}

	game_data[game_round]["blast_level"] = blast_level

	win_name = player_names[win_num]
	lose_name = player_names[3 - win_num]

	update_text(text_blast.format(win_name, blast_level, lose_name))
	clear_entry()
	unbind_all()
	root.after(BLAST_TIME_DELAY*1000, check_game)

# Print end text and unbind KeyPress.
# ==> Add any post-game functionality here.
def end_game():
	global game_data
	update_text(text_game_over)
	# Print the details of each round to the terminal.
	# Can replace with writing to file.
	print(game_data)

### Start Program ##############################################################
# Run calls to set the script running 
################################################################################
update_text(text_welcome,
            "\n\n",
            text_space_continue)
bind_space(ask_player_1)
root.mainloop()