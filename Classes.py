from Functions import *
from math import atan2, radians, degrees, sin, cos
import time


def read_points_from_file(map_name):
    map_file = open(map_name + ".txt", "r")
    lines = map_file.readlines()
    map_file.close()
    map_points = {}
    map_lines = []
    d_type = "p"
    for line in lines:
        if line == "\n":
            continue
        line = line.strip("\n")
        line = line.split("#")[0]
        if line == "-":
            d_type = "l"
            continue
        if d_type == "p":
            line = line.split("=")
            line[1] = line[1].strip("[")
            line[1] = line[1].strip("]")
            coordinates_in_line = line[1].split(",")
            coordinates_in_line[1], coordinates_in_line[0] =\
                float(coordinates_in_line[1]), float(coordinates_in_line[0])
            map_points[line[0]] = coordinates_in_line
        elif d_type == "l":
            line = line.split("=")
            print(line)
            line[1] = line[1].strip("[")
            line[1] = line[1].strip("]")
            points_in_line = line[1].split(",")
            map_line = Line(map_points[points_in_line[0]], map_points[points_in_line[1]])
            map_lines.append(map_line)

    return map_lines


class Line:

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2


class Player:

    def __init__(self, x, y, forward_x, forward_y, draw_distance, normal_speed, normal_sensitivity):
        self.normal_speed = normal_speed
        self.fast_speed = normal_speed * 10
        self.slow_speed = normal_speed / 5
        self.speed = normal_speed
        self.point = [x, y]
        self.forward = [forward_x, forward_y]
        self.draw_distance = draw_distance
        self.normal_sensitivity = normal_sensitivity
        self.fast_sensitivity = normal_sensitivity * 1.5
        self.slow_sensitivity = normal_sensitivity / 2
        self.sensitivity = normal_sensitivity

    def rotate(self, angle, start):
        done = time.time()
        delta_time = done - start
        self.forward = find_next_point(self.forward, self.point, angle * delta_time)

    def move(self, speed, direction, start, used_map):
        vector_x = self.forward[0] - self.point[0]
        vector_y = self.forward[1] - self.point[1]
        angle = atan2(vector_x, vector_y)
        angle = radians(degrees(angle) + direction)
        done = time.time()
        delta_time = done - start
        new_x_pos = self.point[0] + (sin(angle) * speed * delta_time)
        new_y_pos = self.point[1] + (cos(angle) * speed * delta_time)
        closest_intersection = [new_x_pos, new_y_pos]
        for line in used_map.vectors_in_use:
            intersection = find_intersection(self.point, [new_x_pos, new_y_pos], line)
            if intersection is None:
                continue
            else:
                if find_distance(self.point, closest_intersection) > find_distance(self.point, intersection):
                    closest_intersection = intersection

        if closest_intersection != [new_x_pos, new_y_pos]:
            if speed < 0:
                self.point[0] = closest_intersection[0] + (sin(angle) * 0.001)
                self.point[1] = closest_intersection[1] + (cos(angle) * 0.001)
            else:
                self.point[0] = closest_intersection[0] + (sin(angle) * -0.001)
                self.point[1] = closest_intersection[1] + (cos(angle) * -0.001)
            return

        self.point[0], self.point[1] = new_x_pos, new_y_pos
        self.forward[0] += sin(angle) * speed * delta_time
        self.forward[1] += cos(angle) * speed * delta_time


class Map:

    def __init__(self, map_name):
        self.vectors = read_points_from_file(map_name)
        self.vectors_in_use = []

    def change_vectors_in_use(self, center, draw_distance):
        self.vectors_in_use = []
        for vector in self.vectors:
            if find_distance(center, vector.point_1) > draw_distance and \
               find_distance(center, vector.point_2) > draw_distance:
                continue
            self.vectors_in_use.append(vector)
