import scrap_engine as se
import time, os, threading, sys
import random

os.system("")
width, height = os.get_terminal_size()
t=ev=v=0
g=0.015

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

block=se.Object("#")
ground=se.Square("#", map.width, 5)
player=se.Object(f'O')
frame = se.Frame(height-1, width-5, 
                 corner_chars=["+", "+", "+", "+"], 
                 horizontal_chars=["-", "-"], 
                 vertical_chars=["|", "|"], state="solid")
h=se.Text(f'Width: {width}\nHeight: {height}', float)

player.add(map, round(smap.width/2), round(map.height/2))
frame.add(map, 1,0)
h.add(map,10,3)



#smap.remap()
smap.show(init=True)
smap.set(smap.x+1, smap.y)

# Initialize direction variable
direction = 1  # X direction changer
y_change = 1

while True:
    # Check if the player touches the frame side boundaries
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
    player.set(player.x+1 * direction, player.y+1 * y_change)

    # Update and display the map
    smap.remap()
    smap.show()

    # Add a small delay to control the speed of movement
    time.sleep(0.03)
