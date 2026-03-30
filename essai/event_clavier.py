from tkinter import *

fenetre = Tk()

# Va voir la video (avec le lien) elle explique comment utiliser les touches pour avancer un perso par exemple
# https://www.youtube.com/watch?v=GsbLSDc2j8o

def press(event):
    """ permet de savoir quelle touches sont enfoncés 
    et les traduit en vecteur mouvement"""
    if event.keysym=='Up':
        mouvement[0]=1
    if event.keysym=='Down':
        mouvement[0]=-1
    if event.keysym=='Right':
        mouvement[1]=1
    if event.keysym=='Left':
        mouvement[1]=-1

    print(mouvement)
    print('--')
    return mouvement

def release(event):
    if event.keysym=='Up':
        mouvement[0]=0
    if event.keysym=='Down':
        mouvement[0]=0
    if event.keysym=='Left':
        mouvement[1]=0
    if event.keysym=='Right':
        mouvement[1]=0

mouvement=[0,0]

mouvement=fenetre.bind_all('<KeyPress>',press)
mouvement=fenetre.bind_all('<KeyRelease>',release)

fenetre.mainloop()
