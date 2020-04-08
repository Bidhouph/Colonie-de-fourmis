#-*- coding: utf-8 -*-

import Ville
import numpy
from Tkinter import *

class Route :
    def __init__(self,master,ville1,ville2):
        self.master=master
        self.ville1=ville1
        self.ville2=ville2
        self.longueur=((ville1.x-ville2.x)**2+(ville1.y-ville2.y)**2)**0.5
        self.delay= int(0.1*((ville1.x-ville2.x)**2+(ville1.y-ville2.y)**2)**0.5) # pour une distance de 10 pixels, un délai de 1 tour
        self.pheromone=100.0

        # Zone de texte pour les pheromones
        angle=2*numpy.arctan((self.ville1.x-self.ville2.x)/(self.ville1.y-self.ville2.y+self.longueur))+numpy.pi/2
        x,y=(self.ville1.x+self.ville2.x)/2+20*numpy.sin(angle),(self.ville1.y+self.ville2.y)/2+20*numpy.cos(angle)
        self.label=Label(self.master.can,text=str(int(self.pheromone)))
        self.label.pack()
        self.text=self.master.can.create_window((x,y),window=self.label)

    def evapore(self,rho):
        pheromone*=(1-rho)

    def affiche(self):
        self.master.can.create_line(self.ville1.x,self.ville1.y,self.ville2.x,self.ville2.y,width=3)

    def updatePhero(self):
        self.label['text'] = str(int(self.pheromone))
