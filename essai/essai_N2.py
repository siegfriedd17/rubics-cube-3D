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
    #point=matrice(point, rotation_z)
    #point=matrice(point, rotation_x)
    return matrice(point,rotation_y)
    
    

def mouvement(points_list, angle_tour):
    """ applique les nouvelles coordonnees aux points du carré """
    points_list = [coordonne(points_list[i], angle_tour)
                   for i in range(len(points_list))]
    return points_list

    
def cube_test(points_list_2d):
    """dessine le cube 3d """
    
    x1 = [points_list_2d[i+4][0] for i in range(4)] + [points_list_2d[4][0]]
    y1 = [points_list_2d[i+4][1] for i in range(4)] + [points_list_2d[4][1]]
    plt.plot(x1, y1, 'violet')

    x = [points_list_2d[i][0] for i in range(4)] + [points_list_2d[0][0]]
    y = [points_list_2d[i][1] for i in range(4)] + [points_list_2d[0][1]]
    plt.plot(x, y, 'blue')  # plt.plot(x,y,'blue')

    
    for i in range(4):
        x1 = [points_list_2d[i][0], points_list_2d[i+4][0]]
        y1 = [points_list_2d[i][1], points_list_2d[i+4][1]]
        plt.plot(x1, y1, 'black')  # ,marker='o'


def cube(points_list_2d, face, ordre, couleur):
    """dessine un cube 3d """

    for h in ordre: #permet de dessiner 6 faces
        
        pts=face[h]
        coord=[points_list_2d[i] for i in pts]
        #print(pts,coord)
        x1 = [j[0] for j in coord] 
        y1 = [j[1] for j in coord]
        #print(x1,y1,couleur[ h ])
        
        plt.fill(x1, y1, couleur[h])
    plt.show()
    #print('---')
    #print('/////')
    
    
        

def dist_camera_points(points_list, face, camera):
    """renvoie l'ordre de remplissage des faces en fonction de 
    la localisation du point central de la face par rapport à la camera"""
    ordre=0
    pts_centor=[]
    for i in face:
        #calcule le vecteur(x,y,z) entre les points opposés d'une face 
        vector=[points_list[i[2]][0] - points_list[i[0]][0],
                points_list[i[2]][1] - points_list[i[0]][1],
                points_list[i[2]][2] - points_list[i[0]][2]]
        vector=[i/2 for i in vector]
        
        #on obtient les coordonnees du point central de la face
        centor=(points_list[i[0]][0]+vector[0],
                points_list[i[0]][0]+vector[1],
                points_list[i[0]][0]+vector[2])
        distance_cam_centor=camera[0]-centor[0]
        pts_centor.append( (distance_cam_centor, ordre) )
        ordre+=1
    #on trie les faces à dessiner en premier
    pts_centor.sort( key=lambda x: x[0],reverse=True)
    ordre_face=[i[1] for i in pts_centor]
    return ordre_face
    

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


def affichage(points_list,face,couleur):
    """fait tourner le carré 
    points_list: list de tuple"""
    tour = 0
    fps = 60
    angle_tour = pi/30
    rapprochement = 0
    
    # permet de faire 1 rotation à tant fps(c'est une variable)
    while tour <= fps:
        plt.clf()
        plt.close()
        
        camera = (6+rapprochement, 0, 0)
        ordre=dist_camera_points(points_list, face, camera)
        points_list_2d = in2d_parameter(points_list, camera,rapprochement)

        # permet d'afficher le cube en 3d (1 face à la fois)
        cube(points_list_2d,face,ordre,couleur)

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


def zoom(points_list):
    """ agrandi le cube"""
    nvx_points_list=[]
    zoom=2
    for i in points_list:
        x=i[0]*zoom
        y=i[1]*zoom
        z=i[2]*zoom
        nvx_points_list.append( (x, y, z) )
    return nvx_points_list


def main():
    """execute le prgm"""
    points_list = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                  (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)]
    
    points_list=zoom(points_list)

    face=[(0,1,2,3),(0,1,5,4),(0,3,7,4),
           (1,2,6,5),(7,6,2,3),(7,6,5,4)]
    couleur=['red','blue','violet', 'green', 'yellow', 'black']
    affichage(points_list,face,couleur)


# Progamme principal
if __name__=='__main__':
    main()