import pygame
from math import cos, sin, pi, sqrt, tan, acos

"""
Le programme à été fait seulement avec les notions de maths de première 
et terminale (produit scalaire, normale d'un plan, droite paramétrée...)
et de nsi de première (tri, list, performance des algos...)
et sans aide extérieure

On peut faire bouger le rubiks cube avec les lettres a,z,e,q,s,d
et le faire tourner sur lui-même k,l,m,i,o,p

on peut faire tourner des parties du cube en cliquant sur 2 faces de
la section que l'on veux tourner (click gauche)"""



def matrice(point, matrice_rotation):
    """ renvoie les coordonnes du point en passant par la matrice de rotation"""
    nvx_point = [0,0,0]
    l = len(point)
    for i in range(l):
        for j in range(l):
            nvx_point[i] += point[j]*matrice_rotation[3*i+j]
    nvx_point = [round(nvx_point[i],12) for i in range(3)]
    return nvx_point


def coordonne(point, angle, rot_X, rot_Y, rot_Z):
    """ retourne les nouvelles coordonnes du point avec une rotation 
    d'angle 'angle' """
    rotation_x = [1.0,      0.0,      0.0,
                0.0, cos(angle), -sin(angle),
                0.0, sin(angle), cos(angle)]
    
    rotation_y = [cos(angle), 0.0, -sin(angle),
                    0.0,      1.0,      0.0,
                sin(angle), 0.0, cos(angle)]
    
    rotation_z = [cos(angle), -sin(angle), 0.0,
                sin(angle), cos(angle), 0.0,
                    0.0,      0.0,      1.0] 
    #tout les axes
    if rot_Z is True:
        point = matrice(point, rotation_z)
    if rot_Y is True:
        point = matrice(point, rotation_y)
    if rot_X is True:
        point = matrice(point, rotation_x)
    return point
    

def mouvement(all_face, angle_tour, rot_X, rot_Y, rot_Z):
    """ applique les nouvelles coordonnees aux points/normal de l'objet """
    tt_nvx_all_face = []
    for face in all_face:
        pts = face[0:4]
        nvx_all_face = [coordonne(pts[i], angle_tour, rot_X, rot_Y, rot_Z) for i in range(len(pts))]
        nvx_all_face += face[-2:]
        tt_nvx_all_face.append(nvx_all_face)
    return tt_nvx_all_face


def mouvement_point(all_points, angle_tour, rot_X, rot_Y, rot_Z):
    """ applique les nouvelles coordonnees aux points/normal de l'objet """
    tt_nvx_all_points = []
    for point in all_points:
        nvx_all_points = coordonne(point, angle_tour, rot_X, rot_Y, rot_Z) 
        tt_nvx_all_points.append(nvx_all_points)
    return tt_nvx_all_points


def in2d_parameter(all_face, camera, mur):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation des droites parametrees"""
    nvx_all_face = []
    for face in all_face:
        pts = face[0:4]
        nvx_points_list = []
        for i in pts:
            inverse_alpha = (mur[2]-camera[2])/(i[2]-camera[2])
            vector_plan_y = inverse_alpha*(i[1]-camera[1])
            vector_plan_x = inverse_alpha*(i[0]-camera[0])
            
            point_projection = (round(camera[0]+vector_plan_x ,15),
                            round(camera[1]+vector_plan_y ,15)) 
            nvx_points_list.append(point_projection)

        nvx_points_list += face[-2:]
        nvx_all_face.append(nvx_points_list)
    return nvx_all_face
    

def make_face(div, face):
    """renvoie les 4 points pour chaque sub face crée"""
    all_face = []
    nbr_face = [i for i in range(0,len(face))]
    for coef in nbr_face:
        for y in range(div+1):
            for x in range(div+1):
                x1 = x+1
                y1 = y+1
                rect = (div+2)**2*coef
                face = ( ( x+y*(div+2) )+rect, ( x1+y*(div+2) )+rect,
                        ( x1+y1*(div+2) )+rect,( x+y1*(div+2) )+rect)
                all_face.append(face)
    return all_face
        

def separation_face(face, points_list, div):
    """permet de separer les faces du cube en plusieurs mini face avec un diviseur de face donnée
    renvoie les 4 points pour chaque sub_face et les coordonnees des points"""
    tt_points = []
    for i in face:
        Vect_abs = [points_list[i[1]][0]-points_list[i[0]][0],
                  points_list[i[1]][1]-points_list[i[0]][1],
                  points_list[i[1]][2]-points_list[i[0]][2]]
        Vect_abs = [i/(div+1) for i in Vect_abs]
        
        Vect_ord = [points_list[i[3]][0]-points_list[i[0]][0],
                  points_list[i[3]][1]-points_list[i[0]][1],
                  points_list[i[3]][2]-points_list[i[0]][2]]
        Vect_ord = [i/(div+1) for i in Vect_ord]
        
        for y in range(div+2):
            Vect_ord_2 = [i*y for i in Vect_ord]
            for x in range(div+2):
                Vect_abs_2 = [i*x for i in Vect_abs]
                sub_point = [points_list[i[0]][0]+Vect_ord_2[0]+Vect_abs_2[0],
                           points_list[i[0]][1]+Vect_ord_2[1]+Vect_abs_2[1],
                           points_list[i[0]][2]+Vect_ord_2[2]+Vect_abs_2[2]]
                tt_points.append(sub_point)
    return tt_points


def mini_face(face, points_list, div, color):
    tt_face = []
    all_face = make_face(div, face)
    tt_points = separation_face(face, points_list, div)
    nb_col = 0
    for i in all_face:
        face = [tt_points[i[0]],tt_points[i[1]],tt_points[i[2]],tt_points[i[3]],nb_col]
        face += [color[ nb_col//((div+1)**2) ]]
        tt_face.append(face)
        nb_col += 1
    return tt_face
 

def dist_cam_face(all_face, camera):
    """renvoie l'ordre de remplissage des faces (de la plus loin 
    à la plus proche) en fonction de la localisation du point central 
    de la face par rapport à la camera"""
    face_ordre = []
    for face in all_face:
        centroid = [(face[0][0]+face[1][0]+face[2][0]+face[3][0])/4,
                (face[0][1]+face[1][1]+face[2][1]+face[3][1])/4,
                (face[0][2]+face[1][2]+face[2][2]+face[3][2])/4]
        distance_cam_centor = camera[2]-centroid[2]
        face_ordre.append( (distance_cam_centor, face) )

    #on trie les faces à dessiner en premier
    face_ordre.sort( key=lambda x: x[0],reverse=True)
    nvx_ordre_face=[i[1] for i in face_ordre]
    return nvx_ordre_face


def rectification (all_face, res_fenetre, zoom):
    """recentre le cube au centre de la fenetre"""
    nvx_all_face = []
    for face in all_face:
        pts = face[0:4]
        nvx_sub_face = []
        for i in pts:
            x = zoom*i[0] + res_fenetre[0]/2
            y = zoom*i[1] + res_fenetre[1]/2
            nvx_sub_face.append( [x,y] )    
        nvx_sub_face+=face[-2:]
        nvx_all_face.append(nvx_sub_face)
    return nvx_all_face


def dot_product(vect2,vect1):
    """ fait le dot_product de 2 vecteurs et renvoie la valeur """
    valeur = vect2[0]*vect1[0]+vect2[1]*vect1[1]+vect2[2]*vect1[2]
    return round(valeur, 10)


def dot_product_2d(vect2,vect1):
    """ fait le dot_product de 2 vecteurs et renvoie la valeur """
    valeur = vect2[0]*vect1[0]+vect2[1]*vect1[1]
    return round(valeur, 10)


def shadow(vect_normal, light, couleur):
    """permet d'assombrir les faces qui sont opposés à la source de lumière"""
    #vect_light_base = [0,0,-10]
    coef = sqrt(vect_normal[0]**2+vect_normal[1]**2+vect_normal[2]**2)*sqrt(light[0]**2+light[1]**2+light[2]**2)
    rate = 0.6 -0.4*dot_product(vect_normal,light)/coef
    # on fait la fonction darken ici (cf voir les autres ESSAI) 
    s = [i*rate for i in couleur]
    return s


def show_face(all_face, camera, div):
    """ permet de retourner les seules faces à afficher"""
    face_see = []
    i = 0
    for face in all_face:
        vect_ord = [face[1][0]-face[0][0],
                    face[1][1]-face[0][1],
                    face[1][2]-face[0][2]]
        
        vect_abs = [face[3][0]-face[0][0],
                    face[3][1]-face[0][1],
                    face[3][2]-face[0][2]]
        
        vect_normal = [vect_ord[1]*vect_abs[2] - vect_ord[2]*vect_abs[1],
                    vect_ord[2]*vect_abs[0] - vect_ord[0]*vect_abs[2],
                    vect_ord[0]*vect_abs[1] - vect_ord[1]*vect_abs[0]]

        # on flip la normal car elles sont mélangés
        normal = i//((div+1)**2)
        if normal==0 or normal==2 or normal==5: 
            vect_normal=[-i for i in vect_normal]
        
        vect_cam_face=[face[0][0] - camera[0],
                        face[0][1] - camera[1],
                        face[0][2] - camera[2]]
        i+=1
        if dot_product( vect_cam_face, vect_normal )>0:
            pt_light=(0,0,10)
            vec_light=[pt_light[0]-face[0][0],
                        pt_light[1]-face[0][1],
                        pt_light[2]-face[0][2]]
            
            color = shadow(vect_normal, vec_light, face[-1])
            nvx_face = face[0:5] + [color]
            face_see.append(nvx_face)     
    return face_see


def tt_transformation(all_face, res_fenetre, div, mouv_cote, mouv_hauteur, mouv_longueur, x, y, z):
    """permet de faire toute les transformation necessaire pour afficher le cube"""
    camera = (0, 0, 10)
    mur = (0, 0, 2)  # le mur est sur l'axe des x
    zoom = 80

    face = mouvement(all_face, mouv_hauteur, True, False, False)
    face = mouvement(face, mouv_longueur, False, False, True)
    face = mouvement(face, mouv_cote, False, True, False)
    face=position_obj(x, y, z, face)

    face_visible = show_face(face, camera, div)
    #face_visible = 
    face_visible = dist_cam_face(face_visible, camera)
    
    face_visible_2d = in2d_parameter(face_visible, camera, mur)
    face_visible_2d = rectification(face_visible_2d, res_fenetre, zoom)
    return face_visible_2d


def position_obj(x, y, z, all_face):
    """ deplace l'origine de l'objet dans le monde"""
    
    for face in all_face:
        for j in range(0,4):
            face[j][0]=face[j][0]+x
            face[j][1]=face[j][1]+y
            face[j][2]=face[j][2]+z
    return all_face


def recognition(x_souris, y_souris, face_visible_2d):
    """permet de retrouver sur quel face est attribué le clic de la souris"""
    approx = 0.01
    for face_2d in face_visible_2d:
        vect1 = [face_2d[0][0]-x_souris,face_2d[0][1]-y_souris]
        vect2 = [face_2d[1][0]-x_souris,face_2d[1][1]-y_souris]
        vect3 = [face_2d[2][0]-x_souris,face_2d[2][1]-y_souris]
        vect4 = [face_2d[3][0]-x_souris,face_2d[3][1]-y_souris]

        angle1 = acos(dot_product_2d(vect1,vect2) / ( sqrt(vect1[0]**2+vect1[1]**2) * sqrt(vect2[0]**2+vect2[1]**2) ))
        angle2 = acos(dot_product_2d(vect3,vect2) / ( sqrt(vect3[0]**2+vect3[1]**2) * sqrt(vect2[0]**2+vect2[1]**2) ))
        angle3 = acos(dot_product_2d(vect3,vect4) / ( sqrt(vect3[0]**2+vect3[1]**2) * sqrt(vect4[0]**2+vect4[1]**2) ))
        angle4 = acos(dot_product_2d(vect1,vect4) / ( sqrt(vect1[0]**2+vect1[1]**2) * sqrt(vect4[0]**2+vect4[1]**2) ))
        angle_final = angle1 + angle2 + angle3 + angle4
        angle_final = angle_final - 2*pi
        if -approx < angle_final and angle_final < approx:
            return face_2d[4]


def get_the_cube(liste):
    """renvoi les coordonnées du mini cube en tant que nom de ces facettes
    permet la rotation lorsque l'on clique"""
    face_link=[
    ### POUR LES Z = 1
    [4, [0,0,1]], [5,28, [1,0,1]], [10,1, [0,1,1]], [7,43, [0,-1,1]], [19,3, [-1,0,1]], [11,2,27, [1,1,1]],
    [9,18,0, [-1,1,1]], [8,29,44, [1,-1,1]], [20,6,42, [-1,-1,1]],
    ### POUR LES Z = 0
    [22, [-1,0,0]], [13, [0,1,0]], [40, [0,-1,0]], [31, [1,0,0]], [23,39, [-1,-1,0]], [32,41, [1,-1,0]],
    [21,12, [-1,1,0]], [14,30, [1,1,0]], 
    ### POUR LES Z = -1
    [49, [0,0,-1]], [50,34, [1,0,-1]], [25,48, [-1,0,-1]], [16,52, [0,1,-1]], [46,37, [0,-1,-1]],
    [17,53,33, [1,1,-1]], [51,24,15, [-1,1,-1]], [47,35,38, [1,-1,-1]], [45,26,36, [-1,-1,-1]] ]

    for face in liste:
        for id in face_link:
            if face[4] in id:
                face[4] = id[-1]
                break
    return liste


def axis_difference(loc1, loc2):
    """ permet de trouver sur quelle axe il faut tourner la face et dans quelle sens"""
    axis=[]
    for i in range(3):
        if loc1[i] == loc2[i]:
            axis.append(i)
            axis.append(1) # pour l'instant c'est ca mais il faut avoir un sens 
            return axis


def choose_rotation(all_face, face_clic):
    """ permet de trouver la rotation en fonction des faces cliqué"""
    turn = []
    face_a_tourner = []
    #cherche l'axe différent entre les faces cliqué
    axis = axis_difference(face_clic[0], face_clic[1])
    if axis[0] == 2:
        turn.append([False, False, True])
    elif axis[0] == 1:
        turn.append([False, True, False])
    else:
        turn.append([True, False, False])
    turn.append(axis[1])

    rangee = face_clic[0][axis[0]]
    for face in all_face:
        if face[4][axis[0]] == rangee:
            face_a_tourner.append(face[4])
    turn=turn[0:3] + [face_a_tourner]
    return turn


def sans_recurrence(turn):
    """retourne la liste de turn sans recurrence"""
    nvx_turn=[]
    for turn_1 in turn:
        if turn_1 not in nvx_turn:
            nvx_turn.append(turn_1)
    return nvx_turn


def application_mouvement(all_face, turn, info_rot, angle_tour):
    """permet d'appliquer la rotation dicté par l'utilisateur"""
    orientation, rot_x, rot_y, rot_z = info_rot[0], info_rot[1], info_rot[2], info_rot[3]
    if len(turn) != 0:
        for i in turn:
            if i[1] != 30:
                for nbr_face in range(len(all_face)):
                    if all_face[nbr_face][4] == i[0]:                              
                        pre_face = mouvement_point( all_face[nbr_face][0:4] , orientation*angle_tour,  rot_x, rot_y, rot_z)
                        all_face[nbr_face] = pre_face + all_face[nbr_face][4:]    
                i[1] += 1

            else:
                turn= [i[0] for i in turn]
                # change le nom des faces tournées
                if rot_x is True or rot_z is True:
                    orientation = -orientation
                    
                for nbr_face in range(len(all_face)):
                    if all_face[nbr_face][4] in turn:
                        pre_nom_face= mouvement_point( [all_face[nbr_face][4]], orientation*pi/2,  rot_x, rot_y, rot_z)
                        pre_nom_face = [int(i) for i in pre_nom_face[0]]
                        all_face[nbr_face][4] = pre_nom_face + [2]

                for nbr_face in range(len(all_face)):
                     all_face[nbr_face][4] =  all_face[nbr_face][4][0:3]

                turn = []
    return all_face, turn
    
def tri_random(all_face, nbr):
    """ permet de mélanger le cube avant de jouer"""
    
    return all_face

def affichage(all_face, res_fenetre, div):
    """fait tourner le carré 
    points_list: list de tuple"""
    run = True
    clock = pygame.time.Clock()
    angle_tour = pi/60
    sensi = 0.1
    turn = []
    face_clic = []
    face_turn = []
    
    key_o, key_l, key_m, key_k, key_i, key_p = 0, 0, 0, 0, 0, 0
    key_z, key_s, key_d, key_q, key_a, key_e = 0, 0, 0, 0, 0, 0  
    mouv_hauteur, mouv_cote, mouv_longueur = 0, 0, 0
    x_mouv, y_mouv, z_mouv = 0, 0, 0
    info_rot=[1, False, False, False]
    
    all_face = tri_random(all_face, 10)
    while run is True:
        # permet d'afficher le cube en 3d 
        face_visible_2d = tt_transformation(all_face, res_fenetre, div, mouv_cote, mouv_hauteur, mouv_longueur, x_mouv ,y_mouv ,z_mouv)
        cube (face_visible_2d)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 2: # clic bouton droit et milieu(pavé) de la souris 
                    x, y = pygame.mouse.get_pos()
                    face = recognition(x, y, face_visible_2d)
                    if face is not None:
                        face_clic.append(face)
                                  

            if event.type == pygame.KEYUP:
                #pour faire pivoter l'objet
                if event.key == pygame.K_o:
                    key_o=0
                if event.key == pygame.K_l:
                    key_l=0
                if event.key == pygame.K_m:
                    key_m=0
                if event.key == pygame.K_k:
                    key_k=0
                if event.key == pygame.K_i:
                    key_i=0
                if event.key == pygame.K_p:
                    key_p=0

                #pour faire bouger la camera
                if event.key == pygame.K_z:
                    key_z=0
                if event.key == pygame.K_s:
                    key_s=0
                if event.key == pygame.K_d:
                    key_d=0
                if event.key == pygame.K_q:
                    key_q=0
                if event.key == pygame.K_a:
                    key_a=0
                if event.key == pygame.K_e:
                    key_e=0

            if event.type == pygame.KEYDOWN:
                #pour faire pivoter l'objet
                if event.key == pygame.K_o:
                    key_o=1
                elif event.key == pygame.K_l:
                    key_l=1
                elif event.key == pygame.K_m:
                    key_m=1
                elif event.key == pygame.K_k:
                    key_k=1
                elif event.key == pygame.K_i:
                    key_i=1
                elif event.key == pygame.K_p:
                    key_p=1

                #pour faire bouger la camera
                if event.key == pygame.K_z:
                    key_z=1
                elif event.key == pygame.K_s:
                    key_s=1
                elif event.key == pygame.K_d:
                    key_d=1
                elif event.key == pygame.K_q:
                    key_q=1
                elif event.key == pygame.K_a:
                    key_a=1
                elif event.key == pygame.K_e:
                    key_e=1
                

        dmd_mouvement = key_o+key_l+key_m+key_k+key_i+key_p+key_z+key_s+key_d+key_q+key_a+key_e  
        if dmd_mouvement == 0:
            #choix de la rotation 
            if len(face_clic) == 2:
                face_turn = choose_rotation(all_face, face_clic)
                face_clic = []
                
            # permet d'appliquer la rotation
            if len(face_turn) != 0:
                for nbr_face in range(len(all_face)):
                    if all_face[nbr_face][4] in face_turn[2]:
                        turn.append( [all_face[nbr_face][4],0] )
                turn = sans_recurrence(turn)
                rot_x, rot_y, rot_z = face_turn[0][0], face_turn[0][1], face_turn[0][2]
                orientation = face_turn[1]
                info_rot = [orientation, rot_x, rot_y, rot_z]
                face_turn = []

            # application de la rotation
            all_face, turn = application_mouvement(all_face, turn, info_rot, angle_tour)
        
        # pour pouvoir faire changer d'endroit l'objet
        x_mouv += key_q*sensi - key_d*sensi
        y_mouv += key_z*sensi - key_s*sensi
        z_mouv += key_e*sensi - key_a*sensi
        
        # pour les touches 'o' et 'l'
        mouv_hauteur = (mouv_hauteur+key_l*angle_tour - key_o*angle_tour) %(2*pi)
        # pour les touches 'k' et 'm'
        mouv_cote = (mouv_cote+key_m*angle_tour - key_k*angle_tour) %(2*pi)
        # pour les touches 'i' et 'p'
        mouv_longueur = (mouv_longueur+key_i*angle_tour - key_p*angle_tour) %(2*pi)
        
        clock.tick(100) # maximum de ___ d'images par seconde
    pygame.quit() 


def cube (all_face):
    """dessine le rubic sur pygame """
    screen.fill( (40,40,40) )
    for face in all_face: #permet de dessiner toute les facettes
        print_face = face[0:4]
        print_couleur = face[-1]
        pygame.draw.polygon(screen, print_couleur, print_face)
        pygame.draw.polygon(screen, (0,0,0), print_face, 1)
    pygame.display.update()


def main():
    # coordonée des sommets du cube
    points_list = [[-3, -3, 3], [3, -3, 3], [3, 3, 3], [-3, 3, 3],
                [-3, -3, -3], [3, -3, -3], [3, 3, -3], [-3, 3, -3]]
    

    # face composé de 4 sommets
    face = [(0,1,2,3),(0,1,5,4),(0,3,7,4),
            (1,2,6,5),(7,6,2,3),(7,6,5,4)]

    # couleur du rubik's cube
    couleur = [(200,200,200), (0,200,0), (200,0,0), (255,120,0), 
                (0,0,200), (200,200,0)]
    

    # redivise les faces en 9 sous faces (rubikscube)
    div = 2
    nvx_face = mini_face(face, points_list, div, couleur)
    nvx_face = get_the_cube(nvx_face)

    res_fenetre = (700,700)
    pygame.display.set_caption("rubick's cube loader")
    global screen
    screen = pygame.display.set_mode(res_fenetre)
    affichage(nvx_face, res_fenetre, div)
    
# Progamme principal
if __name__ == '__main__':
    main()