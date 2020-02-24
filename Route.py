import Ville

class Route :
    def __init__(self,master,ville1,ville2):
        self.master=master
        self.ville1=ville1
        self.ville2=ville2
        self.longueur=((ville1.x-ville2.x)**2+(ville1.y-ville2.y)**2)**0.5
        self.pheromone=100.0

    def evapore(self,rho):
        pheromone*=(1-rho)

    def affiche(self):
        self.master.can.create_line(self.ville1.x,self.ville1.y,self.ville2.x,self.ville2.y,width=3)
