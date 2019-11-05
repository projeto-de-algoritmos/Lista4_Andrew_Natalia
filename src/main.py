import math
from cities import Cities

import math
import matplotlib.pyplot as plt

# Distancia entre dois pontos
def dist(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# Desenha o pĺano, mostrando os pontos mais proximos
def draw(points, closest_points):
    plt.figure(figsize = (10, 8))
    for point in points:
        plt.scatter(point.x, point.y, color = 'blue')
        plt.annotate(point.name, (point.x, point.y))
    plt.scatter([closest_points[0].x, closest_points[1].x], [closest_points[0].y, closest_points[1].y], color = 'red')
    plt.plot([closest_points[0].x, closest_points[1].x], [closest_points[0].y, closest_points[1].y])
    plt.show()

#
def create_points(cities):
    points_list = []
    for city in cities:
        point = (city.x, city.y)
        points_list.append(point)
    return points_list


def get_closest_points(points):
    len_points = len(points)

    if len_points == 0 or len_points == 1:
        print('empty set of points')
        return
    
    elif len_points == 2:
        return dist(points[0], points[1]), points

    # Sort points based on their x values.
    x_sorted_points = sorted(points, key = lambda x: x.x)
    return get_closest_points_internal(x_sorted_points)


def get_closest_points_internal(points):
    len_points = len(points)
    
    if len_points == 1:
        return [math.inf, points]
    if len_points == 2:
        return [dist(points[0],points[1]), points]
    
    # dividing input to two halves
    first_half = points[:len_points//2]
    second_half = points[len_points//2:]

    # getting minimum distance between two points in each half
    d_f_min, f_closest_points = get_closest_points_internal(first_half)
    d_s_min, s_closest_points = get_closest_points_internal(second_half)

    # minimum distance in two halves
    d_fs_min = min(d_f_min, d_s_min)

    # getting minimum interdistance between halves
    min_inter_dist, closest_inter_points = merge_closest_points(d_fs_min, first_half, second_half) 
    
    # choosing the minimum distance with the corresponding point
    if min_inter_dist < d_fs_min:  
        return [min_inter_dist, closest_inter_points]
    elif d_f_min > d_s_min:
        return [d_s_min, s_closest_points]
    else:
        return [d_f_min, f_closest_points]
    

def merge_closest_points(d_fs_min, first_half, second_half):

    min_inter_dist = d_fs_min
    out_of_range = False
    i = len(first_half) - 1
    closest_inter_point = -1
    # calculate distance between points starting from closest ones on the x axis
    while i > -1 and not out_of_range:
        for j in range(len(second_half)):
            first_x = first_half[i].x
            first_y = first_half[i].y
            second_x = second_half[j].x
            second_y = second_half[j].y

            # if distance between x-values exceeds minimum distance 
            # then all points after this one will give bigger distance (because halves are sorted)    
            if abs(second_x - first_x) > d_fs_min:
                if j == 0:
                    out_of_range = True
                break
            
            dist_i_j = math.sqrt((first_x - second_x)**2 + (first_y - second_y)**2)
            if dist_i_j < min_inter_dist:
                min_inter_dist = dist_i_j
                closest_inter_point = [first_half[i], second_half[j]]
        i -= 1
    
    return min_inter_dist, closest_inter_point 

def main():
    uf = input("Digite o estado: ")
    cities = Cities(uf)
    points = cities.list
    d, closest_points = get_closest_points(points)
    draw(points, closest_points)

if __name__ == '__main__':
    main()
