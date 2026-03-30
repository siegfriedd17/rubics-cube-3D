
from tkinter import *
from math import cos, sin, pi, sqrt
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
    
    rotation_y=[cos(3*angle), 0, -sin(3*angle),
                    0,      1,      0,
                sin(3*angle), 0, cos(3*angle)]
    
    rotation_z=[cos(2*angle), -sin(2*angle), 0,
                sin(2*angle), cos(2*angle), 0,
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
        """
        vector=[points_list.get(i[pt_oppose])[0] - points_list.get(i[0])[0],
                points_list.get(i[pt_oppose])[1] - points_list.get(i[0])[1],
                points_list.get(i[pt_oppose])[2] - points_list.get(i[0])[2]]
        vector=[i/2 for i in vector]
        
        #on obtient les coordonnees du point central de la face
        centor=(points_list.get(i[0])[0]+vector[0],
                points_list.get(i[0])[0]+vector[1],
                points_list.get(i[0])[0]+vector[2])

        distance_cam_centor=camera[0]-centor[0]
        """
        vector=(points_list.get(i[pt_oppose])[0] - points_list.get(i[0])[0])/2
        #on obtient les coordonnees du point central de la face
        centor=points_list.get(i[0])[0]+vector
        distance_cam_centor=camera[0]-centor

        
        pts_centor.append( (distance_cam_centor, ordre) )
        ordre+=1
    #on trie les faces à dessiner en premier
    pts_centor.sort( key=lambda x: x[0],reverse=True)
    ordre_face=[i[1] for i in pts_centor]
    return ordre_face


def make_face(div, face):
    """renvoie les 4 points pour chaque sub face crée"""
    all_face=[]
    lettre_face=lettre_face=[chr(i) for i in range(58,58+len(face))]
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
    lettre_face=[chr(i) for i in range(58,58+len(face))]
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


def matrix_color(matrix):
    """calcule la valeur de la matrice de couleur pour assombrir les faces"""
    return matrix[0]*matrix[3]-matrix[1]*matrix[2]

def dot_product_light(normal,light,coef):
    """ renvoi True ou False s'il faut assombrir la face en fonction de si la valeur du dot product 
    entre vecteur normal d'une face et celle de la source de lumière est négative ou non"""
    valeur=normal[0]*light[0]+normal[1]*light[1]+normal[2]*light[2]
    valeur=valeur/coef
    return valeur

def darken(rgb, rate):
    rgb=rgb[1::]
    s = '#'
    for i in [0,2,4]:
        c = rgb[i:i+2]
        c = int(c, 16)
        c = int(c * rate)
        c = format(c, '02x')
        s += c
    return s

def shadow(points_list, face, color, div):
    """permet d'assombrir les faces qui sont opposés à la source de lumière"""
    light=(-10,-10,-10)
    list_color=[]
    indice_couleur=0
    for i in face:
        vect_abs=[points_list[i[1]][0]-points_list[i[0]][0],
                  points_list[i[1]][1]-points_list[i[0]][1],
                  points_list[i[1]][2]-points_list[i[0]][2]]
        
        vect_ord=[points_list[i[3]][0]-points_list[i[0]][0],
                  points_list[i[3]][1]-points_list[i[0]][1],
                  points_list[i[3]][2]-points_list[i[0]][2]]

        vect_prod=vect_abs+vect_ord
        matrix_x=vect_prod[1:3]+vect_prod[4:6]
        matrix_y=[vect_prod[0],vect_prod[2],vect_prod[3],vect_prod[5]]
        matrix_z=vect_prod[0:2]+vect_prod[3:5]

        # les normal sont dans le sens inverse par rapport à la formule voir png
        vect_normal=(-matrix_color(matrix_x),
                    matrix_color(matrix_y),
                    -matrix_color(matrix_z))
        coef=sqrt(vect_normal[0]**2+vect_normal[1]**2+vect_normal[2]**2)*sqrt(light[0]**2+light[1]**2+light[2]**2)
        
        # permet de recalibrer la rate allant de 0 à 1 en fonction du cos(angle) qui va de -1 a 1
        rate= 0.6 -0.4*dot_product_light(vect_normal,light,coef)
        for i in range( (div+1)**2) :
            list_color.append( darken(color[i], rate) )

        indice_couleur += (div+1)**2
    return list_color

def face_color(div, points_list):
    """renvoie une liste de couleur"""
    list_color=[]
    for i in points_list:
        rand_colors = "#"+''.join([random.choice('ABCDE0123456789') for i in range(6)])
        list_color.append(rand_colors)
    list_color=list_color*(div+1)**2
    random.shuffle(list_color)
    return list_color


def rectification(points_list_2d, res_fenetre,zoom):
    """recentre le cube au centre de la fenetre"""
    nvx_points_list={}
    for key, value in points_list_2d.items():
        x=zoom*value[0]+res_fenetre[0]/2
        y=zoom*value[1]+res_fenetre[1]/2
        nvx_points_list.update( {key : (x,y)} )
    return nvx_points_list


def cube(points_list_2d, nvx_face, div, ordre, couleur, res_fenetre):
    """dessine un cube 3d """
    calque.delete("all")
    #permet d'enlever l'affichage de 1faces et demie => optimisation
    #ordre=ordre[int(3/2*(div+1)**2)::]
    #ordre=ordre[0:1] #tkinter est lent 
    for h in ordre: #permet de dessiner 6 faces
        nvx_coord=[]
        coord=[points_list_2d[i] for i in nvx_face[h]]
        for i in coord:
            nvx_coord.append(i[0])
            nvx_coord.append(i[1])
        calque.create_polygon(nvx_coord, fill=couleur[h])
    calque.update()


def affichage(points_list, face, couleur, choix_3d, div, res_fenetre,fenetre):
    """fait tourner le carré 
    points_list: list de tuple"""
    tour = 0
    fps = 60
    angle_tour = pi/30
    rapprochement = 0
    zoom=80
    
    nvx_face=make_face(div, face)
    # permet de faire 1 rotation à tant fps(c'est une variable)
    while tour <= fps:
        camera = (10+rapprochement, 0, 0)
        mur = (2+rapprochement,0,0)  # le mur est sur l'axe des x
        
        
        nvx_points_list = separation_face(face, points_list,div)
        couleur_fps = shadow(points_list, face, couleur, div)
        
        ordre = dist_camera_faces(nvx_points_list, nvx_face, camera)
    
        if choix_3d == 0:
            points_list_2d = in2d_Thales(nvx_points_list, camera,mur)
        else:
            points_list_2d = in2d_parameter(nvx_points_list, camera,mur)
        points_list_2d=rectification(points_list_2d, res_fenetre, zoom)

        # permet d'afficher le cube en 3d (1 face à la fois)
        cube (points_list_2d, nvx_face, div, ordre, couleur_fps, res_fenetre)
        points_list = mouvement(points_list, angle_tour)
        tour += 1
        time.sleep(0.1)
        #rapprochement += -1/21
    time.sleep(0.3)
    fenetre.destroy()


def main():
    """execute le prgm"""
    points_list = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                      (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)]
    face = [(0,1,2,3),(0,1,5,4),(0,3,7,4),
               (1,2,6,5),(7,6,2,3),(7,6,5,4)]

    #div=int(input("combien de sous face par face voulez vous: (max: 10)"))
    div=25
    couleur = face_color(div, points_list)
    #choix_3d = int(input("\nchoix de la fonction 3d:\n0=Thales / 1=Parameter "))
    choix_3d=1

    res_fenetre=(800,600)
    fenetre=Tk()
    fenetre.geometry(str(res_fenetre[0])+'x'+str(res_fenetre[1]))
    global calque
    calque = Canvas(fenetre,width=res_fenetre[0], height=res_fenetre[1], bg='white')
    calque.pack()
    
    affichage(points_list, face, couleur, choix_3d, div, res_fenetre, fenetre)
    fenetre.mainloop()
    

# Progamme principal
if __name__=='__main__':
    start=time.time()
    main()
    end=time.time()
    print("\n{} secondes\n".format(end-start))
    