import scrap_engine as se
import time, os, threading, sys
import pynput
from pynput import keyboard
import random

os.system("")
width, height = os.get_terminal_size()
t=ev=v=0
g=0.015

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

frame = se.Frame(height-2, width-1, 
                 corner_chars=["+", "+", "+", "+"], 
                 horizontal_chars=["-", "-"], 
                 vertical_chars=["|", "|"], state="solid")
text=se.Text(f'Width: {width}\nHeight: {height}', float)


# Player design data
from player_design import PLAYER_DESIGN  # Import player design data

def create_player(map, start_x=5, start_y=5):
    player_parts = []
    for char, rel_x, rel_y in PLAYER_DESIGN:
        obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
    player_parts.append(obj)
    return player_parts

# Create the player at the specified position
create_player(map, 5, 5)  # Creates entire drill at (5,5)

# Rock design data
from rock_design import ROCK_DESIGN  # Import rock design data

def create_rock(map, start_x=25, start_y=5):
    rock_parts = []
    for char, rel_x, rel_y in ROCK_DESIGN:
        if char != ' ':  # Skip empty spaces
            obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
            rock_parts.append(obj)
    return rock_parts

# Usage:
boulder = create_rock(map, 25, 3)  # Creates rock at (10,3)

frame.add(map, 1,0)
text.add(map,10,3)

smap.show(init=True)
smap.set(smap.x+1, smap.y)

# Initialize direction variable
direction = 1  # X direction changer
y_change = 1

while True:
    '''# Check if the player touches the frame side boundaries
    if player.x >= frame.width -1:  # Right boundary
        direction = -1  # Move left
    elif player.x <= 2:  # Left boundary
        direction = 1  # Move right

    # Check if the player touches the frame upper/lower boundaries
    if player.y <= 2:  # Right boundary
        y_change = 1  # Move left
    elif player.y >= frame.height -3:  # Left boundary
        y_change = -1  # Move right
    
    # Move the player in the current direction
    player.set(player.x+1 * direction, player.y+1 * y_change)'''

    # Update and display the map
    smap.remap()
    smap.show()

    # Add a small delay to control the speed of movement
    time.sleep(0.03)
