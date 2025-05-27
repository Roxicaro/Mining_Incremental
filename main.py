import scrap_engine as se
import time, os, threading, sys
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

#Implement Save Data
SAVE_FILE = "save.txt"
save_text = se.Text("Game Saved.", "float")
load_text = se.Text("Game Loaded.", "float")

#Show "game saved" notification on screen
def save_notification(): 
        save_text.add(map, frame.width - (len(save_text.text)+1), 1)
        time.sleep(0.75)
        save_text.remove()

def load_notification(): 
        load_text.add(map, frame.width - (len(load_text.text)+1), 1)
        time.sleep(0.75)
        load_text.remove()

def save_game():
    with open(SAVE_FILE, 'w') as f:
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
        f.write(f"{store_can_open}\n")
        f.write(f"{command_bottom}\n")
        f.write(f"{auto_mine_cd}\n")
        f.write(f"{descend_available}\n")
        f.write(f"{depth}\n")
        f.write(f"{mining_cart_bought}\n")
        f.write(f"{build_can_open}")
        save_notification()        

##### LOAD GAME FUNCTION #####
def load_game():
    global iron, gold, rubble, drill_power, auto_miner, auto_mine_level, drill_power_price, auto_miner_price, hp, damage, store_can_open, commands, command_bottom, auto_mine_cd, descend_available, depth, mining_cart_bought, build_can_open   
    try:
        with open(SAVE_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) < 17:
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
            store_can_open = lines[10].strip().lower() == 'true'
            command_bottom = lines[11].strip() 
            auto_mine_cd = float(lines[12].strip())
            descend_available = lines[13].strip().lower() == 'true'   
            depth = int(lines[14].strip())
            mining_cart_bought = lines[15].strip().lower() == 'true'
            build_can_open = lines[16].strip().lower() == 'true'  
            
            # Update UI
            iron_text.remove()
            gold_text.remove()
            rubble_text.remove()
            depth_text.remove()          
            if iron > 0:
                iron_text.add(map,3,1)
                iron_text.rechar(f'Iron: {int(iron)}')
            if gold > 0:
                gold_text.add(map, iron_text.x, iron_text.y+1)
                gold_text.rechar(f'Gold: {int(gold)}')
            if rubble > 0:
                rubble_text.add(map,iron_text.x,iron_text.y+2)
                rubble_text.rechar(f'Rubble: {int(rubble)}')
            if auto_mine_level > 0:
                auto_mine.rechar(f"[A]uto-mine ({auto_mine_level})")
            auto_mine_price.rechar(f"{int(auto_miner_price)} Gold")
            if drill_power >=2:
                better_drill.rechar(f"[B]etter drill ({drill_power})")
            better_drill_price.rechar(f"{int(drill_power_price)} Gold")
            if descend_available == True:
                start_descend_text.rechar("[D]escend")
                start_descend_text_price.rechar(f"{descend_price} Rubble")
                ui_box.set_ob(start_descend_text_price, menu_ui.width - len(start_descend_text_price.text)-1, 4) #reset UI position
            if depth > 0:
                depth_text.rechar(f'> Depth: {depth} <')
                depth_text.add(map, int((frame.width/2)-len(depth_text.text)+7), 1)

            commands.add(map, 1,frame.height)
            commands.rechar(f"{command_bottom}")

            #Start auto_mine if game is loaded
            if auto_miner == True:
                auto_miner_thread = threading.Thread(target=iron_counter, daemon=True)
                auto_miner_thread.start()
            if mining_cart_bought == True:
                create_mining_cart(map, frame.width-40, frame.height-4)
                mining_cart_price_text.rechar("ACTIVE!")
                auto_sell_thread = threading.Thread(target=auto_sell, daemon=True)
                auto_sell_thread.start() 
 
            load_notification()
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

#GLOBAL VARIABLES----------------------------------------------------------------
#Rock status
first_rock = True
damage = 0
damage_lock = Lock()
max_hp = 1000
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

rubble = int(0)
rubble_lock = Lock()

#STATES
store_can_open = False #Opens once 1st gold is aquired
store_open = False #Store UI check
build_can_open = False
build_open = False
autosave = False #Game starts with auto-save feature disabled
mining_cart_bought = False #Mining cart bought state
auto_sell_thread = None #Auto-sell thread

#Auto miner
auto_miner = False #Auto miner
auto_miner_price = 1
auto_miner_price_increase = 10
auto_miner_thread = None
auto_mine_cd = float(1)

#Descend
descend_available = False
descend_started = False
descend_price = 5

#Depth
depth = int(0)
depth_lock = Lock()

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

build_ui = se.Frame(6,40,
                 corner_chars=["╭", "╮", "╰", "╯"], 
                 horizontal_chars=["─", "─"], 
                 vertical_chars=["│", "│"], state="float")

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
start_descend_text = se.Text(f"", float) #Blank descend text to be updated latter
start_descend_text_price = se.Text(f"", float) #Blank descend text to be updated latter

#Create UI box that will contain all Store UI elements
ui_box = se.Box(menu_ui.width, menu_ui.height)
ui_box.add_ob(menu_ui, 0,0)
ui_box.add_ob(store_text, (int(menu_ui.width/2)) -len(store_text.text)+5, 1)
ui_box.add_ob(close_store_text, menu_ui.width - len(close_store_text.text) -3, menu_ui.height-1)
ui_box.add_ob(auto_mine, 1, 2)
ui_box.add_ob(auto_mine_price, menu_ui.width - len(auto_mine_price.text)-1, 2)
ui_box.add_ob(better_drill, 1, 3)
ui_box.add_ob(better_drill_price, menu_ui.width - len(better_drill_price.text)-1, 3)
ui_box.add_ob(start_descend_text, 1, 4)
ui_box.add_ob(start_descend_text_price, menu_ui.width - len(start_descend_text_price.text)-1, 4)

ui_center_x = int((width/2)-(menu_ui.width/2))
ui_center_y = int((height/2)-(menu_ui.height/2))


#Build UI text elements
build_text = se.Text("___Build___", "float")
close_build_text = se.Text("[T]Exit build", float)
mining_cart_text = se.Text("[M]ining cart", float)
mining_cart_price_text = se.Text(f"10 Gold", float)

#Create UI box that will contain all Build UI elements
build_ui_box = se.Box(build_ui.width, build_ui.height)
build_ui_box.add_ob(build_ui, 0,0)
build_ui_box.add_ob(build_text, (int(build_ui.width/2)) -len(build_text.text)+5, 1)
build_ui_box.add_ob(close_build_text, build_ui.width - len(close_build_text.text) -3, build_ui.height-1)
build_ui_box.add_ob(mining_cart_text, 1, 2)
build_ui_box.add_ob(mining_cart_price_text, build_ui.width - len(mining_cart_price_text.text)-1, 2)

# Create text
    #Tutorial text
tutorial_state = f'{">   Press SPACEBAR to mine the boulder   <":^{frame.width+2}}' #Tutorial text
tutorial=se.Text(tutorial_state, float)
tutorial.add(map, 0, center_y-1) # Add tutorial text to the map

    #Command list text
command_bottom = '' # Initialize command list
commands = se.Text(command_bottom, float)

    #Resources text
iron_text=se.Text(f'', float) # Create a text object to display iron count
iron_text.add(map,3,1)
gold_text=se.Text(f'', float) # Create a text object to display gold count
gold_text.add(map, iron_text.x, iron_text.y+1)
rubble_text=se.Text(f'', float)
rubble_text.add(map,3,3)

    #Depth counter text
depth_text = se.Text(f'> Depth: {depth} <', float)

    #TESTING TEXT FOR COLORS
'''test_text = se.Text(f'\033[31;1;4mTESTING COLORS\033[0m', float)
test_text.add(map, int((frame.width/2)-len(depth_text.text)+7), 2)'''

# Player design data
from player_design import PLAYER_DESIGN  # Import player design data
def create_player(map, start_x=4, start_y=5):
    for char, rel_x, rel_y in PLAYER_DESIGN:
        se.Object(char).add(map, start_x + rel_x, start_y + rel_y)

#Background
from ascii_designs import background_top
bg_top = []
def create_bg_top(map, start_x=1, start_y=1):
    global bg_top
    for char, rel_x, rel_y in background_top:
        obj = se.Object(char,float)
        obj.add(map, start_x + rel_x, start_y + rel_y)
        bg_top.append(obj)
    return bg_top
create_bg_top(map)

# Rock design data
from rock_design import ROCK_DESIGN  # Import rock design data
rock_parts = []  # List to store rock parts
def create_rock(map, start_x=24, start_y=5):
    global rock_parts
    for char, rel_x, rel_y in ROCK_DESIGN:
        obj = se.Object(char,float)
        obj.add(map, start_x + rel_x, start_y + rel_y)
        rock_parts.append(obj)
    return rock_parts

def remove_rock():
    for part in rock_parts:
        part.remove()

#Mining-cart design data
from ascii_designs import mining_cart_design, mining_cart_design_2
mining_cart_parts = []
def create_mining_cart(map, start_x=15, start_y=5, mining_cart_design=mining_cart_design):
    global mining_cart_parts
    for char, rel_x, rel_y in mining_cart_design:
        obj = se.Object(char)
        obj.add(map, start_x + rel_x, start_y + rel_y)
        mining_cart_parts.append(obj)
    return mining_cart_parts

def remove_mining_cart():
    for part in mining_cart_parts:
        part.remove()

def mining_cart_animation():
    global mining_cart_parts
    create_mining_cart(map, frame.width-40, frame.height-4)
    time.sleep(0.3)  # Adjust the speed of the animation
    remove_mining_cart()
    create_mining_cart(map, frame.width-41, frame.height-4, mining_cart_design_2)
    time.sleep(0.3)  # Adjust the speed of the animation
    remove_mining_cart()
    create_mining_cart(map, frame.width-42, frame.height-4)
    time.sleep(0.3)  # Adjust the speed of the animation
    remove_mining_cart()
    create_mining_cart(map, frame.width-41, frame.height-4, mining_cart_design_2)
    time.sleep(0.3)  # Adjust the speed of the animation
    remove_mining_cart()
    mining_cart_animation()

#HP bar objects
'''
filled = '■'
empty = '□' 
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
#create_mining_cart(map, frame.width-40, frame.height-4)

smap.show(init=True)
smap.set(smap.x+1, smap.y)


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
        time.sleep(auto_mine_cd)  # Update every 1 second

def auto_sell(): #Starts once the mining cart is bought and is active
    global iron, gold, mining_cart_bought
    while running:
        if mining_cart_bought == True:
            with iron_lock:
                if iron >= 50:
                    iron -= 50
                    iron_text.rechar(f'Iron: {int(iron)}')
                    with gold_lock:
                        gold += 1
                        gold_text.rechar(f'Gold: {int(gold)}')
            smap.remap()
            smap.show()
        time.sleep(0.1)

# Keyboard control
space_pressed = False
def on_press(key):
    global iron, gold, space_pressed, drill_state, hp, hp_lock, damage, damage_lock, tutorial_state,command_bottom, store_can_open, store_open, auto_miner, drill_power, ui_center_x, ui_center_y, autosave, descend_price, build_can_open, build_open, mining_cart_bought, auto_sell_thread
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
            if autosave == False:
                autosave = True        
        
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
                iron_text.rechar(f'Iron: {int(iron)}')
                with gold_lock:
                    gold += 1
                    gold_text.rechar(f'Gold: {int(gold)}')
                    store_can_open = True #Allows store to open
                    if command_bottom == command_list[0] + spacer + command_list[1] + spacer: #rewrite later
                        command_bottom += command_list[2] + spacer
                        commands.rechar(command_bottom)
                smap.remap()
                smap.show()
    
    #Opens and closes Store
    if key == KeyCode(char='e') and store_can_open == True and build_open == False: 
        if store_open == False:
            ui_box.add(map, ui_center_x, ui_center_y)
            store_open = True
            ui_box.set_ob(auto_mine_price, menu_ui.width - len(auto_mine_price.text)-1, 2) #Fix position of auto_mine price
            ui_box.set_ob(better_drill_price, menu_ui.width - len(better_drill_price.text)-1, 3) #Fix position of better_drill price
        elif store_open == True:
            store_open = False
            ui_box.remove()
    
    #Opens and closes Build UI
    if key == KeyCode(char='t'): 
        if build_open == False and build_can_open == True and store_open == False:
            build_ui_box.add(map, ui_center_x, ui_center_y)
            build_open = True
        elif build_open == True:
            build_open = False
            build_ui_box.remove()
    
    #Build actions
    if key == KeyCode(char='m') and build_open == True and mining_cart_bought == False:
        if gold >= 10:
            with gold_lock:
                gold -= 10
                gold_text.rechar(f'Gold: {int(gold):<7}')
            #Create mining cart
            create_mining_cart(map, frame.width-40, frame.height-4)
            mining_cart_price_text.rechar("ACTIVE!")
            ui_box.set_ob(mining_cart_price_text, menu_ui.width - len(mining_cart_price_text.text)-1, 2)
            mining_cart_bought = True
            smap.remap()
            smap.show()
        #Start auto-sell thread if mining cart is bought
        if mining_cart_bought == True and auto_sell_thread is None or not auto_sell_thread.is_alive():
            auto_sell_thread = threading.Thread(target=auto_sell, daemon=True)
            auto_sell_thread.start()
    
    #Store actions
    if key == KeyCode(char='a') and store_open == True:
        global auto_miner_price, auto_miner_price_increase, drill_power_price, drill_power_price_increase, auto_mine_level, auto_mine_cd
        if gold >= auto_miner_price:
            with gold_lock:
                gold -= auto_miner_price
                gold_text.rechar(f'Gold: {int(gold):<7}')             
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
                gold_text.rechar(f'Gold: {int(gold):<7}')
                drill_power += 1
                drill_power_price = drill_power_price * drill_power_price_increase
            better_drill.rechar(f"[B]etter drill ({drill_power})")
            better_drill_price.rechar(f"{drill_power_price} Gold")
            ui_box.set_ob(better_drill_price, menu_ui.width - len(better_drill_price.text)-1, 3)
            smap.remap()
            smap.show()
    
    if key == KeyCode(char='d') and store_open == True:
        global rubble, rubble_lock, descend_price, descend_available, descend_started, depth_lock, depth, depth_text
        if rubble >= descend_price:
            with rubble_lock:
                rubble -= descend_price
                rubble_text.rechar(f'Rubble: {int(rubble)}')
            with depth_lock:
                if descend_started == False:
                    descend_started = True
                depth += 1
                depth_text.remove()
                depth_text.rechar(f'> Depth: {depth} <')
                depth_text.add(map, int((frame.width/2)-len(depth_text.text)+7), 1)
            smap.remap()
            smap.show()
            if command_bottom == command_list[0] + spacer + command_list[1] + spacer + command_list[2] + spacer:
                command_bottom += command_list[3] + spacer
                commands.rechar(command_bottom)
                build_can_open = True
                smap.remap()
                smap.show()
    
    #Press Esc to quit game
    if key == Key.esc:
        global running
        save_game()
        running = False
        raise KeyboardInterrupt 
    
    #Debugging
    '''if key == KeyCode(char='w'):
        with iron_lock:
            iron += 100000
            iron_text.rechar(f'Iron: {int(iron)}')
        with gold_lock:
            gold += 100000
            gold_text.rechar(f'Gold: {gold}')
        with rubble_lock:
            rubble += 1000
            rubble_text.rechar(f'Rubble: {rubble}')'''
    
    if key == KeyCode(char='7'):
        global mining_cart_animation_thread
        mining_cart_animation_thread = threading.Thread(target=mining_cart_animation, daemon=True)
        mining_cart_animation_thread.start()

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
        if hp <= (max_hp*0.95) and hp >= (max_hp*0.9):
            hp_state = '[■■■■■■■■■□]' if hp_state == '[■■■■■■■■■■]' else '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.9) and hp >= (max_hp*0.8):
            hp_state = '[■■■■■■■■□□]' if hp_state == '[■■■■■■■■■□]' else '[■■■■■■■■■□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.8) and hp >= (max_hp*0.7):
            hp_state = '[■■■■■■■□□□]' if hp_state == '[■■■■■■■■□□]' else '[■■■■■■■■□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.7) and hp >= (max_hp*0.6):
            hp_state = '[■■■■■■□□□□]' if hp_state == '[■■■■■■■□□□]' else '[■■■■■■■□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.6) and hp >= (max_hp*0.5):
            hp_state = '[■■■■■□□□□□]' if hp_state == '[■■■■■■□□□□]' else '[■■■■■■□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.5) and hp >= (max_hp*0.4):
            hp_state = '[■■■■□□□□□□]' if hp_state == '[■■■■■□□□□□]' else '[■■■■■□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.4) and hp >= (max_hp*0.3):
            hp_state = '[■■■□□□□□□□]' if hp_state == '[■■■■□□□□□□]' else '[■■■■□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.3) and hp >= (max_hp*0.2):
            hp_state = '[■■□□□□□□□□]' if hp_state == '[■■■□□□□□□□]' else '[■■■□□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.2) and hp >= (max_hp*0.1):
            hp_state = '[■□□□□□□□□□]' if hp_state == '[■■□□□□□□□□]' else '[■■□□□□□□□□]'
            hp_bar.rechar(hp_state)
        elif hp < (max_hp*0.1) and hp >= 0:
            hp_state = '[□□□□□□□□□□]' if hp_state == '[■□□□□□□□□□]' else '[■□□□□□□□□□]'
            hp_bar.rechar(hp_state)        
        else:
            hp_state = '[■■■■■■■■■■]'
            hp_bar.rechar(hp_state)
        time.sleep(0.5)  # Same timing drill animation
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

#Game state checker function
def game_state():
    if autosave == True:
        save_game()
    time.sleep(30)
    game_state()

#Defining threads
    #Animations
hp_animation_thread = threading.Thread(target=hp_animation, daemon=True)
drill_animation_thread = threading.Thread(target=drill_animation, daemon=True)
mining_cart_animation_thread = threading.Thread(target=mining_cart_animation, daemon=True)

    #Game State checker
game_state_thread = threading.Thread(target=game_state, daemon=True)
game_state_thread.start()


#DEBUB
dmg = se.Text(f"Dmg: {damage}")
#dmg.add(map, 30, 2)
hpp = se.Text(f"HP: {hp}")
#hpp.add(map, 30, 3)

#Try to auto-load game
load_game()

# Main game loop
try:
    while running:
        '''with damage_lock:
            dmg.rechar(f"Dmg: {damage}")
        with hp_lock:
            hpp.rechar(f"HP: {hp}")'''
        if hp <= 950 and hp_animation_thread.is_alive() == False and first_rock == True:
            first_rock = False
            hp_animation_thread.start()
        if hp <= 0:
            if descend_available == False:
                descend_available = True
                start_descend_text.rechar("[D]escend")
                start_descend_text_price.rechar(f"{descend_price} Rubble")
                ui_box.set_ob(start_descend_text_price, menu_ui.width - len(start_descend_text_price.text)-1, 4)
            max_hp = 1000 + int(100 * depth)
            hp = max_hp         
            explosion_animation()
            with rubble_lock:
                rubble += 1
                rubble_text.add(map,3,3)
                rubble_text.rechar(f'Rubble: {int(rubble)}')
        '''#TESTING COLORS
        for i in range(30,38):
            test_text.rechar(f'\033[{i};1;4mTESTING COLORS {i}\033[0m')
            time.sleep(0.1)'''
        
        smap.remap()
        smap.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    save_game()
    running = False
