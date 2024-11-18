from __future__ import annotations
import pygame,random, uuid, math
from CONS import PLANTS_CONS, SCREEN_DATA
WHITE = (255,255,255)
MITOSIS_CHANCE = PLANTS_CONS["MITOSIS_CHANCE"]
DEATH_CHANCE = PLANTS_CONS["DEATH_CHANCE"]
MUTATION_CHANCE = PLANTS_CONS["MUTATION_CHANCE"]

class RGPlant():
    def __init__(self, x:int, y:int, gene:tuple):
        self.id = uuid.uuid1()
        self.x = x
        self.y = y
        self.gene = gene
        self.color = gene
        self.body = pygame.Rect(x,y,1,1)
        self.neighbor_region = pygame.Rect(self.x-1,self.y-1,3,3)

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, value):
        return (
            (self.id)
            == (value.id)
        )

    def update(self,grid_obj:"Grid") -> "Grid":
        self.color = self.update_color(grid_obj)
        dice = random.random()
        if dice <= MITOSIS_CHANCE:
            grid_obj = self.mitosis(grid_obj)
        elif dice <= MITOSIS_CHANCE + DEATH_CHANCE:
            grid_obj.remove_plant(x=self.x,y=self.y)
        return grid_obj

    def draw(self,canvas):
        #pygame.draw.rect(canvas,WHITE,self.neighbor_region)
        canvas.set_at((self.x,self.y), self.color)
        return canvas

    def update_color(self,grid_obj):
        neighbors = grid_obj.get_neighbors(x=self.x,y=self.y)
        color=[self.gene[0],self.gene[1],self.gene[2]]
        total_neighbors = 1
        if neighbors:
            for x,y in neighbors:
                if (x,y) in grid_obj.occupied_space:
                    total_neighbors += 1
                    color[0] += grid_obj.grid[x][y].gene[0]
                    color[1] += grid_obj.grid[x][y].gene[1]
                    color[2] += grid_obj.grid[x][y].gene[2]
            
            fase = math.radians(30)
            for i,value in enumerate(color):
                #average
                #color[i] = value/total_neighbors  

                #average but MOAR RED
                # color[i] = value/total_neighbors 
                # if i>0: color[i] *= 0.25

                #average, but my color matters more.
                if total_neighbors==1: color[i]=self.gene[i]
                else:
                    color[i] = (value-self.gene[i])/(total_neighbors-1)
                    color[i] = (self.gene[i]*0.75+color[i]*0.25)

                #another cool one
                # color[i] = (self.gene[0]+self.gene[1]+self.gene[2])%255
                # if color[i] > 255: color[i] = 255
                
                color[i] = int(color[i])
                #print(color[i])
            #color = self.gene
            print(f"self: {self.color}, new: {color}")

        return color

    def mitosis(self,grid_obj):
        gene = self.gene
        if random.random() < MUTATION_CHANCE: 
            gene = self.mutate(self.gene)

        for x in range(-1,2):
            for y in range(-1,2):
                if (
                    (x+self.x < SCREEN_DATA["RESOLUTION"][0]) and (y+self.y< SCREEN_DATA["RESOLUTION"][1]) 
                    and (x+self.x >=0) and (y+self.y>=0)):
                    grid_obj.add_plant(x=self.x+x, y=self.y+y,gene=gene)
        return grid_obj
                    
    def mutate(self, gene):
        gene = list(gene)
        index = random.randint(0,2)
        if random.random() < 0.5:
            gene[index] += 15
            if gene[index] > 255: gene[index] = 255
            if gene[index] == 0: gene[index] = 10
        else:
            gene[index] -= 15
            if gene[index] < 0: gene[index] = 0
        return tuple(gene)
