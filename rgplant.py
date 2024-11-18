import pygame, random, uuid, math

WHITE = (255, 255, 255)

class RGPlant:
    def __init__(self, x: int, y: int, gene: list, neighbor_dict: dict, PLANTS_CONS: dict, neighbors=tuple):
        self.id = uuid.uuid1()
        self.x = x
        self.y = y
        self.gene = gene
        self.color = gene
        self.body = pygame.Rect(x, y, 1, 1)
        self.neighbor_region = pygame.Rect(self.x - 1, self.y - 1, 3, 3)
        self.mitosis_chance = PLANTS_CONS["MITOSIS_CHANCE"] / 100
        self.death_chance = 0.01#PLANTS_CONS["DEATH_CHANCE"] / 2 / 100
        self.mutation_chance = PLANTS_CONS["MUTATION_CHANCE"] / 100
        self.neighbors = neighbors

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, value):
        return (self.id) == (value.id)

    def update(self, grid):
        new_plants = []
        death = False
        self.color = self.update_color(grid)
        dice = random.random()
        if dice <= self.mitosis_chance:
            new_plants = self.mitosis()
        elif dice > 1 - self.death_chance:
            death = True
        return death, new_plants, grid

    def draw(self, canvas):
        # pygame.draw.rect(canvas,WHITE,self.neighbor_region)
        canvas.set_at((self.x, self.y), self.color)
        return canvas

    # def get_neighbors(self, all_plants):
    #     neighbors = []
    #     for key in neighbor_dict:
    #         if key==(self.x,self.y):
    #             return neighbor_dict
    #     # for plant in all_plants:
    #     #     if self.neighbor_region.colliderect(plant.body):
    #     #         neighbors.append(plant)
    #     return neighbors

    def update_color(self, grid):
        color = [0, 0, 0]
        flower_number=0
        for position in self.neighbors:
            if position in grid:
                for flower in grid[position]:
                    flower_number += 1
                    color[0] += flower.gene[0]
                    color[1] += flower.gene[1]
                    color[2] += flower.gene[2]

        if flower_number != 0:
            for i, value in enumerate(color):
                # Average
                color[i] = int(value / flower_number)
                if color[i] > 255: color[i]=255
        return color

    def mitosis(self):
        gene = self.gene
        if random.random() <= self.mutation_chance:
            gene = self.mutate(self.gene)

        new_plants = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_plants.append([self.x + x, self.y + y, gene])
        return new_plants

    def mutate(self, gene):
        gene = list(gene)
        index = random.randint(0, 2)
        if random.random() < 0.5:
            gene[index] *= 1.25
            if gene[index] > 255:
                gene[index] = 255
        else:
            gene[index] *= 0.75
            if gene[index] < 0:
                gene[index] = 0
        return gene