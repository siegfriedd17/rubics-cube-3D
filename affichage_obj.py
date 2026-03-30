import pygame 
#import csv

def in2d_parameter(points_list, camera, mur):
    """transformes the coordinates of the points from 3d to 2d
    the camera coordinates are in variable and the wall is 'mur'
    Utilisation des droites parametrees"""
    nvx_points_list = []
    mur = [2,0,0]  # le mur est sur l'axe des x
    for i in points_list:
        inverse_alpha=(mur[0]-camera[0])/(i[0]-camera[0])
        vector_plan_y=inverse_alpha*(i[1]-camera[1])
        vector_plan_z=inverse_alpha*(i[2]-camera[2])
        
        point_projection=( (round(camera[1]+vector_plan_y ,12),
                          round(camera[2]+vector_plan_z ,12)) )
        nvx_points_list.append(point_projection)
    return nvx_points_list

def cube(points_list_2d, face, ordre):
    """dessine un cube 3d """

    screen.fill( (255,255,255) )
    for h in ordre: #permet de dessiner 6 faces
        coord=[points_list_2d[i-1] for i in face[h]]
        pygame.draw.polygon(screen, (0, 0, 0), coord,width=1)
    pygame.display.update()

def rectification(points_list_2d, res_fenetre, zoom):
    """recentre le cube au centre de la fenetre"""
    nvx_points_list=[]
    for i in points_list_2d:
        x=zoom * i[0]+res_fenetre[0]/10
        y=zoom * i[1]+res_fenetre[1]/3
        nvx_points_list.append( [x, y] )
    return nvx_points_list


def vertex(string):
    """ permet d'obtenir les points"""
    point=[]
    nvx_point=[[0,0,0]]
    for i in string:
        c=string.find('\n')
        point.append(string[2:c-1])
        string=string[c+1:]
        if c==-1:
            break
    for i in point:
        c=i.split()
        nvx_point.append( [float(i) for i in c] )
    return nvx_point

def normal(string):
    """ permet d'obtenir les points"""
    point=[]
    nvx_point=[]
    for i in string:
        c=string.find('\n')
        point.append(string[2:c-1])
        string=string[c+1:]
        if c==-1:
            break
    for i in point:
        c=i.split()
        nvx_point.append( [float(i) for i in c] )
    return nvx_point

def face(string):
    """ permet d'avoir les faces à afficher"""
    face=[]
    nvx_face=[]
    for i in string:
        c=string.find('\n')
        face.append(string[2:c])
        string=string[c+1:]
        if c==-1:
            break
    for i in face:
        c=i.split()
        triangle=[]
        for i in c:
            k=i.split('/')
            k=[int(i) for i in k]
            triangle.append(k)
        nvx_face.append( triangle )
    return nvx_face


def conversion_obj(file):
    """convertit le fichier obj en deux list
    list_point et list_face"""
    str_file= file.read()

    g=str_file.find('v ')
    c=str_file.find('vt')
    list_point=str_file[g:c-1]
    list_point=vertex(list_point)
    
    d=str_file.find('f ')
    list_face=str_file[d:]
    list_face=face(list_face)
    list_face=list_face[:-1]
    list_face=[i[0] for i in list_face]
    

    t=str_file.find('vn ')
    r=str_file.find('usemtl')
    list_normal=str_file[t:r]
    list_normal=normal(list_normal)[:-1]

    
    return list_face, list_point


def dist_camera_faces(points_list, list_face, camera):
    """renvoie l'ordre de remplissage des faces (de la plus loin 
    à la plus proche) en fonction de la localisation du point central 
    de la face par rapport à la camera"""
    ordre=0
    pts_centor=[]
    for i in list_face:
        tt_pts_x=0
        for j in i:
            #print(points_list[j-1])
            tt_pts_x+=points_list[j-1][0]
        tt_pts_x=tt_pts_x/len(i)
        
        distance_cam_centor=camera[0]-tt_pts_x        
        pts_centor.append( (distance_cam_centor, ordre) )
        ordre+=1
    #on trie les faces à dessiner en premier
    pts_centor.sort( key=lambda x: x[0],reverse=True)
    ordre_face=[i[1] for i in pts_centor]
    return ordre_face


def main():
    """permet l'affichage de l'object en 3d """
    res_fenetre=(800,600)
    camera = (10, 0, 0)
    mur = (2, 0, 0)  # le mur est sur l'axe des x

    list_face, list_point = conversion_obj(file)
    
    nvx_list_point=in2d_parameter(list_point, camera, mur)
    nvx_list_point=rectification(nvx_list_point, res_fenetre, zoom)
    ordre=dist_camera_faces(nvx_list_point, list_face, camera)

    pygame.display.set_caption("3D projection in pygame!")
    global screen
    screen = pygame.display.set_mode((res_fenetre[0], res_fenetre[1]))

    cube(nvx_list_point, list_face, ordre)

    pygame.time.delay(100)
    pygame.quit()


file = open("cube.obj", "r", encoding="utf8")
zoom=60
main()