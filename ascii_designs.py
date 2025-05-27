#ASCII Designs

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


Smelter > Unlocks resource convertion
╔═══╗
║███║
║▓▓▓║
╚═▲═╝

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
pure_background_top =r'''
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
pure_background_bottom = r'''
                           ,
                          / \
                         ,'  \                                          ,
                        ,'    \._                      ,.              .'.                           ,_
..._______ _____ ____..'       ,V`,       _,., ___,,.-'  `-..____...._,'  `-... --`--......_____,,..,  `-.,_
'''



def ascii_converter(input):
    background_top = []
    lines = input.strip('\n').split('\n')

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != " ":
                background_top.append((f'\033[38;5;236m{char}\033[0m', x, y))
    return background_top

background_top = ascii_converter(pure_background_top)
background_bottom = ascii_converter(pure_background_bottom)
