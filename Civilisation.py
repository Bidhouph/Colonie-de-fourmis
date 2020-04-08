#-*- coding: utf-8 -*-

from Ville import Ville
from Route import Route
from Ant import Ant
from Tkinter import *
from random import randint,random

class Civilisation :
    def __init__(self):
        self.rho=0.001 # float (taux d'evaporation des pheromones)
        self.villes=[] # [ville]
        self.nville=0
        self.routes=[] # [route]
        self.nid=None # ville
        self.source=None # ville
        self.ants=None # [ant]
        self.nants=50
        self.lifeSpan=200 # temps de vie moyen des fourmis
        self.tempSimu=300

        # Proprietes graphiques
        self.window=Tk()

        # Options
        self.opFrame = Frame(self.window)
        self.but1 = Button(self.opFrame,text="Exemple",command=self.defaultSetup)
        self.but1.grid(row=0,column=1)
        self.but2 = Button(self.opFrame,text="Lancer (espace)",command=self.run)
        self.but2.grid(row=0,column=2)
        self.but3 = Button(self.opFrame,text="Aide",command=self.help)
        self.but3.grid(row=0,column=3)
        self.but4 = Button(self.opFrame,text="Reset",command=self.reset)
        self.but4.grid(row=0,column=4)
        self.opFrame.pack()

        # Canvas
        self.can=Canvas(self.window,width=800, height=800)

        self.dx=10 # demi largeur des villes
        self.pressTemps=(-1000,-1000) # variable temporaire pour les routes
        self.villeTemps=(0,0) # variable temporaire pour les villes

        # Pour entrer le nom des villes
        self.entry = Entry(self.can)
        self.button = None
        self.popup = None
        self.popup2 = None

        # binding des clics et touches
        self.can.pack()
        self.can.bind("<ButtonPress-1>",lambda event : self.lpress(event))
        self.can.bind("<ButtonRelease-1>",lambda event : self.lrelease(event))
        self.can.bind("<Button-3>",lambda event : self.rclic(event))
        self.window.bind("<space>",lambda event : self.run())


    def evapore(self):
        for route in self.routes:
            route.evapore(rho)

    def addVille(self,ville):
        self.villes.append(ville)
        self.villes[-1].affiche()

    def createNewVille(self,x,y):
        self.villeTemps=(x,y)
        self.entry.pack()
        self.button=Button(self.can,text='OK',command=self.callback)
        self.popup=self.can.create_window((x,y-15),window = self.entry)
        self.popup2=self.can.create_window((x,y+15),window = self.button)
        self.entry.focus_set()

    def callback(self):
        text=self.entry.get()
        self.can.delete(self.popup)
        self.can.delete(self.popup2)
        self.addVille(Ville(self,self.villeTemps[0],self.villeTemps[1],text))

    def addRoute(self,route):
        self.routes.append(route)
        self.routes[-1].affiche()

    def affiche(self):
        self.window.mainloop()

    def rclic(self,event):
        v1 = self.quelleVille(event.x,event.y)
        if (v1 != None and self.nid==None):
            v1.setNid()
        elif (v1 != None and self.source==None):
            v1.setSource()

    def lpress(self,event):
        v1 = self.quelleVille(event.x,event.y)
        if (v1==None):
            self.createNewVille(event.x,event.y)
        self.pressTemp=(event.x,event.y)

    def lrelease(self,event):
        v1=self.quelleVille(self.pressTemp[0],self.pressTemp[1])
        v2=self.quelleVille(event.x,event.y)
        if (v1 != None and v2 != None and v1 != v2):
            self.addRoute(Route(self,v1,v2))
        self.pressTemp=None

    def quelleVille(self,x,y):
        for ville in self.villes:
            if (abs(ville.x-x)<=self.dx and abs(ville.y-y)<=self.dx):
                return ville
        return None

    def defaultSetup(self):
        # La geographie
        self.addVille(Ville(self,30,30,"Source"))
        self.addVille(Ville(self,130,360,"Ville 1"))
        self.addVille(Ville(self,400,280,"Ville 2"))
        self.addVille(Ville(self,100,600,"Ville 3"))
        self.addVille(Ville(self,500,550,"Ville 4"))
        self.addVille(Ville(self,700,750,"Objectif"))
        self.addVille(Ville(self,350,500,"Ville 5"))
        self.villes[0].setNid()
        self.villes[5].setSource()
        self.addRoute(Route(self,self.villes[0],self.villes[1]))
        self.addRoute(Route(self,self.villes[0],self.villes[2]))
        self.addRoute(Route(self,self.villes[3],self.villes[5]))
        self.addRoute(Route(self,self.villes[4],self.villes[5]))
        self.addRoute(Route(self,self.villes[2],self.villes[3]))
        self.addRoute(Route(self,self.villes[2],self.villes[4]))
        self.addRoute(Route(self,self.villes[1],self.villes[3]))
        self.addRoute(Route(self,self.villes[3],self.villes[6]))

        # Les fourmis
        self.ants=[Ant(self,4*random(),4*random(),4*random(),self.lifeSpan) for _ in range (self.nants)]

    def updatePhero(self):
        for route in self.routes:
            route.updatePhero()

    def run(self):
        self.nville=len(self.villes)
        for frame in range(self.tempSimu):
            # Les fourmis se deplacent et on tue les perdantes
            print('tour '+str(frame))
            i=0
            while(i<len(self.ants)):
                if (self.ants[i].alive):
                    self.ants[i].move()
                    i+=1
                else:
                    self.ants.pop(i)

            # On repeuple
            if (len(self.ants)>=1):
                nenfant=self.nants-len(self.ants)
                newpop=[]
                for i in range(nenfant):
                    parent1,parent2=self.ants[randint(0,len(self.ants))-1],self.ants[randint(0,len(self.ants))-1]
                    newpop.append(Ant(self,(parent1.alpha+parent2.alpha)/2,(parent1.beta+parent2.beta)/2,(parent1.gamma+parent2.gamma)/2,self.lifeSpan))
                self.ants=self.ants+newpop
            else:
                print('Population morte !')
                break
        self.updatePhero()

    def help(self):
        win = Tk()
        Label(win,text="Bonjour.\n Ce programme implémente un algorithme de colonie de fourmis couplé d'un algorithme génétique\npour la recherche de chemin le plus court dans un graphe.\n\n -> Le bouton 'Exemple' permet de charger un ensemble de villes et routes préenregistré.\n -> Cliquer sur le Canevas permet de créer une ville, en choisissant un nom.\n -> Maintenir le clic d'une ville à une autre crée une route entre les deux.\n -> Un premier clic droit sur une ville crée un nid.\n -> Un deuxième clic droit sur une ville crée un objectif.\n -> Pour lancer la simulation appuyer sur 'espace' ou cliquer sur 'Lancer'.\n -> Le bouton 'Reset' permet d'effacer toutes les villes et routes.").pack()

    def reset(self):
        self.can.delete('all')
        self.villes=[] # [ville]
        self.nville=0
        self.routes=[] # [route]
        self.nid=None # ville
        self.source=None # ville
        self.ants=None # [ant]
        self.nants=50
