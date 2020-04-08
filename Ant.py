#-*- coding: utf-8 -*-

from random import randint,random
import numpy

class Ant :
    def __init__(self,master,alpha,beta,gamma,lifeSpan):
        self.master=master
        self.gagnant=False
        self.position=master.nid
        self.direction=None
        self.tours=1 # nombre de villes visites
        self.depotPhero=100 # nombre de phéromones à déposer ( décroit au cours du temps )
        self.alpha=alpha # importance des pheromones
        self.beta=beta # importance d la longueur
        self.gamma=gamma # probabilite de choisir au hasard son chemin
        self.memoire=[]
        self.delay=0
        self.alive=True
        self.lifeSpan=int(lifeSpan*(1+0.6*(random()-0.5))) # Une durée de vie aléatoire dans [0.7*lifespan ; 1.3*lifeSpan]


    def move(self):

        # Gestion globale des déplacements

        if (self.lifeSpan<1): # La fourmi meurt si elle n'a plus de temps de vie
            self.alive=False
        else:
            if(self.delay == 0):
                if (self.gagnant):
                    self.moveFixed()
                elif (self.alive):
                    self.moveRandom()
                else:
                    pass
            else:
                self.delay-=1

            self.lifeSpan-=1
            self.tours+=1
            self.depotPhero=100/numpy.log(2.8*(1+self.tours))


    def moveRandom(self):

        ### fonction de déplacement à l'allée vers l'objectif

        # Recherche des destinations possibles
        ways=[]
        for route in self.master.routes:
            if (route.ville1==self.position or route.ville2==self.position):
                if (len(self.memoire)==0 or route != self.memoire[-1][0]): # On empèche le retour sur ses pas
                    ways.append(route)

        if(len(ways)==0):  # On tue les fourmis qui se retrouvent dans un cul-de-sac (cela évite les accumulations sur un cul de sac proche de l'arrivée)
            self.alive=False
            return None

        # Choix du chemin
        # A l'allée, les fourmis cherchent l'objectif en suivant :
        #   - les phéromones (coef alpha)
        #   - la longueur minimale des chemins (coef beta)
        #   - et de l'aléatoire (coef gamma)

        preference=[0 for _ in range(len(ways))]
        for i in range(len(ways)):
            preference[i]=ways[i].pheromone**self.alpha*(2000/ways[i].longueur)**self.beta*(1+10*random())**self.gamma
        max,imax=preference[0],0
        for i in range(1,len(ways)):
            if (preference[i]>max):
                imax,max=i,preference[i]
        self.direction=ways[imax]

        # deplacement de la fourmi

        # Décomenter la ligne suivante pour ajouter des phéromones sur l'allée.
        # self.direction.pheromone+=self.depotPhero

        self.memoire.append((self.direction,self.position))

        if (self.position == self.direction.ville1):
            self.position = self.direction.ville2
        else:
            self.position = self.direction.ville1
        self.delay+=self.direction.delay
        print("Une fourmi est arrivée à "+self.position.name)

        # Test d'arrivee a la Source
        if (self.position.issource) :
            self.gagnant=True
            self.tours=1

    def moveFixed(self):

        ### Fonction de déplacement au retour

        if(len(self.memoire)>0):
            (self.direction,self.position)=self.memoire.pop()
            print("Une fourmi est arrivée à "+self.position.name)
            self.direction.pheromone+=self.depotPhero
            self.delay+=self.direction.delay
        else:
            self.alive=False
