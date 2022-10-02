import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random

### Experiment Configuration ###################################################
# Customise variables and text messages here, for ease of use.
################################################################################
# Number of rounds to play
NUM_ROUNDS = 3

# Maximum number of seconds to wait during game
MAX_WAIT = 2

# Minimum number of seconds to wait during game
MIN_WAIT = 1

# Time to wait after the blast (in seconds)
BLAST_TIME_DELAY = 4

# Whether or not to use the 'set_round_text' function (see below)
CLEAR_TEXT_AFTER_ROUNDS = False

# Text strings to be used in the experiment.
# '{}' characters can be replaced dynamically using the .format() function.
text_welcome_message = "Welcome!"
text_p1_char = "Please press a button for Player 1..."
text_p2_char = "Please press a button for Player 2..."
text_p1_char_selected = 'Player 1 is using the "{}" key.'
text_p2_char_selected = 'Player 2 is using the "{}" key.'
text_round = "\nRound {}"
text_start_game = "Press the space bar when you are ready to start..."
text_get_ready = "Get ready..."
text_get_set = "Set..."
text_go = "GO!!"
text_win = "Player {} wins!"
text_blast = "Player {}, what blast level do you want to deliver? Select 1-10 then hit Enter:   "
text_blast_action = "Player {} chose blast level {}\nPlayer {}, stand by for blast..."
text_game_over = "\nGame Over\nThanks for playing!"

### Setting Up GUI #############################################################
# Set up the Tkinter GUI that the players will use.
################################################################################

root = tk.Tk()
root.title("Competitive Reaction Time Game")

# Set the window size
root.geometry("500x300")

# Initialise global variables
p1 = None
p2 = None
game_round = 0
game_data = {}

display_label = ScrolledText(
                    root,
                    fg="white",
                    bg="black",
                    font=("Times New Roman", 12), # Set the font here
                    state="disabled" # This prevents the users from typing anything.
                )

# Get the ScrolledText box to fit the Root window
display_label.pack(expand=True, fill='both')

### Text Functions  ############################################################
# Manipulate the text of the ScrolledText object in the window
################################################################################

# Adds text to the window, after a new line
def update_text(new_text):
	display_label.configure(state='normal')
	display_label.insert('end', new_text + "\n")
	display_label.configure(state='disabled')
	display_label.see('end')

# Clears all text from the window and resets it to show the keys of each user,
# and the Round number. Optional.
def clear_round_text():
	global game_round, p1, p2

	display_label.configure(state='normal')
	display_label.delete('1.0', 'end')
	
	update_text(text_p1_char_selected.format(p1))
	update_text(text_p2_char_selected.format(p2))


### Stage Functions ############################################################
# These control the flow of the experiment
################################################################################

# root.bind("<Return>", lambda x: update_text("Enter Pressed"))
# root.bind("<BackSpace>", lambda x: update_text("Backspace Pressed"))

# Function that sets the key for player 1
def set_player_1(e):
	global p1
	p1 = e.keysym
	update_text(text_p1_char_selected.format(p1))
	update_text(text_p2_char)
	root.bind("<KeyPress>", set_player_2)

# Function that sets the key for player 2
def set_player_2(e):
	global p2
	p2 = e.keysym
	update_text(text_p2_char_selected.format(p2))
	start_game()

# Starts a round if the round number is less than NUM_ROUNDS, else ends the game.
def start_game():
	global game_round
	game_round += 1

	if game_round > NUM_ROUNDS:
		end_game()
	else:
		if CLEAR_TEXT_AFTER_ROUNDS:
			clear_round_text()

		update_text(text_round.format(game_round))
		update_text(text_start_game)
		root.bind("<KeyPress>", play_game)

# Starts the game when the Space Bar is pressed.
def play_game(e):
	if e.char != " ":
		return
	# Unbind <KeyPress> so that pressing a key won't do anything
	root.unbind("<KeyPress>")
	update_text(text_get_ready)

	# Print "Get Set..." after 1 second (1000ms)
	root.after(1000, update_text, text_get_set)

	# Call the 'start_timer' function after a randomised delay (in Milliseconds)
	random_delay = 1000 + random.randint(MIN_WAIT, MAX_WAIT)*1000
	root.after(random_delay, start_timer)

# Print GO text, and record pressed keys
def start_timer():
	update_text(text_go)
	root.bind("<KeyPress>", record_game)

# Check keypresses to see if one of them was a player.
# If yes, initiate final stage accordingly.
def record_game(e):
	global p1, p2
	if e.keysym not in (p1, p2):
		return
	elif e.keysym == p1:
		aftermath(1)
	else:
		aftermath(2)

# Declare the winner, and get the level of the blast
def aftermath(winner):
	update_text(text_win.format(winner))
	update_text(text_blast.format(winner))

	def end_get_input_string(e):
		last_line = display_label.get("end-3c linestart", "end-2c")
		input_num = last_line.split(":")[-1].strip()
		root.after(50, create_blast, input_num, winner)
		display_label.configure(state="disabled")

	root.unbind("<KeyPress>")
	root.bind("<Return>", end_get_input_string)
	display_label.configure(state='normal')
	display_label.focus_set()

def create_blast(input_num, winner):
	global game_data, game_round
	game_data[game_round] = {
		"winner": winner,
		"blast_selected": input_num
	}

	if winner == 1:
		loser = 2
	else:
		loser = 1
	update_text(text_blast_action.format(winner, input_num, loser))
	root.after(BLAST_TIME_DELAY*1000, start_game)

# Print end text and unbind KeyPress.
# ==> Add any post-game functionality here.
def end_game():
	global game_data
	update_text(text_game_over)
	root.unbind("<KeyPress>")
	# Print the details of each round to the terminal.
	# Can replace with writing to file.
	print(game_data)

### Start Program ##############################################################
# Run calls to set the script running 
################################################################################
update_text(text_welcome_message)
update_text(text_p1_char)
root.bind("<KeyPress>", set_player_1)
root.mainloop()