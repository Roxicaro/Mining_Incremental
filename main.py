import scrap_engine as se
import time, os, threading, sys

os.system("")
width, height = os.get_terminal_size()
t=ev=v=0
g=0.015

map=se.Map(height, 1000, " ")
smap=se.Submap(map, 0, 0)

block=se.Object("#")
ground=se.Square("#", map.width, 5)
player=se.Object(f'O')
frame = se.Frame(height-1, width-1, 
                 corner_chars=["+", "+", "+", "+"], 
                 horizontal_chars=["-", "-"], 
                 vertical_chars=["|", "|"], state="solid")
h=se.Text("00 00")

player.add(map, round(smap.width/2), round(map.height/2))
frame.add(map, 0,0)


smap.remap()
smap.show(init=True)

smap.remap()
smap.show()
smap.set(smap.x+1, smap.y)
