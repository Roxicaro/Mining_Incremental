import scrap_engine as se
import time, os, threading, sys
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

os.system("")
width, height = os.get_terminal_size()

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

# Create a frame with the specified height and width
frame = se.Frame(height-2, width-1, 
                 corner_chars=["+", "+", "+", "+"], 
                 horizontal_chars=["-", "-"], 
                 vertical_chars=["|", "|"], state="solid")
frame.add(map, 1,0)

#GLOBAL VARIABLES----------------------------------------------------------------
#Rersources
iron = int(0)
iron_lock = Lock()

allow_sell = False # Allow selling of resources
gold = int(0)
gold_lock = Lock()

center_y = int(frame.height / 2)
#--------------------------------------------------------------------------------

# Create text
tutorial_state = f'{">   Press SPACEBAR to mine the boulder   <":^{frame.width+2}}' #Tutorial text
tutorial=se.Text(tutorial_state, float)
tutorial.add(map, 0, center_y-1) # Add tutorial text to the map

command_bottom = '' # Initialize command list
commands = se.Text(command_bottom, float)

iron_text=se.Text(f'Iron: {iron}', float) # Create a text object to display iron count
gold_text=se.Text(f'Gold: {gold}', float) # Create a text object to display gold count

# Player design data
from player_design import PLAYER_DESIGN  # Import player design data

def create_player(map, start_x=5, start_y=5):
    for char, rel_x, rel_y in PLAYER_DESIGN:
        se.Object(char).add(map, start_x + rel_x, start_y + rel_y)

# Rock design data
from rock_design import ROCK_DESIGN  # Import rock design data

def create_rock(map, start_x=25, start_y=5):
    rock_parts = []
    for char, rel_x, rel_y in ROCK_DESIGN:
        if char != ' ':  # Skip empty spaces
            obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
            rock_parts.append(obj)
    return rock_parts

# Create the player at the specified position
create_player(map, frame.width-16, frame.height-4)  # Creates entire drill at (5,5)

# Create and place drill
drill_state = '►'  # Initial state of the drill
drill = se.Object(drill_state)
drill.add(map, frame.width-12, frame.height-3)

# Place the rock at the specified position:
rock = create_rock(map, frame.width-10, frame.height-5)  # Creates rock at (10,3)

smap.show(init=True)
smap.set(smap.x+1, smap.y)

# Initialize direction variable
direction = 1  # X direction changer
y_change = 1

#EVENTS------------------------------------------------------------------
##Check if the player has enough iron to sell for the first time (50 iron)  

# Keyboard control
space_pressed = False
def on_press(key):
    global iron, gold, space_pressed, drill_state, tutorial_state,command_bottom, allow_sell
    if key == Key.space and not space_pressed:
        space_pressed = True
        if iron >= 0:
            iron_text.add(map,3,1)
            from command_list import command_list, spacer
            commands.add(map, 1,frame.height)
            if command_bottom == '':
                command_bottom += command_list[0] + spacer
            commands.rechar(command_bottom)
        
        #Event: Enough tutorial text
        if iron >18:
            tutorial.remove()
        
        with iron_lock:
            iron += 1
        for _ in range(2):
            # Update the drill state to show it's working
            drill_state = ' ' if drill_state == '►' else '►'  # Toggle drill state
            drill.rechar(drill_state)  # Update the drill object with the new state
            tutorial_state = f'{">   Press SPACEBAR to mine the boulder   <":^{frame.width+2}}' if tutorial_state == ' ' else ' '
            tutorial.rechar(tutorial_state)
            smap.remap()
            smap.show()
            time.sleep(0.05)

    #Check if the player has enough iron to sell for the first time (50 iron)   
    if iron >= 50 and allow_sell == False:
        allow_sell = True
        gold_text.add(map, iron_text.x, iron_text.y+1)
        if command_bottom == command_list[0] + spacer:
            command_bottom += command_list[1] + spacer


    if key == KeyCode(char='s') and allow_sell == True:
        with iron_lock:
            if iron >= 50:
                iron -= 50
                with gold_lock:
                    gold += 1
                # Update the display of iron and gold
                iron_text.rechar(f'Iron: {iron}')
                gold_text.rechar(f'Gold: {gold}')
                smap.remap()
                smap.show()

def on_release(key):
    global space_pressed
    if key == Key.space:
        space_pressed = False


# Start keyboard listener in a daemon thread
def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

keyboard_thread = threading.Thread(target=start_listener, daemon=True)
keyboard_thread.start()

# Global control variable
running = True

#Resource IRON updater automically
'''def iron_counter():
    global iron
    iron_cd = 1
    while running:
        #iron += 1
        text.rechar(f"Iron: {iron}")
        smap.remap()
        smap.show()
        time.sleep(iron_cd)  # Update every 1 second'''

#iron_thread = threading.Thread(target=iron_counter, daemon=True)
#iron_thread.start()

#Drill animation automatic
'''def drill_animation():
    drill_state = '►'
    while running:
        drill_state = ' ' if drill_state == '►' else '►'  # Toggle drill state
        drill.rechar(drill_state)  # Update the drill object with the new state
        time.sleep(0.1)
        # Update and display the map
        smap.remap()
        smap.show()

drill_animation_thread = threading.Thread(target=drill_animation, daemon=True)
drill_animation_thread.start()'''

# Main game loop
running = True
try:
    while running:
        with iron_lock:
            iron_text.rechar(f'Iron: {int(iron)}')
        smap.remap()
        smap.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    running = False
    #listener.stop()