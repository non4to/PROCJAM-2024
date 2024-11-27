import pygame, random
from CONS import SCREEN_DATA
from rgplant import RGPlant
from textbox import TextBox
from grid import Grid

class Game():
    def __init__(self,window_title:str="RGPlants"):
        self.textbox_list = []
        self.configuration_start(window_title=window_title)

    def start_game(self):
        while not self.exit:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.exit=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toogle_pause()
                    elif event.key == pygame.K_r:
                        self.meteor()

            self.update()
            #self.before_draw()
            self.draw()
            self.update_screen()

    def update (self):
        plants_list = list(self.grid_obj.occupied_space)
        random.shuffle(plants_list)
        plants_list = set(plants_list)
        
        self.mouse_pos = self.get_mouse_position()
        self.manage_mouse_clicks()

        #plants
        if not self.pause:
            if plants_list:
                for x,y in plants_list:
                    self.grid_obj = self.grid_obj.grid[x][y].update(self.grid_obj)
                    
        else:
            for textbox in self.textbox_list:
                textbox.update()

    def draw (self):
        #plants
        for x,y in self.grid_obj.occupied_space:
            self.canvas = self.grid_obj.grid[x][y].draw(self.canvas)

        if self.pause:
            font = pygame.font.Font(None,12)
            pause_text = font.render(f"GAME PAUSED",True, (255,255,255))
            self.canvas.blit(pause_text,self.pause_pos)

            #Text Boxes
            for textbox in self.textbox_list:
                self.canvas = textbox.draw(self.canvas)
##############################################
##############################################
#####################################_#########
##############################################
##############################################
    def before_draw(self):
        self.canvas.fill((0, 0, 0)) 

    def update_screen(self):
        #draw mouse
        #self.canvas.set_at((self.mouse_pos[0],self.mouse_pos[1]), (255,0,255))
        scaled_canvas = pygame.transform.scale(self.canvas, self.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update() 
        self.clock.tick(self.fps_cap) #TODO: Option to change this value

    def meteor(self):
        """Cleans whole screen"""
        for x,y in self.grid_obj.occupied_space:
            self.grid_obj.grid[x][y] = None
        self.grid_obj.occupied_space = set()
        self.canvas.fill((0, 0, 0)) 

    def get_mouse_position(self) -> tuple:
        mouse_pos = pygame.mouse.get_pos()
        canvas_x = int(mouse_pos[0] * self.x_screen_scale)
        canvas_y = int(mouse_pos[1] * self.y_screen_scale)
        canvas_x = max(0, min(self.resolution[0] - 1, canvas_x))
        canvas_y = max(0, min(self.resolution[1] - 1, canvas_y))
        return canvas_x,canvas_y
    
    def toogle_pause(self):
        if self.pause:
            self.pause=False
        else:
            self.pause=True
    
    def manage_mouse_clicks(self):
        left, scroll, right = pygame.mouse.get_pressed()
        if left: 
            #Pause Menu
            if self.pause:
                for textbox in self.textbox_list:

                    if textbox.rect.collidepoint(self.mouse_pos[0],self.mouse_pos[1]):
                        textbox.active = True
                        self.toogle_textboxes(textbox)
                        break
                    else:
                        self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],(255,255,255))
            #Game Loop
            else:
                self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],(255,255,255))

    def toogle_textboxes(self,active_textbox):
        for textbox in self.textbox_list:
            if textbox == active_textbox: next
            else:
                if textbox.active: textbox.active = False

    def add_plant_to_position(self,x:int,y:int,gene:tuple):
        self.grid_obj.add_plant(x,y,gene)

    def configuration_start(self, window_title):
        pygame.init()
        pygame.font.init()
        # pygame.mouse.set_v    isible(False)
        self.resolution = SCREEN_DATA["RESOLUTION"]
        self.screen_size = SCREEN_DATA["SCREEN_SIZE"]
        self.grid_obj = Grid(SCREEN_DATA["RESOLUTION"][0],SCREEN_DATA["RESOLUTION"][1])
        self.canvas = pygame.Surface(self.resolution)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.x_screen_scale = self.resolution[0] / self.screen_size[0]
        self.y_screen_scale = self.resolution[1] / self.screen_size[1]
        self.fps_cap = SCREEN_DATA["FPS_CAP"]
        pygame.display.set_caption(window_title)
        self.exit = False
        self.pause = False
        self.mouse_pos = (0,0)
        self.clock = pygame.time.Clock()
        self.pause_pos = [3,0]

        ### Pause Menu Configuration
        tbox_width = 10
        tbox_height = 5
        tbox_y_pos = 30
        tbox_x_initial = 12
        #red box, most left
        self.textbox_list.append(TextBox(tbox_x_initial,tbox_y_pos,tbox_width,tbox_height,(255,0,0),(125,0,0)))
        #green box, middle
        self.textbox_list.append(TextBox(self.textbox_list[0].x+15,tbox_y_pos,tbox_width,tbox_height,(0,255,0),(0,125,0)))
        #blue box, most right
        self.textbox_list.append(TextBox(self.textbox_list[1].x+15,tbox_y_pos,tbox_width,tbox_height,(0,0,255),(0,0,125)))

        
def main():
    A = Game()
    A.start_game()

if __name__ == "__main__":
    main()