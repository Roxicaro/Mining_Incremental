import scrap_engine as se
import time, os, threading, sys
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

#Implement Save Data
SAVE_FILE = "save.txt"

def save_game():
    """Saves game data to a simple text file"""
    with open(SAVE_FILE, 'w') as f:
        # Write all important variables in a specific order
        f.write(f"{iron}\n")
        f.write(f"{gold}\n")
        f.write(f"{rubble}\n")
        f.write(f"{drill_power}\n")
        f.write(f"{auto_miner}\n")
        f.write(f"{auto_mine_level}\n")
        f.write(f"{drill_power_price}\n")
        f.write(f"{auto_miner_price}\n")
        f.write(f"{hp}\n")
        f.write(f"{damage}\n")

def load_game():
    """Loads game data from the text file"""
    global iron, gold, rubble, drill_power, auto_miner
    global auto_mine_level, drill_power_price, auto_miner_price, hp, damage
    
    try:
        with open(SAVE_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) < 10:
                print("Save file corrupted")
                return False
                
            # Read values in the same order they were saved
            iron = int(lines[0].strip())
            gold = int(lines[1].strip())
            rubble = int(lines[2].strip())
            drill_power = int(lines[3].strip())
            auto_miner = lines[4].strip().lower() == 'true'
            auto_mine_level = int(lines[5].strip())
            drill_power_price = int(lines[6].strip())
            auto_miner_price = int(lines[7].strip())
            hp = int(lines[8].strip())
            damage = int(lines[9].strip())
            
            # Update UI
            iron_text.rechar(f'Iron: {iron}')
            gold_text.rechar(f'Gold: {gold}')
            rubble_text.rechar(f'Rubble: {rubble}')
            auto_mine.rechar(f"[A]uto-mine ({auto_mine_level})")
            auto_mine_price.rechar(f"{auto_miner_price} Gold")
            better_drill.rechar(f"[B]etter drill ({drill_power})")
            better_drill_price.rechar(f"{drill_power_price} Gold")

            return True
            
    except FileNotFoundError:
        print("No save file found")
    except Exception as e:
        print(f"Error loading: {e}")
    return False
############################

os.system("")
width, height = os.get_terminal_size()

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

running = True
load_game() ######################### NOT WORKING

#GLOBAL VARIABLES----------------------------------------------------------------
#Rock status
first_rock = True
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

rubble = 0
rubble_lock = Lock()

store_can_open = False #Opens once 1st gold is aquired
store_open = False #Store UI check

#Auto miner
auto_miner = False #Auto miner
auto_miner_price = 1
auto_miner_price_increase = 10
auto_miner_thread = None
auto_mine_cd = 1
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

#Exit game UI text
exit_text = se.Text("[Esc] Quit", float)
exit_text.add(map, frame.width - len(exit_text.text), frame.height)

#Store text elements
store_text = se.Text("___Store___", "float")
close_store_text = se.Text("[E]xit store", float)
auto_mine = se.Text("[A]uto-mine", float)
auto_mine_price = se.Text(f"{auto_miner_price} Gold", float) #Price of auto-mine
auto_mine_level = 0
better_drill = se.Text("[B]etter drill", float)
better_drill_price = se.Text(f"{drill_power_price} Gold", float) #Price of better drill
#drill level is tracked by the variable drill_power

#Create UI box that will contain all Store UI elements
ui_box = se.Box(menu_ui.width, menu_ui.height)
ui_box.add_ob(menu_ui, 0,0)
ui_box.add_ob(store_text, (int(menu_ui.width/2)) -len(store_text.text)+5, 1)
ui_box.add_ob(close_store_text, menu_ui.width - len(close_store_text.text) -3, menu_ui.height-1)
ui_box.add_ob(auto_mine, 1, 2)
ui_box.add_ob(auto_mine_price, menu_ui.width - len(auto_mine_price.text)-1, 2)
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
rubble_text=se.Text(f'', float)
rubble_text.add(map,3,3)

# Player design data
from player_design import PLAYER_DESIGN  # Import player design data

def create_player(map, start_x=4, start_y=5):
    for char, rel_x, rel_y in PLAYER_DESIGN:
        se.Object(char).add(map, start_x + rel_x, start_y + rel_y)

# Rock design data
from rock_design import ROCK_DESIGN  # Import rock design data
rock_parts = []  # List to store rock parts
def create_rock(map, start_x=24, start_y=5):
    global rock_parts
    for char, rel_x, rel_y in ROCK_DESIGN:
        obj = se.Object(char,float).add(map, start_x + rel_x, start_y + rel_y)
        rock_parts.append(obj)
    return rock_parts

#Mining-cart design data
from ascii_designs import mining_cart_design
def create_mining_cart(map, start_x=15, start_y=5):
    mining_cart_parts = []
    for char, rel_x, rel_y in mining_cart_design:
        obj = se.Object(char).add(map, start_x + rel_x, start_y + rel_y)
        mining_cart_parts.append(obj)
    return mining_cart_parts

#HP bar objects
'''
filled = '■'
#empty = '□' 
'''
hp_bar = se.Text(f'[■■■■■■■■■■]', float)

# Create the player at the specified position
create_player(map, frame.width-16, frame.height-4)  # Creates entire drill at (5,5)

# Create and place drill
drill_state = '►'  # Initial state of the drill
drill = se.Object(drill_state)
drill.add(map, frame.width-12, frame.height-3)

# Place the rock at the specified position:
create_rock(map, frame.width-10, frame.height-5)  # Creates rock at (10,3)

smap.show(init=True)
smap.set(smap.x+1, smap.y)

#Create mining-cart
#create_mining_cart(map, frame.width-25, frame.height-4)

# Initialize direction variable
direction = 1  # X direction changer
y_change = 1

#EVENTS------------------------------------------------------------------
##Check if the player has enough iron to sell for the first time (50 iron)  


#Resource IRON updater automically
def iron_counter():
    global iron, damage, damage_lock, hp, hp_lock, auto_mine_cd
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
        time.sleep(auto_mine_cd)  # Update every 1 second'''

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
                gold_text.rechar(f'Gold: {int(gold)}')
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
        global auto_miner_price, auto_miner_price_increase, drill_power_price, drill_power_price_increase, auto_mine_level, auto_mine_cd
        if gold >= auto_miner_price:
            with gold_lock:
                gold -= auto_miner_price
                gold_text.rechar(f'Gold: {int(gold)}')
            auto_miner = True
            auto_miner_price = auto_miner_price * auto_miner_price_increase
            auto_mine_level += 1
            auto_mine_cd /= (auto_mine_level * 2)
            auto_mine.rechar(f"[A]uto-mine ({auto_mine_level})")
            auto_mine_price.rechar(f"{auto_miner_price} Gold")
            ui_box.set_ob(auto_mine_price, menu_ui.width - len(auto_mine_price.text)-1, 2)
            smap.remap()
            smap.show()
            # Start the thread only if it's not already running
            global auto_miner_thread, drill_animation_thread
            if auto_miner_thread is None or not auto_miner_thread.is_alive():
                auto_miner_thread = threading.Thread(target=iron_counter, daemon=True)
                auto_miner_thread.start()
            if drill_animation_thread.is_alive() == False:
                drill_animation_thread.start()

    
    if key == KeyCode(char='b') and store_open == True:
        if gold >= drill_power_price:
            with gold_lock:
                gold -= drill_power_price
                gold_text.rechar(f'Gold: {int(gold)}')
                drill_power += 1
                drill_power_price = drill_power_price * drill_power_price_increase
            better_drill.rechar(f"[B]etter drill ({drill_power})")

            better_drill_price.rechar(f"{drill_power_price} Gold")
            ui_box.set_ob(better_drill_price, menu_ui.width - len(better_drill_price.text)-1, 3)
            smap.remap()
            smap.show()
    
    if key == KeyCode(char='1'):
        save_game()
    if key == KeyCode(char='2'):
        load_game()
    
    #Press Esc to quit game
    if key == Key.esc:
        global running
        save_game()
        running = False
        raise KeyboardInterrupt 
    
    #Debugging
    if key == KeyCode(char='w'):
        with iron_lock:
            iron += 10000
            iron_text.rechar(f'Iron: {int(iron)}')
        with gold_lock:
            gold += 10000
            gold_text.rechar(f'Gold: {gold}')

def on_release(key):
    global space_pressed
    if key == Key.space:
        space_pressed = False #This prevents the drill from being spammed when holding space


# Start keyboard listener in a daemon thread
def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

keyboard_thread = threading.Thread(target=start_listener, daemon=True)
keyboard_thread.start()

#Drill animation function
def drill_animation():
    drill_state = '►'
    while running:
        drill_state = ' ' if drill_state == '►' else '►'  # Toggle drill state
        drill.rechar(drill_state)  # Update the drill object with the new state
        time.sleep(0.1)
        # Update and display the map
        smap.remap()
        smap.show()

#HP animation function
def hp_animation():
    global hp, damage, running
    hp_state = '[■■■■■■■■■■]'  # Initial state (full HP)
    hp_bar.add(map, int(width-len(hp_bar.text)-1), height-8)
    while running:
        if hp <= 950 and hp >= 900:
            hp_state = '[■■■■■■■■■□]' if hp_state == '[■■■■■■■■■■]' else '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        elif hp < 900 and hp >= 800:
            hp_state = '[■■■■■■■■□□]' if hp_state == '[■■■■■■■■■□]' else '[■■■■■■■■■□]'
            hp_bar.rechar(hp_state)
        elif hp < 800 and hp >= 700:
            hp_state = '[■■■■■■■□□□]' if hp_state == '[■■■■■■■■□□]' else '[■■■■■■■■□□]'
            hp_bar.rechar(hp_state)
        elif hp < 700 and hp >= 600:
            hp_state = '[■■■■■■□□□□]' if hp_state == '[■■■■■■■□□□]' else '[■■■■■■■□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 600 and hp >= 500:
            hp_state = '[■■■■■□□□□□]' if hp_state == '[■■■■■■□□□□]' else '[■■■■■■□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 500 and hp >= 400:
            hp_state = '[■■■■□□□□□□]' if hp_state == '[■■■■■□□□□□]' else '[■■■■■□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 400 and hp >= 300:
            hp_state = '[■■■□□□□□□□]' if hp_state == '[■■■■□□□□□□]' else '[■■■■□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 300 and hp >= 200:
            hp_state = '[■■□□□□□□□□]' if hp_state == '[■■■□□□□□□□]' else '[■■■□□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 200 and hp >= 100:
            hp_state = '[■□□□□□□□□□]' if hp_state == '[■■□□□□□□□□]' else '[■■□□□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < 100 and hp >= 0:
            hp_state = '[□□□□□□□□□□]' if hp_state == '[■□□□□□□□□□]' else '[■□□□□□□□□□]'
            hp_bar.rechar(hp_state)        
        else:
            hp_state = '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        time.sleep(0.5)  # Same timing as your drill animation
        smap.remap()
        smap.show()

#Explosion animation function
boom_box = se.Square(char='#',width=9, height=4,state="float")

def explosion_animation():
    global hp, running, rock_parts, boom_box
    boom_box.add(map, frame.width-10, frame.height-5)
    explosion = se.Text('BOOM!', float)
    explosion.add(map, frame.width-8, frame.height-3)
    explosion.rechar('BOOM!')
    smap.remap()
    smap.show()
    time.sleep(0.5)  # Display the explosion for a short time
    explosion.remove()  # Remove the explosion text after displaying it
    boom_box.remove()
    smap.remap()
    smap.show()


#Defining threads for animations
hp_animation_thread = threading.Thread(target=hp_animation, daemon=True)
drill_animation_thread = threading.Thread(target=drill_animation, daemon=True)

#DEBUB
dmg = se.Text(f"Dmg: {damage}")
#dmg.add(map, 30, 2)
hpp = se.Text(f"HP: {hp}")
#hpp.add(map, 30, 3)

# Main game loop
try:
    while running:
        #ui_render() #Uncomment this once implementation is done
        '''with damage_lock:
            dmg.rechar(f"Dmg: {damage}")
        with hp_lock:
            hpp.rechar(f"HP: {hp}")'''
        if hp <= 950 and hp_animation_thread.is_alive() == False and first_rock == True:
            first_rock = False
            hp_animation_thread.start()
        if hp <= 0:
            hp = 1000            
            explosion_animation()
            with rubble_lock:
                rubble += 1
            if rubble >= 1:
                with rubble_lock:
                    rubble_text.rechar(f'Rubble: {int(rubble)}')
        
        smap.remap()
        smap.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    save_game()
    running = False
    #listener.stop()
