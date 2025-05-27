pure_background_top =r'''
                     .                                               __,,,-''-.....     ____ ___.--..     ,   
-'-.    ,-''-''`._,./ \          ,-.-L....__---.            _..   ,-'              \   /    '        `'--' ``.
    \ ,'               ]    ,-`-'              \          ,'   `.'                  | .'                      
     -                  \ ,'                    |        '                          `/'                       
                         ||                     `. ..   .'                                                    
                         `'                      i|     |                                                     
                                                 '|   | /                                                     
                                                     | |                                                      
                                                     |,'                                                      
                                                      |/                                                      
                                                      ;                                                        
'''

def converter(input=pure_background_top):
    background_top = []
    lines = pure_background_top.strip('\n').split('\n')

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            background_top.append((f'\033[38;5;236m{char}\033[0m', x, y))
    return background_top

print(converter())