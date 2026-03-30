# -*- coding: utf-8 -*-
"""
Created on Thu May  5 12:07:01 2022

@author: Delete
"""
import matplotlib.pyplot as plt
from math import cos, sin, pi
import random
import time


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
    points_list = [coordonne(points_list[i], angle_tour) for i in range(len(points_list))]
    return points_list


def in2d_Thales(points_list, camera, mur):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation of the theoreme of Thales"""
    nvx_points_list = {}
    rapport_cam_mur = camera[0]-mur[0]
    for i in points_list:
        dist = camera[0]-points_list[i][0]
        rapport = rapport_cam_mur/dist
        nvx_points_list.update( {i: (round(rapport*(points_list[i][1]-camera[1])+camera[1], 15),
                                round(rapport*(points_list[i][2]-camera[2])+camera[2], 15))} )
    return nvx_points_list


def in2d_parameter(points_list, camera,mur):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation des droites parametrees"""
    nvx_points_list = {}
    for i in points_list:
        
        inverse_alpha = (mur[0]-camera[0])/(points_list[i][0]-camera[0])
        vector_plan_y = inverse_alpha*(points_list[i][1]-camera[1])
        vector_plan_z = inverse_alpha*(points_list[i][2]-camera[2])
        
        point_projection={ i: (round(camera[1]+vector_plan_y ,15),
                          round(camera[2]+vector_plan_z ,15)) }
        nvx_points_list.update(point_projection)
    return nvx_points_list


def dist_camera_faces(points_list, face, camera):
    """renvoie l'ordre de remplissage des faces (de la plus loin 
    à la plus proche) en fonction de la localisation du point central 
    de la face par rapport à la camera"""
    ordre=0
    pts_centor=[]
    for i in face:
        pt_oppose=len(i)//2
        #calcule le vecteur(x,y,z) entre les points opposés d'une face 
        
        vector=[points_list.get(i[pt_oppose])[0] - points_list.get(i[0])[0],
                points_list.get(i[pt_oppose])[1] - points_list.get(i[0])[1],
                points_list.get(i[pt_oppose])[2] - points_list.get(i[0])[2]]
        vector=[i/2 for i in vector]
        
        #on obtient les coordonnees du point central de la face
        centor=(points_list.get(i[0])[0]+vector[0],
                points_list.get(i[0])[0]+vector[1],
                points_list.get(i[0])[0]+vector[2])
        distance_cam_centor=camera[0]-centor[0]
        pts_centor.append( (distance_cam_centor, ordre) )
        ordre+=1
    #on trie les faces à dessiner en premier
    pts_centor.sort( key=lambda x: x[0],reverse=True)
    ordre_face=[i[1] for i in pts_centor]
    return ordre_face


def cube(points_list_2d, nvx_face, ordre, couleur):
    """dessine un cube 3d """    
    for h in ordre: #permet de dessiner 6 faces
        pts=nvx_face[h]
        
        coord=[points_list_2d[i] for i in pts]
        x1 = [j[0] for j in coord] 
        y1 = [j[1] for j in coord]
        plt.fill(x1, y1, couleur[h])
        
    # permet de garder la même échelle en fonction des graphiques
    scale_graphique = 3
    plt.plot(scale_graphique, scale_graphique)
    plt.plot(-scale_graphique, -scale_graphique)
    #  Repère orthonormée
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.axis('equal')  
    plt.autoscale(False)
    
    plt.show() # affichage


def make_face(div):
    """renvoie les 4 points pour chaque sub face crée"""
    all_face=[]
    lettre_face=('a','b','c','d','e','f')
    for letter in lettre_face:
        for y in range(div+1):
            for x in range(div+1):
                x1=x+1
                y1=y+1
                face = ( str(str(x)+letter+str(y)), str(str(x1)+letter+str(y)),
                    str(str(x1)+letter+str(y1)), str(str(x)+letter+str(y1)) )
                all_face.append(face)
    return all_face
        

def separation_face(face, points_list, div):
    """permet de separer les faces du cube en plusieurs mini face avec un diviseur de face donnée
    renvoie les 4 points pour chaque sub_face et les coordonnees des points"""
    tt_points={}
    lettre_face=('a','b','c','d','e','f')
    indice_lettre=0
    for i in face:
        letter=lettre_face[indice_lettre]
        temp_points={}
        vect_abs=[points_list[i[1]][0]-points_list[i[0]][0],
                  points_list[i[1]][1]-points_list[i[0]][1],
                  points_list[i[1]][2]-points_list[i[0]][2]]
        vect_abs=[i/(div+1) for i in vect_abs]
        
        vect_ord=[points_list[i[3]][0]-points_list[i[0]][0],
                  points_list[i[3]][1]-points_list[i[0]][1],
                  points_list[i[3]][2]-points_list[i[0]][2]]
        vect_ord=[i/(div+1) for i in vect_ord]
        
        for y in range(div+2):
            vect_ord_2=[i*y for i in vect_ord]
            for x in range(div+2):
                vect_abs_2=[i*x for i in vect_abs]
                sub_point=(points_list[i[0]][0]+vect_ord_2[0]+vect_abs_2[0],
                           points_list[i[0]][1]+vect_ord_2[1]+vect_abs_2[1],
                           points_list[i[0]][2]+vect_ord_2[2]+vect_abs_2[2])
                
                temp_points.update( {str( str(x)+letter+str(y) ) : sub_point } )
        
        tt_points.update(temp_points)
        indice_lettre+=1

    return tt_points


def face_color(div):
    """renvoie une liste de couleur"""
    list_color=[]
    for i in range(6):
        rand_colors = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        list_color.append(rand_colors)
    list_color=list_color*(div+1)**2
    random.shuffle(list_color)
    return list_color


def zoom(points_list):
    """ agrandi le cube"""
    nvx_points_list=[]
    zoom=1
    for i in points_list:
        x=i[0]*zoom
        y=i[1]*zoom
        z=i[2]*zoom
        nvx_points_list.append( (x, y, z) )
    return nvx_points_list

    
def affichage(points_list, face, couleur, choix_3d, div):
    """fait tourner le carré 
    points_list: list de tuple"""
    tour = 0
    fps = 60
    angle_tour = pi/30
    rapprochement = 0
    
    nvx_face=make_face(div)
    
    # permet de faire 1 rotation à tant fps(c'est une variable)
    while tour <= fps:
        camera = (10+rapprochement, 0, 0)
        mur = (2+rapprochement,0,0)  # le mur est sur l'axe des x
        
        nvx_points_list = separation_face(face, points_list,div)
        
        ordre = dist_camera_faces(nvx_points_list, nvx_face, camera)
    
        if choix_3d == 0:
            points_list_2d = in2d_Thales(nvx_points_list, camera,mur)
        else:
            points_list_2d = in2d_parameter(nvx_points_list, camera,mur)

        # permet d'afficher le cube en 3d (1 face à la fois)
        cube (points_list_2d, nvx_face, ordre, couleur)

        points_list = mouvement(points_list, angle_tour)
        plt.pause (1/fps)
        tour += 1
        #rapprochement += -1/21


def main():
    """execute le prgm"""
    points_list = [(-1.0, -1.0, 1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0),
                      (-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, -1.0)]
    face = [(0,1,2,3),(0,1,5,4),(0,3,7,4),
               (1,2,6,5),(7,6,2,3),(7,6,5,4)]
    points_list=zoom(points_list)
    #print(points_list)
        
    #div=int(input("combien de sous face par face voulez vous: (max: 10)"))
    div=5
    couleur = face_color(div)
    #choix_3d = int(input("\nchoix de la fonction 3d:\n0=Thales / 1=Parameter "))
    choix_3d=1

    affichage(points_list, face, couleur, choix_3d,div)
    

# Progamme principal
if __name__=='__main__':
    start=time.time()
    main()
    end=time.time()
    print(end-start)