from Ville import Ville
from Route import Route
from Ant import Ant
from Tkinter import *
from random import randint,random

class Civilisation :
    def __init__(self):
        self.rho=0.01 # float (taux d'evaporation des pheromones)
        self.villes=[] # [ville]
        self.nville=0
        self.routes=[] # [route]
        self.nid=None # ville
        self.source=None # ville
        self.ants=None # [ant]
        self.nants=100

        # Proprietes graphiques
        self.window=Tk()
        self.can=Canvas(self.window,width=800, height=800)
        self.can.pack()
        self.can.bind("<ButtonPress-1>",lambda event : self.lpress(event))
        self.can.bind("<ButtonRelease-1>",lambda event : self.lrelease(event))
        self.can.bind("<Button-3>",lambda event : self.rclic(event))
        self.window.bind("<Key>",lambda event : self.run())
        self.dx=10
        self.pressTemps=(-1000,-1000)

    def evapore(self):
        for route in self.routes:
            route.evapore(rho)

    def addVille(self,ville):
        self.villes.append(ville)
        self.villes[-1].affiche()

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
            self.addVille(Ville(self,event.x,event.y))
        self.pressTemp=(event.x,event.y)

    def lrelease(self,event):
        v1=self.quelleVille(self.pressTemp[0],self.pressTemp[1])
        v2=self.quelleVille(event.x,event.y)
        if (v1 != None and v2 != None):
            self.addRoute(Route(self,v1,v2))
        self.pressTemp=None

    def quelleVille(self,x,y):
        for ville in self.villes:
            if (abs(ville.x-x)<=self.dx and abs(ville.y-y)<=self.dx):
                return ville
        return None

    def defaultSetup(self):
        # La geographie
        self.addVille(Ville(self,30,30))
        self.addVille(Ville(self,130,360))
        self.addVille(Ville(self,400,280))
        self.addVille(Ville(self,100,600))
        self.addVille(Ville(self,500,550))
        self.addVille(Ville(self,700,750))
        self.villes[0].setNid()
        self.villes[-1].setSource()
        self.addRoute(Route(self,self.villes[0],self.villes[1]))
        self.addRoute(Route(self,self.villes[0],self.villes[2]))
        self.addRoute(Route(self,self.villes[3],self.villes[5]))
        self.addRoute(Route(self,self.villes[4],self.villes[5]))
        self.addRoute(Route(self,self.villes[2],self.villes[3]))
        self.addRoute(Route(self,self.villes[2],self.villes[4]))
        self.addRoute(Route(self,self.villes[1],self.villes[3]))

        # Les fourmis
        self.ants=[Ant(self,4*random(),4*random(),random()) for _ in range (self.nants)]

    def run(self):
        print('oui')

        # On effectue un certain nombre de tours
        self.nvillle=len(self.villes)
        for turn in range(self.nville):
            for ant in self.ants :
                ant.move()

        # On tue les perdantes
        i=0
        while (i<len(self.ants)):
            if (not self.ants[i].gagnant):
                self.ants.pop(i)
            else:
                i+=1

        # On repeuple
        nenfant=self.nants-len(self.ants)
        newpop=[]
        for i in range(nenfant):
            parent1,parent2=self.ants[randint(0,len(self.ants))-1],self.ants[randint(0,len(self.ants))-1]
            newpop.add(Ant(self,(parent1.alpha+parent2.alpha)/2,(parent1.beta+parent2.beta)/2,(parent1.probarand+parent2.probarand)/2))
        self.ants=self.ants+newpop

        # Test
        for route in self.routes:
            print(route.pheromone)
