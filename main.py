import scrap_engine as se
import time, os, threading, sys
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

os.system("")
width, height = os.get_terminal_size()

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

running = True

#GLOBAL VARIABLES----------------------------------------------------------------
#Rock status
damage = 0
damage_lock = Lock()
hp = 1000
hp_lock = Lock()

#Drill
drill_power = 1 #Drill power
drill_power_price = 10
drill_power_price_increase = 10

#Rersources
iron = int(0)
iron_lock = Lock()

gold = int(0)
gold_lock = Lock()

store_can_open = False #Opens once 1st gold is aquired
store_open = False #Store UI check

auto_miner = False #Auto miner
auto_miner_price = 1
auto_miner_price_increase = 10
auto_miner_thread = None
#--------------------------------------------------------------------------------

# Create a frame with the specified height and width
frame = se.Frame(height-2, width-1, 
                 corner_chars=["+", "+", "+", "+"], 
                 horizontal_chars=["-", "-"], 
                 vertical_chars=["|", "|"], state="solid")
frame.add(map, 1,0)

#Create frame for Store UI elements
menu_ui = se.Frame(6,40,
                 corner_chars=["╭", "╮", "╰", "╯"], 
                 horizontal_chars=["─", "─"], 
                 vertical_chars=["│", "│"], state="float")
center_y = int(frame.height / 2)

#Store text elements
store_text = se.Text("___Store___", "float")
close_store_text = se.Text("[E]xit store", float)
auto_mine = se.Text("[A]uto-mine", float)
auto_mine_price = se.Text(f"{auto_miner_price} Gold", float) #Price of auto-mine
better_drill = se.Text("[B]etter drill", float)
better_drill_price = se.Text(f"{drill_power_price} Gold", float) #Price of better drill

#Create UI box that will contain all Store UI elements
ui_box = se.Box(menu_ui.width, menu_ui.height)
ui_box.add_ob(menu_ui, 0,0)
ui_box.add_ob(store_text, (int(menu_ui.width/2)) -len(store_text.text)+5, 1)
ui_box.add_ob(close_store_text, menu_ui.width - len(close_store_text.text) -3, menu_ui.height-1)
ui_box.add_ob(auto_mine, 1, 2)
ui_box.add_ob(auto_mine_price, menu_ui.width - len(auto_mine_price.text)-2, 2)
ui_box.add_ob(better_drill, 1, 3)
ui_box.add_ob(better_drill_price, menu_ui.width - len(better_drill_price.text)-1, 3)

ui_center_x = int((width/2)-(menu_ui.width/2))
ui_center_y = int((height/2)-(menu_ui.height/2))

#UI render function
def ui_render():
    menu_ui.add(map, int(width/2)-200,int(height/2)+4)
    smap.remap()

# Create text
tutorial_state = f'{">   Press SPACEBAR to mine the boulder   <":^{frame.width+2}}' #Tutorial text
tutorial=se.Text(tutorial_state, float)
tutorial.add(map, 0, center_y-1) # Add tutorial text to the map

command_bottom = '' # Initialize command list
commands = se.Text(command_bottom, float)

iron_text=se.Text(f'Iron: {int(iron)}', float) # Create a text object to display iron count
gold_text=se.Text(f'', float) # Create a text object to display gold count

# Player design data
from player_design import PLAYER_DESIGN  # Import player design data

def create_player(map, start_x=4, start_y=5):
    for char, rel_x, rel_y in PLAYER_DESIGN:
        se.Object(char).add(map, start_x + rel_x, start_y + rel_y)

# Rock design data
from rock_design import ROCK_DESIGN  # Import rock design data

def create_rock(map, start_x=24, start_y=5):
    rock_parts = []
    for char, rel_x, rel_y in ROCK_DESIGN:
        if char != ' ':  # Skip empty spaces
            obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
            rock_parts.append(obj)
    return rock_parts

#HP bar objects
#filled = '■'
#empty = '□'
hp_bar = se.Text(f'[■■■■■■■■■■]', float)
#hp_bar.add(map, int(width-len(hp_bar.text)-1),height-8)

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


#Resource IRON updater automically
def iron_counter():
    global iron, damage, damage_lock, hp, hp_lock
    iron_cd = 1
    while running:
        with iron_lock:
            iron += 1
            iron_text.rechar(f"Iron: {iron}")
        with damage_lock:
            damage += 1
        with hp_lock:
            hp -= 1
        smap.remap()
        smap.show()
        time.sleep(iron_cd)  # Update every 1 second'''

# Keyboard control
space_pressed = False
def on_press(key):
    global iron, gold, space_pressed, drill_state, hp, hp_lock, damage, damage_lock, tutorial_state,command_bottom, store_can_open, store_open, auto_miner, drill_power, ui_center_x, ui_center_y
    from command_list import command_list, spacer
    if key == Key.space and not space_pressed:
        space_pressed = True
        with damage_lock:
            damage += drill_power
        with hp_lock:
            hp -= drill_power
        if iron == 0:
            iron_text.add(map,3,1)
            commands.add(map, 1,frame.height)
            if command_bottom == '':
                command_bottom += command_list[0] + spacer
                commands.rechar(command_bottom)
        
        #Event: Enough tutorial text
        if iron >18:
            tutorial.remove()
        
        with iron_lock:
            iron += drill_power
            iron_text.rechar(f'Iron: {int(iron)}')
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
    if iron >= 50:
        gold_text.add(map, iron_text.x, iron_text.y+1)
        if command_bottom == command_list[0] + spacer:
            command_bottom += command_list[1] + spacer
            commands.rechar(command_bottom)
        smap.remap()
        smap.show()

    if key == KeyCode(char='s') and iron >= 50:
        with iron_lock:
            if iron >= 50:
                iron -= 50
                with gold_lock:
                    gold += 1
                    store_can_open = True #Allows store to open
                    if command_bottom == command_list[0] + spacer + command_list[1] + spacer: #rewrite later
                        command_bottom += command_list[2] + spacer
                        commands.rechar(command_bottom)
                # Update the display of iron and gold
                iron_text.rechar(f'Iron: {int(iron)}')
                gold_text.rechar(f'Gold: {gold}')
                smap.remap()
                smap.show()
    
    #Opens and closes Store
    if key == KeyCode(char='e') and store_can_open == True: 
        if store_open == False:
            ui_box.add(map, ui_center_x, ui_center_y)
            store_open = True

        elif store_open == True:
            store_open = False
            ui_box.remove()
    
    #Store actions
    if key == KeyCode(char='a') and store_open == True:
        global auto_miner_price, auto_miner_price_increase, drill_power_price, drill_power_price_increase
        if gold >= auto_miner_price:
            with gold_lock:
                gold -= 1
            auto_miner = True
            auto_miner_price = auto_miner_price * auto_miner_price_increase
            gold_text.rechar(f'Gold: {gold}')
            auto_mine.rechar(f"[A]uto-mine (Purchased)")
            auto_mine_price.rechar(f"{auto_miner_price} Gold")
            smap.remap()
            smap.show()
            # Start the thread only if it's not already running
            global auto_miner_thread
            if auto_miner_thread is None or not auto_miner_thread.is_alive():
                auto_miner_thread = threading.Thread(target=iron_counter, daemon=True)
                auto_miner_thread.start()
    
    if key == KeyCode(char='b') and store_open == True:
        if gold >= 1:
            with gold_lock:
                gold -= 1
                drill_power += 1
            better_drill.rechar("[B]etter drill (Purchased)")
            # Update the display of gold
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

'''def hp_animation():
    global hp, damage,running
    hp_state = f'[■■■■■■■■■□]'
    hp_bar.add(map, int(width-len(hp_bar.text)-1),height-8)
    while running:
        #if hp <= 800 and hp >700:
        hp_state = f'[■■■■■■■■■□]' if hp_state == '[■■■■■■■■□□]' else '[■■■■■■■■■□]'
        hp_bar.rechar(hp_state)
        time.sleep(2)
        smap.remap()
        smap.show()'''
def hp_animation():
    global hp, damage, running
    hp_state = '[■■■■■■■■■■]'  # Initial state (full HP)
    hp_bar.add(map, int(width-len(hp_bar.text)-1), height-8)
    while running:
        if hp <= 950:
            hp_state = '[■■■■■■■■■□]' if hp_state == '[■■■■■■■■■■]' else '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        else:
            hp_state = '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        time.sleep(0.5)  # Same timing as your drill animation
        smap.remap()
        smap.show()

hp_animation_thread = threading.Thread(target=hp_animation, daemon=True)

#DEBUB
dmg = se.Text(f"Dmg: {damage}")
dmg.add(map, 30, 2)
hpp = se.Text(f"HP: {hp}")
hpp.add(map, 30, 3)


# Main game loop
try:
    while running:
        #ui_render() #Uncomment this once implementation is done
        with damage_lock:
            dmg.rechar(f"Dmg: {damage}")
        with hp_lock:
            hpp.rechar(f"HP: {hp}")
        if hp <= 950 and hp_animation_thread.is_alive() == False:
            hp_animation_thread.start()
        
        smap.remap()
        smap.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    running = False
    #listener.stop()
