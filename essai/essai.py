# -*- coding: utf-8 -*-
"""
Created on Thu May  5 12:07:01 2022

@author: Delete
"""
import matplotlib.pyplot as plt
from math import cos, sin, pi

def matrice(point, matrice_rotation):
    """ renvoie les coordonnes du point en passant par la matrice de rotation"""
    
    nvx_point=[0,0,0]
    for i in range(3):
        for j in range(3):
            nvx_point[i]+=point[j]*matrice_rotation[3*i+j]
    nvx_point=[round(nvx_point[i],12) for i in range(3)]
    return nvx_point


def coordonne(point, angle):
    """ retourne les nouvelles coordonnes du point avec une rotation 
    d'angle 'angle' """
    rotation_x=[1,      0,      0,
                0, cos(angle), -sin(angle),
                0, sin(angle), cos(angle)]
    
    rotation_y=[cos(angle), 0, -sin(angle),
                    0,      1,      0,
                sin(angle), 0, cos(angle)]
    
    rotation_z=[cos(angle), -sin(angle), 0,
                sin(angle), cos(angle), 0,
                    0,      0,      1]
    
    
    #tout les axes
    point=matrice(point, rotation_z)
    point=matrice(point, rotation_x)
    return matrice(point,rotation_y)
    
    

def mouvement(points_list, angle_tour):
    """ applique les nouvelles coordonnees aux points du carré """
    points_list = [coordonne(points_list[i], angle_tour)
                   for i in range(len(points_list))]
    return points_list

    
def cube(points_list_2d):
    """dessine le cube 3d """
    milieu=int(len(points_list_2d)/2)
    x1 = [points_list_2d[i+milieu][0] for i in range(milieu)] + [points_list_2d[milieu][0]]
    y1 = [points_list_2d[i+milieu][1] for i in range(milieu)] + [points_list_2d[milieu][1]]
    plt.plot(x1, y1, 'red')

    x = [points_list_2d[i][0] for i in range(milieu)] + [points_list_2d[0][0]]
    y = [points_list_2d[i][1] for i in range(milieu)] + [points_list_2d[0][1]]
    plt.plot(x, y, 'blue')  # plt.plot(x,y,'blue')

    color = ['violet', 'green', 'yellow', 'orange']
    for i in range(milieu):
        x1 = [points_list_2d[i][0], points_list_2d[i+milieu][0]]
        y1 = [points_list_2d[i][1], points_list_2d[i+milieu][1]]
        plt.plot(x1, y1, 'black')  # ,marker='o'

    
def in2d_Thales(points_list, camera,rapprochement):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation of the theoreme of Thales"""
    nvx_points_list = []

    mur = [2+rapprochement,0,0]  # le mur est sur l'axe des x
    rapport_cam_mur = camera[0]-mur[0]
    for i in points_list:
        dist = camera[0]-i[0]
        rapport = rapport_cam_mur/dist
        nvx_points_list.append( (round(rapport*(i[1]-camera[1])+camera[1], 12),
                                round(rapport*(i[2]-camera[2])+camera[2], 12)) )
    return nvx_points_list


def in2d_parameter(points_list, camera,rapprochement):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation des droites parametrees"""
    nvx_points_list = []
    mur = [2+rapprochement,0,0]  # le mur est sur l'axe des x
    for i in points_list:
        inverse_alpha=(mur[0]-camera[0])/(i[0]-camera[0])
        vector_plan_y=inverse_alpha*(i[1]-camera[1])
        vector_plan_z=inverse_alpha*(i[2]-camera[2])
        
        point_projection=( (round(camera[1]+vector_plan_y ,12),
                          round(camera[2]+vector_plan_z ,12)) )
        nvx_points_list.append(point_projection)
    return nvx_points_list


def affichage(points_list, choix_3d):
    """fait tourner le carré 
    points_list: list de tuple"""

    tour = 0
    fps = 10
    angle_tour = pi/30
    rapprochement = 0
    
    # permet de faire 1 rotation à tant fps(c'est une variable)
    while tour <= fps:
        plt.clf()
        plt.close()
        
        camera = (6+rapprochement, 0, 0)
        if choix_3d == 0:
            points_list_2d = in2d_Thales(points_list, camera,rapprochement)
        else:
            points_list_2d = in2d_parameter(points_list, camera,rapprochement)

        # permet d'afficher le cube en 3d (en 3 étapes)
        cube(points_list_2d)

        # permet de garder la même échelle en fonction des graphiques
        scale_graphique = 3
        plt.plot(scale_graphique, scale_graphique)
        plt.plot(-scale_graphique, -scale_graphique)
         
        #  Repère orthonormée
        plt.xlim(-5, 5)
        plt.ylim(-5, 5)
        plt.axis('equal')  
        plt.autoscale(False)

        # affichage + changement des coordonnes des points
        plt.show()

        points_list = mouvement(points_list, angle_tour)
        plt.pause(1/fps)
        tour += 1
        #rapprochement+=-1/10


def main():
    """execute le prgm"""
    forme = int(input("Choisi la forme:\n0=cube / 1=T "))
    if forme==0:
        points_list = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                       (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)]
    else:
        points_list= [(-2, 2, 1),(-2, 1, 1),(-1, 1, 1), (-1, -2, 1),(1, -2, 1), (1, 1, 1),(2, 1, 1),(2, 2, 1),
                     (-2, 2, -1),(-2, 1, -1),(-1, 1, -1), (-1, -2, -1),(1, -2, -1), (1, 1, -1),(2, 1, -1),(2, 2, -1)]

    choix_3d = int(input("\nchoix de la fonction 3d:\n0=Thales / 1=Parameter "))
    affichage(points_list, choix_3d)


# Progamme principal
if __name__=='__main__':
    main()