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
    player_parts = []
    for char, rel_x, rel_y in PLAYER_DESIGN:
        obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
        player_parts.append(obj)
    return player_parts

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
player_parts = create_player(map, frame.width-16, frame.height-4)  # Creates entire drill at (5,5)

# Place the rock at the specified position:
rock = create_rock(map, frame.width-10, frame.height-5)  # Creates rock at (10,3)

smap.show(init=True)
smap.set(smap.x+1, smap.y)

# Initialize direction variable
direction = 1  # X direction changer
y_change = 1


#Resource IRON updater and drill animation
iron_cd = 1
drill_state = '►'
while True:
    iron += 1  # Increment iron count
    text.rechar(f'Iron: {iron}')  # Update the text object with the new iron count

    # Update and display the map
    smap.remap()
    smap.show()
    # Add a small delay to control the speed of movement
    time.sleep(iron_cd)


