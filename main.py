import scrap_engine as se
import time, os, threading, sys
from pynput import keyboard

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

#Rersources
iron = -1

# Create text
text=se.Text(f'Iron: {iron}', float)
text.add(map,3,1)

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



# Global control variable
running = True

#Resource IRON updater
def iron_counter():
    global iron
    iron_cd = 1
    while running:
        iron += 1
        text.rechar(f"Iron: {iron}")
        smap.remap()
        smap.show()
        time.sleep(iron_cd)  # Update every 1 second

iron_thread = threading.Thread(target=iron_counter, daemon=True)
iron_thread.start()

#Drill animation
def drill_animation():
    drill_state = '►'
    while running:
        drill_state = ' ' if drill_state == '►' else '►'  # Toggle drill state
        drill.rechar(drill_state)  # Update the drill object with the new state
        time.sleep(0.1)
        # Update and display the map
        smap.remap()
        smap.show()

drill_animation_thread = threading.Thread(target=drill_animation, daemon=True)
drill_animation_thread.start()

try:
    while running:  # Main game loop
        smap.remap()
        smap.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    running = False  # Signal threads to stop
    iron_thread.join(timeout=0.5)  # Wait for threads to finish
    drill_animation_thread.join(timeout=0.5)

