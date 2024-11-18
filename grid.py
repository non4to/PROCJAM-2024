from rgplant import RGPlant
from CONS import SCREEN_DATA
import typing
import uuid, pickle, random as rd

class Grid():
    def __init__(self,x_size:int, y_size:int) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.grid = self.build_grid()

        self.occupied_space = set()

    def build_grid(self):
        # grid = {}
        grid: list[list[dict[str, typing.Any]]] = [
            [
                {
                } for _ in range(self.x_size)
            ] for _ in range(self.y_size)
        ]
        return grid

    def get_neighbors(self,x,y):
        neighbors = []
        if x==0 and y==0:
            neighbors=((0,1),(1,0),(1,1))
        elif x==0 and y==self.y_size-1:
            neighbors=((0,self.y_size-2),(1,self.y_size-2),(1,self.y_size-1))
        elif x==self.x_size-1 and y==0:
            neighbors=((self.x_size-2,0),(self.x_size-2,1),(self.x_size-1,1))
        elif x==self.x_size-1 and y==self.y_size-1:
            neighbors=((self.x_size-1,self.y_size-2),(self.x_size-2,self.y_size-2),(self.x_size-2,self.y_size-1))
        elif x == 0 and y != self.y_size-1:
            for ix in range(0, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        elif y == 0 and x != self.x_size-1:
            for ix in range(-1, 2):
                for iy in range(0, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        else:
            for ix in range(-1, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        return neighbors 
    
    def add_plant(self, x:int, y:int, gene:tuple=[0]):
        if self.grid[x][y]:
            self.remove_plant(x,y)
        new_plant = RGPlant(x,y,gene)
        self.grid[x][y] = new_plant
        self.occupied_space.add((x,y))
        return new_plant.id

    def remove_plant(self, x, y):
        self.grid[x][y] = None
        self.occupied_space.discard((x,y))

    def save_grid_state(self, address,step):
        with open(f"{address}/[{step}]-{self.id}", "wb") as file:
            pickle.dump(self,file)
        

def print_occupied_positions(grid):
    for y in range(SCREEN_DATA["RESOLUTION"][1]):
        for x in range(SCREEN_DATA["RESOLUTION"][0]):
            if grid[x][y]:
                print(f"({x},{y}): [color]:{grid[x][y].color}")
    print("Finished")

if __name__ == "__main__":
    p1 = RGPlant(5,5,(150,150,150))
    grid_obj = Grid(SCREEN_DATA["RESOLUTION"][0],SCREEN_DATA["RESOLUTION"][1])
    grid_obj.add_plant(5,5,(100,100,100))
    grid_obj.add_plant(6,6,(300,300,300))
    
    # print_occupied_positions(grid_obj.grid)

    grid_obj.grid[5][5].color = grid_obj.grid[5][5].update_color(grid_obj)
    grid_obj.grid[6][6].color = grid_obj.grid[6][6].update_color(grid_obj)    
    # print_occupied_positions(grid_obj.grid)
    



    


    

                