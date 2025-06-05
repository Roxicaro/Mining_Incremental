# Copyright (C) 2025 Icaro Alves (Roxicaro)
# This file is part of Mining Incremental, licensed under GPL-3.0.

#ASCII Designs
# Player object
mining_drill_design = r'''
╔╦╦╗
╠╬╬╣
╚╩╩╝
'''
#Alternative art 1
'''
▄██▄
█▓▓█
▀██▀
'''
#Alternative art 2
'''
██►
'''

mining_cart_design = [
    # Row 0 (top) - "╭─────╮"
    ('╭', 0, 0), ('─', 1, 0), ('─', 2, 0),('─', 3, 0),('─', 4, 0),('─', 5, 0),('╮', 6, 0),
    
    # Row 1 - "│▽△□ │"
    ('│', 0, 1), (' ', 1, 1), ('▽', 2,1),('△', 3, 1),('□', 4, 1),(' ', 5, 1),('│', 6, 1),
    
    # Row 2 - "╰⊙─⊙╯"
    ('╰', 0, 2), ('⊙', 1, 2), ('─', 2, 2),('─', 3, 2),('─', 4, 2),('⊙', 5, 2),('╯', 6, 2)
]

mining_cart_design_2 = [
    # Row 0 (top) - "╭─────╮"
    ('╭', 0, 0), ('─', 1, 0), ('─', 2, 0),('─', 3, 0),('─', 4, 0),('─', 5, 0),('╮', 6, 0),
    
    # Row 1 - "│▽△□ │"
    ('│', 0, 1), (' ', 1, 1), ('▽', 2,1),('△', 3, 1),('□', 4, 1),(' ', 5, 1),('│', 6, 1),
    
    # Row 2 - "╰⊙─⊙╯"
    ('╰', 0, 2), ('◎', 1, 2), ('─', 2, 2),('─', 3, 2),('─', 4, 2),('◎', 5, 2),('╯', 6, 2)
]


'''
◎ and ◉
Mining cart > Autosells IRON > moves back and forth 
╭─────╮  
│▽△□ │  
╰⊙─⊙╯

   .-----.
  /       \
 |  (===)  |
 |   | |   |
 |   \_/   |
 |  \   /  |
 |   \_/   |
 '-----^----'
'''

#Background                                                 
background_top_design =r'''
                     .                                               __,,,-''-.....     ____ ___.--..     ,   
-'-.    ,-''-''`._,./ \          ,-.-L....__---.            _..   ,-'              \   /    '        `'--' ``.
    \ ,'               ]    ,-`-'              \          ,'   `.'                  | .'                      
     -                  \ ,'                    |        '                          `/'                       
                         ||                     `. ..   .'                                                    
                         `'                       |     |                                                     
                                                 '|   | /                                                     
                                                    | |                                                      
                                                    |,'                                                      
                                                    |/                                                      
                                                    ;                                                        
'''
background_bottom_design = r'''
                           ,
                          / \
                         ,'  \                                          ,
                        ,'    \._                      ,.              .'.                           ,_
..._______ _____ ____..'       ,V`,       _,., ___,,.-'  `-..____...._,'  `-... --`--......_____,,..,  `-.,_
'''

#Smelter
    #Unlocks resource convertion
smelter_design= r'''
╔═══╗
║███║
║▓▓▓║
╚═▲═╝
'''

#Rock design
rock_design = r'''
    ___
  _/__/\
 / \  \ \
 \__\__\/
'''

#Large rock design
'''
         __________
   _____/_____ \__/\
  /     \      \  \ \
 /      \      \  \  \
/       \      \  \   \
\_______\______\___\__/
'''

'''
Rock HP and different types of rock
Stone
Copper Ore
Iron Ore
Gold Vein
Diamond Cluster
Mithril Chunk
Coal Seam

 █ (filled)
 ░ (empty)
 
 Alternatives:
 |■■■■■■□□□□| 50%
 ■ (filled)
 □ (empty)
 ▰▰▰▰▱▱
 '''


def ascii_converter(input, color="\033[0m"):
    output = []
    lines = input.strip('\n').split('\n')

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != " ":
                output.append((f'{color}{char}\033[0m', x, y))
    return output

background_top = ascii_converter(background_top_design, "\033[38;5;236m")
background_bottom = ascii_converter(background_bottom_design, "\033[38;5;236m")
smelter = ascii_converter(smelter_design)
rock = ascii_converter(rock_design)
mining_drill = ascii_converter(mining_drill_design)
