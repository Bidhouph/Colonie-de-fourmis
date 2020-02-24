class Ville :
    def __init__(self,master,x,y):
        self.master=master
        self.issource=False
        self.x=x
        self.y=y
        self.color="#444"

    def affiche(self):
        x,y,dx=self.x,self.y,self.master.dx
        self.master.can.create_rectangle(x-dx,y-dx,x+dx,y+dx,fill=self.color)

    def setNid(self):
        self.color="#33e"
        self.affiche()
        self.master.nid=self

    def setSource(self):
        self.color="#e33"
        self.affiche()
        self.master.source=self
        self.issource=True
