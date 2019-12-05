
input()

# Import classes (and functions)

from Classes import *

# Define screen dimensions

Screen_Height = 62
Screen_Width = 210

# Set screen dimensions to even numbers

if Screen_Height % 2 == 1:
    Screen_Height -= 1

if Screen_Width % 2 == 1:
    Screen_Width -= 1

# Define FOV

FOV = 45

# Define the change in angle per ray

Angle_Per_Line = FOV / Screen_Width

# Set draw distance

Draw_Distance = 10

# Define player (position in map and point it is looking towards)

player = Player(3, 8, 20, 8.5, Draw_Distance, 1, 70)

big_map = Map("Big Map")

big_map.change_vectors_in_use(player.point, Draw_Distance)

timer_normal = 5

timer = timer_normal

Start = time.time()


while True:
    
    Start = time.time()
    screen = draw_lines(True, player, big_map, Screen_Width, Screen_Height, Angle_Per_Line)
    print(screen)
    Angle_Per_Line = FOV / Screen_Width
    if timer == 0:
        big_map.change_vectors_in_use(player.point, Draw_Distance)
        timer = timer_normal
    else:
        timer -= 1
    player.move(player.speed, 0, Start, big_map)
