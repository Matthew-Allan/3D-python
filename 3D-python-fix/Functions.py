from math import *
import keyboard
import sys
import mouse

def merge_distances(distances_list, screen_width):
    new_distances = [float('inf')] * screen_width

    for distances in distances_list:
        for index, distance in enumerate(distances):
            if distance < new_distances[index]:
                new_distances[index] = distance

    return new_distances


def find_all_distances(line, pivot, direction, angle, screen_width):
    looking = direction
    distances = []

    for each in range(0, int(screen_width / 2)):
        intersection = find_intersection(pivot, looking, line)
        looking = find_next_point(looking, pivot, -angle)
        if intersection is None:
            distance = float('inf')
        else:
            distance = find_distance(pivot, intersection)
        distances.insert(0, distance)

    looking = direction

    for each in range(0, int(screen_width / 2)):
        intersection = find_intersection(pivot, looking, line)
        looking = find_next_point(looking, pivot, angle)
        if intersection is None:
            distance = float('inf')
        else:
            distance = find_distance(pivot, intersection)
        distances.append(distance)

    return distances


def find_intersection(point_1, point_2, line):
    point_3 = line.point_1
    point_4 = line.point_2

    try:
        ta = (((point_3[1] - point_4[1]) * (point_1[0] - point_3[0])) +
              ((point_4[0] - point_3[0]) * (point_1[1] - point_3[1]))) / \
             (((point_4[0] - point_3[0]) * (point_1[1] - point_2[1])) -
              ((point_1[0] - point_2[0]) * (point_4[1] - point_3[1])))
        tb = (((point_1[1] - point_2[1]) * (point_1[0] - point_3[0])) +
              ((point_2[0] - point_1[0]) * (point_1[1] - point_3[1]))) / \
             (((point_4[0] - point_3[0]) * (point_1[1] - point_2[1])) -
              ((point_1[0] - point_2[0]) * (point_4[1] - point_3[1])))
    except ZeroDivisionError:
        return None

    if 0 <= ta <= 1 and 0 <= tb <= 1:
        x = point_1[0] + (ta * (point_2[0] - point_1[0]))
        y = point_1[1] + (ta * (point_2[1] - point_1[1]))
        return [x, y]

    return None


def find_distance(point_1, point_2):
    return sqrt(((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2))


def find_next_point(old_point, pivot, angle):
    angle = radians(angle)

    x = pivot[0] + ((old_point[0] - pivot[0]) * cos(angle)) + ((old_point[1] - pivot[1]) * sin(angle))
    y = pivot[1] - ((old_point[0] - pivot[0]) * sin(angle)) + ((old_point[1] - pivot[1]) * cos(angle))

    return [x, y]


def find_final_values(lines, pivot, direction, screen_width, angle):
    all_distances = []

    for line in lines:
        distances = find_all_distances(line, pivot, direction, angle, screen_width)
        all_distances.append(distances)

    new_distances = merge_distances(all_distances, screen_width)

    return new_distances


def find_heights(player, used_map, screen_width, screen_height, angle_per_line):
    new_distances = find_final_values(used_map.vectors_in_use, player.point,
                                      player.forward, screen_width, angle_per_line)

    heights = []

    for distance in new_distances:
        if distance < 1:
            heights.append(screen_height)
        else:
            heights.append(int(screen_height / 2) / distance)

    return heights, new_distances


def draw_lines(inverted, pivot, used_map, screen_width, screen_height, angle_per_line):
    
    heights, distances = find_heights(pivot, used_map, screen_width, screen_height, angle_per_line)
    
    screen = ""

    rows = []

    if inverted:
        dark = " "
        darkish = "░"
        medium = "▒"
        lightish = "▓"
        light = "█"
    else:
        dark = "█"
        darkish = "▓"
        medium = "▒"
        lightish = "░"
        light = " "

    # █▓▒░

    for layer in range(int(screen_height/2), 0, -1):
        row = []
        for index, height in enumerate(heights):
            if height >= layer:
                if distances[index] > 6:
                    colour = dark
                elif distances[index] > 3:
                    colour = darkish
                elif distances[index] > 1:
                    colour = medium
                else:
                    colour = lightish
                row.append(colour)
            else:
                row.append(light)
        rows.append(row)

    for layer in range(0, int(screen_height/2)):
        row = []
        for index, height in enumerate(heights):
            if height >= layer:
                if distances[index] > 6:
                    colour = dark
                elif distances[index] > 3:
                    colour = darkish
                elif distances[index] > 1:
                    colour = medium
                else:
                    colour = lightish
                row.append(colour)
            else:
                row.append(light)
        rows.append(row)

    
    for row in rows:
        for char in row:
            screen = screen + char

        screen = screen + "\n"
                
    return screen

def movement_mainloop(player_obj, start, big_map, f_pressed):

    # Map key input to player movement
    if keyboard.is_pressed("w"): player_obj.move(player_obj.speed, 0,   start, big_map)
    if keyboard.is_pressed("a"): player_obj.move(player_obj.speed, 270, start, big_map)
    if keyboard.is_pressed("s"): player_obj.move(player_obj.speed, 180, start, big_map)
    if keyboard.is_pressed("d"): player_obj.move(player_obj.speed, 90,  start, big_map)
    if keyboard.is_pressed("f"): f_pressed = True
    if not keyboard.is_pressed("f") and f_pressed and player_obj.static_mouse:
        player_obj.static_mouse = False
        f_pressed = False
    if not keyboard.is_pressed("f") and f_pressed and not player_obj.static_mouse:
        player_obj.static_mouse = True
        f_pressed = False
        player_obj.static_mouse_pos = mouse.get_position()
    if keyboard.is_pressed("esc"): sys.exit(0)

    return f_pressed

def mouse_mainloop(player_obj, start, x1):

    if (mouse.get_position()[0] < 50 or mouse.get_position()[0] > 1500) and player_obj.static_mouse is not True:
        mouse.move(960,540,duration=0)
        return False
        
    x2 = mouse.get_position()[0]
    delta_pos = x2 - x1
    rot = delta_pos * 3
    player_obj.rotate(rot, start)
    if player_obj.static_mouse:
        mouse.move(player_obj.static_mouse_pos[0],player_obj.static_mouse_pos[1],duration=0)
    
    return True
    
