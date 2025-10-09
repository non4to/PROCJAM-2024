import pygame, random, copy
from CONS import SCREEN_DATA, PLANTS_CONS
from entities import RGPlant, TextBox
# from rgplant import RGPlant
# from textbox import TextBox
from grid import Grid

class Game():
    def __init__(self,window_title:str="RGPlants"):
        self.textbox_list = []
        self.configuration_start(window_title=window_title)

    def game_loop(self):
        while not self.exit:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.exit=True
                elif event.type == pygame.KEYDOWN:
                    
                    if (event.key == pygame.K_SPACE):
                        self.configurationScreen = not(self.configurationScreen)
                        
                    elif (event.key == pygame.K_p):
                        self.pause = not(self.pause)
                        
                    elif event.key == pygame.K_r:
                        self.meteor()
                    elif event.key == pygame.K_ESCAPE:
                        self.exit = True
                    if self.configurationScreen:
                        for i,textbox in enumerate(self.textbox_list):
                            if not(textbox.active): continue
                            
                            if (event.unicode.isdigit()):
                                if not(textbox.editing):
                                    textbox.text = event.unicode
                                    textbox.editing = True
                                else:
                                    textbox.text += event.unicode            
                                    if int(self.textbox_list[3].text)+int(self.textbox_list[4].text) > 100:
                                        newValue = 100 - int(textbox.text)
                                        if newValue < 0: newValue = 0
                                        if (i==3): #Changing Reproduction Chance
                                            self.textbox_list[4].text = str(newValue)
                                        elif (i==4): #Chaging Death Chance
                                            self.textbox_list[3].text = str(newValue)         
                                                           
                            elif (event.key == pygame.K_BACKSPACE):
                                textbox.text = textbox.text[:-1]   
                                if textbox.text == "": textbox.text = "0"
                    print(f"pause: {self.pause}")
                    print(f"config: {self.configurationScreen}")

            self.update()
            self.before_draw()
            self.draw()
            self.update_screen()

    def update (self):
        plants_list = list(self.grid_obj.occupied_space)
        random.shuffle(plants_list)
        plants_list = set(plants_list)
        
        self.mouse_pos = self.get_mouse_position()
        self.manage_mouse_clicks()

        #plants
        if not(self.pause):
            if plants_list:
                for x,y in plants_list:
                    self.grid_obj = self.grid_obj.grid[x][y].update(self.grid_obj)
                    
        if (self.configurationScreen):
            self.pause = True
            for textbox in self.textbox_list:
                textbox.update()
            self.brushColor = (int(self.textbox_list[0].text), int(self.textbox_list[1].text), int(self.textbox_list[2].text))
            self.plantParameter["MITOSIS_CHANCE"] = float(self.textbox_list[3].text)/100
            self.plantParameter["DEATH_CHANCE"] = float(self.textbox_list[4].text)/100
            self.plantParameter["MUTATION_CHANCE"] = float(self.textbox_list[5].text)/100
            
    def draw (self):
        #plants
        for x,y in self.grid_obj.occupied_space:
            self.canvas = self.grid_obj.grid[x][y].draw(self.canvas)

        if self.configurationScreen:
            self.uiCanvas.blit(self.uiPauseText,self.uiPausePos)
            self.uiCanvas.blit(self.uiBrushText1,self.uiBrushTextPos1)
            self.uiCanvas.blit(self.uiBrushText2,self.uiBrushTextPos2)
            self.uiCanvas.blit(self.uiReplicationText1, self.uiReplicationPos1)
            self.uiCanvas.blit(self.uiReplicationText2, self.uiReplicationPos2)
            self.uiCanvas.blit(self.uiDeathText1,self.uiDeathPos1)
            self.uiCanvas.blit(self.uiDeathText2,self.uiDeathPos2)
            self.uiCanvas.blit(self.uiMutationText1,self.uiMutationPos1)
            self.uiCanvas.blit(self.uiMutationText2,self.uiMutationPos2)

            #Text Boxes
            for textbox in self.textbox_list:
                self.uiCanvas = textbox.draw(self.uiCanvas)
        
        if self.pause:
            if random.random() < 0.01:
                self.pauseColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

            width = 1 
            rect = pygame.Rect(0,0,SCREEN_DATA["SCREEN_SIZE"][0],SCREEN_DATA["SCREEN_SIZE"][1])
            pygame.draw.rect(self.pauseCanvas, self.pauseColor, rect, width)
            

    def before_draw(self):
        if (self.configurationScreen): self.uiCanvas.fill((0, 0, 0, 0))  
        pass
        
    def update_screen(self):
        #draw mouse
        #self.canvas.set_at((self.mouse_pos[0],self.mouse_pos[1]), (255,0,255))
        scaled_canvas = pygame.transform.scale(self.canvas, self.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        if (self.pause): self.screen.blit(self.pauseCanvas, (0,0))
        if (self.configurationScreen): self.screen.blit(self.uiCanvas, (0, 0))  # Draw scaled canvas on the screen

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
        if not(self.configurationScreen):
            canvas_x = int(mouse_pos[0] * self.x_screen_scale)
            canvas_y = int(mouse_pos[1] * self.y_screen_scale)
            canvas_x = max(0, min(self.resolution[0] - 1, canvas_x))
            canvas_y = max(0, min(self.resolution[1] - 1, canvas_y))
            mouse_pos = [canvas_x, canvas_y]
        return mouse_pos
    
    def toogle_var(self, var):
            return not(var)

    
    def manage_mouse_clicks(self):
        left, scroll, right = pygame.mouse.get_pressed()
        if left: 
            #Pause Menu
            if self.configurationScreen:
                for textbox in self.textbox_list:
                    if textbox.rect.collidepoint(self.mouse_pos[0],self.mouse_pos[1]):
                        textbox.active = True
                        self.toogle_textboxes(textbox)
                        break
                    # else:
                    #     self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],(255,255,255))
            #Game Loop
            else:
                self.add_plant_to_position(copy.deepcopy(self.plantParameter), self.mouse_pos[0],self.mouse_pos[1],self.brushColor)

    def toogle_textboxes(self,active_textbox):
        for textbox in self.textbox_list:
            if textbox == active_textbox: next
            else:
                if textbox.active: 
                    textbox.active = False
                    textbox.editing = False

    def add_plant_to_position(self, parameters:dict, x:int,y:int,gene:tuple):
        self.grid_obj.add_plant(parameters, x,y,gene)

    def configuration_start(self, window_title):
        pygame.init()
        pygame.font.init()
        self.resolution = SCREEN_DATA["RESOLUTION"]
        self.screen_size = SCREEN_DATA["SCREEN_SIZE"]
        self.grid_obj = Grid(SCREEN_DATA["RESOLUTION"][0],SCREEN_DATA["RESOLUTION"][1])
        self.canvas = pygame.Surface(self.resolution)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.x_screen_scale = self.resolution[0] / self.screen_size[0]
        self.y_screen_scale = self.resolution[1] / self.screen_size[1]
        self.plantParameter = {"MITOSIS_CHANCE": PLANTS_CONS["MITOSIS_CHANCE"],
                          "DEATH_CHANCE": PLANTS_CONS["DEATH_CHANCE"],
                          "MUTATION_CHANCE": PLANTS_CONS["MUTATION_CHANCE"]}
        
        ###########
        self.fps_cap = SCREEN_DATA["FPS_CAP"]
        pygame.display.set_caption(window_title)
        self.exit = False
        self.configurationScreen = False
        self.pause = False
        self.mouse_pos = (0,0)
        self.clock = pygame.time.Clock()
        self.brushColor = (255,0,0)
        
        ## UI ##
        self.pauseColor = (255,255,255)
        self.uiCanvas = pygame.Surface(self.screen_size)
        self.pauseCanvas = pygame.Surface(self.screen_size)
        
        self.uiFontBIG = pygame.font.Font(None,53)
        self.uiFontMID = pygame.font.Font(None,24)
        self.uiPauseText = self.uiFontBIG.render(f"CONFIGURATION",True,(255,255,255))
        self.uiPausePos = [SCREEN_DATA["SCREEN_SIZE"][0]/4-20,3]        
        self.uiBrushText1 = self.uiFontMID.render(f"BRUSH",True,(255,255,255))
        self.uiBrushText2 = self.uiFontMID.render(f"COLOR",True,(255,255,255))
        self.uiReplicationText1 = self.uiFontMID.render(f"REPLICATION",True,(255,255,255))
        self.uiReplicationText2 = self.uiFontMID.render(f"(%)",True,(255,255,255))
        self.uiDeathText1 = self.uiFontMID.render(f"DEATH",True,(255,255,255))
        self.uiDeathText2 = self.uiFontMID.render(f"(%)",True,(255,255,255))
        self.uiMutationText1 = self.uiFontMID.render(f"MUTATION",True,(255,255,255))
        self.uiMutationText2 = self.uiFontMID.render(f"(%)",True,(255,255,255))


        ### Pause Menu Configuration
        tbox_width = SCREEN_DATA["SCREEN_SIZE"][0]/5
        tbox_height = SCREEN_DATA["SCREEN_SIZE"][1]*0.1
        
        tbox_x_initial = SCREEN_DATA["SCREEN_SIZE"][0]/6
        tbox_y_initial = SCREEN_DATA["SCREEN_SIZE"][1]/7
        
        spaceBetweenBoxes = 30
        text_font = pygame.font.Font(None,53)
         
        #red box, most left
        self.textbox_list.append(TextBox("brush",tbox_x_initial,tbox_y_initial,tbox_width,tbox_height,(255,0,0),(125,0,0),text_font))

        self.uiBrushTextPos1 = [self.textbox_list[0].x-75, self.textbox_list[0].y+10]   
        self.uiBrushTextPos2 = [self.uiBrushTextPos1[0], self.uiBrushTextPos1[1]+15]   
        #green box, middle
        self.textbox_list.append(TextBox("brush",self.textbox_list[0].x+tbox_width+spaceBetweenBoxes,tbox_y_initial,tbox_width,tbox_height,(0,255,0),(0,125,0), text_font))
        #blue box, most right
        self.textbox_list.append(TextBox("brush",self.textbox_list[1].x+tbox_width+spaceBetweenBoxes,tbox_y_initial,tbox_width,tbox_height,(0,0,255),(0,0,125), text_font))
        #Replication chance
        self.textbox_list.append(TextBox("param",self.textbox_list[1].x,tbox_y_initial+tbox_height+spaceBetweenBoxes*2,tbox_width,tbox_height,(0,255,255),(0,125,125), text_font))
        self.uiReplicationPos1 = [self.textbox_list[3].x-125, self.textbox_list[3].y+10]  
        self.uiReplicationPos2 = [self.uiReplicationPos1[0]+40, self.uiReplicationPos1[1]+15]  
        #Death Chance
        self.textbox_list.append(TextBox("param",self.textbox_list[1].x,self.textbox_list[3].y+tbox_height+spaceBetweenBoxes,tbox_width,tbox_height,(180,180,0),(100,100,0), text_font))
        self.uiDeathPos1 = [self.textbox_list[4].x-70, self.textbox_list[4].y+10]  
        self.uiDeathPos2 = [self.uiDeathPos1[0]+20, self.uiDeathPos1[1]+15]  
        #Mutation Chance
        self.textbox_list.append(TextBox("param",self.textbox_list[1].x,self.textbox_list[4].y+tbox_height+spaceBetweenBoxes,tbox_width,tbox_height,(255,0,255),(125,0,125), text_font))
        self.uiMutationPos1 = [self.textbox_list[5].x-95, self.textbox_list[5].y+10]  
        self.uiMutationPos2 = [self.uiMutationPos1[0]+30, self.uiMutationPos1[1]+15]  
        
        
def main():
    A = Game()
    A.game_loop()

if __name__ == "__main__":
    main()