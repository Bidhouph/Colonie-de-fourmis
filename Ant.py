from random import randint,random

class Ant :
    def __init__(self,master,alpha,beta,probarand):
        self.master=master
        self.gagnant=False
        self.position=master.nid
        self.direction=None
        self.ways=[]
        self.preference=[]
        self.tours=1 # nombre de villes visites
        self.alpha=alpha # importance des pheromones
        self.beta=beta # importance d la longueur
        self.probarand=probarand # probabilite de choisir au hasard son chemin

    def move(self):
        # Recherche des destinations possibles
        for route in self.master.routes:
            if (route.ville1==self.position or route.ville2==self.position):
                self.ways.append(route)

        # Choix du chemin
        if (random()<self.probarand):
            self.direction=self.ways[randint(0,len(ways))-1]
        else :
            self.preference=[0 for _ in range(len(self.ways))]
            for i in range(len(ways)):
                self.preference[i]=(ways[i].pheromone**self.alpha*(2000/longueur(ways[i]))**self.beta)
            max,imax=preference[0],0
            for i in range(1,len(ways)):
                if (self.preference[i]>max):
                    imax,max=i,self.preference[i]
            self.direction=self.ways[imax]

        # deplacement de la fourmi
        self.position=self.direction
        self.position.pheromone+=10.0/self.tours
        self.tours+=1
        self.direction=None
        self.ways=[]
        self.preference=0

        # Test d'arrivee a la Source
        if (self.position.issource) :
            self.gagnant=True
