import os
import pygame
from pygame import *

pygame.init()
pygame.font.init()

entities = pygame.sprite.Group()

PlatformImages = {}
BGImages = {}

display_width = 800
display_height = 640

screen = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption("Profielwerkstuk 2018")
timer = pygame.time.Clock()

def main():
    level_playing = show_start_screen(screen)
    
    up = down = left = right = running = False
    
    bg = Surface((display_width, display_height)).convert()
    bg.fill((15,150,150))
    

    
    
    camera = Camera(complex_camera, level_playing[0], level_playing[1])

    player = level_playing[2]
    platforms = level_playing[3]
     
    entities.add(player)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                pygame.quit()
                exit()
            
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        #achtergrond vullen
        screen.blit(bg, (0,0))

        camera.update(player) #camera volgt de speler, kan overigens ook andere sprites volgen

        #speler updaten, alle andere sprites op scherm tevoorschijn toveren
        player.update(up, down, left, right, running, platforms)
        player.animate()
        for e in entities:
            screen.blit(e.image, camera.apply(e)) #alle entities bewegen met het scherm mee

        pygame.display.update()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    #target_rect is in het centrum van het scherm
    x = -target_rect.center[0] + display_width/2 
    y = -target_rect.center[1] + display_height/2
    #camera bewegen met behulp van vectors
    camera.topleft += (pygame.math.Vector2((x, y)) - pygame.math.Vector2(camera.topleft)) * 0.06
    #zorgen dat we niet buiten het level kunnen kijken
    camera.x = max(-(camera.width-display_width), min(0, camera.x))
    camera.y = max(-(camera.height-display_height), min(0, camera.y))

    return camera




class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)




class Button():
    def __init__(self, x, y, width, height, colour, txt):
        #extra geeft de ruimte aan in pixels die nodig is om de text ongeveer in het midden van de knop te zetten
        
        self.image = pygame.Surface((width, height)).convert()
        self.image.fill(colour)
        self.rect = Rect(x, y, width, height)
        
        self.font = pygame.font.SysFont('Arial', 40)
        self.text = self.font.render(txt, True, (0,0,0))
        screen.blit(self.image, (x,y))
        screen.blit(self.text, (x + ((width - self.text.get_rect().width) / 2) , y + (height - self.text.get_rect().height) / 2))
                

def show_start_screen(screen):
    screen.fill((10,100,100))
    play_button = Button(300, 180, 200, 60, (150,15,15), "Play")
    quit_button = Button(300, 280, 200, 60, (150,15,15), "Quit")
    showStartScreen = True
    while showStartScreen:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos   #geeft positie van de muis
                if play_button.rect.collidepoint(mouse_pos):
                    level_1 = build_level( [        #hier staat trouwens LEVEL_EEN, niet LEVEL_L (kut font)
                                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                                            "A                ABA                                                                                A",
                                            "A                ABA                                                                                A",
                                            "A                ABA                                                                                A",
                                            "A                ABA                                                                                A",
                                            "A                ABA                                                                       BAAAB    A",
                                            "A                ABA                                                                       A   A    A",
                                            "A                ABA                                                                       A   A    A",
                                            "A                ABA                BAAAAAAAAAAAAAAAAAAAAB                              AAAA   A    A",
                                            "A                ABA                                 A                               AAA       A    A", 
                                            "A                ABA                                 A                            AAA          A    A",
                                            "A                ABA                                 A                         AAA             A    A",
                                            "A                ABAAAAAAAB                          A                      BAA                A    A",
                                            "A                AAAAAAAAAA                          BAAAAAAAAAAAAAAB                      BBBBB    B",
                                            "A                                                                                          B        B",
                                            "A                                                                                          B        B",
                                            "A        P                            BAAAAB                                               B   E    B",
                                            "A                                                                                          B        B",
                                            "A                                                                                          B        B",
                                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBB",] )
                    return level_1

                if quit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
        pygame.display.update()




class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.walking = False
        self.frame_change = 80      #na hoeveel aantal ticks het character frame verandert
        self.walking_startup = 1
        self.goingRight = 1         #kijkend naar rechts: 1       kijkend naar links: 0
        self.load_images()          #als hij net begint met lopen: 1   als hij al loopt: _run_2 niet laten zien, dus 0
        self.last_update = 0        #telt aantal ticks sinds laatste keer dat het character frame is veranderd tijdens het lopen
        self.current_frame = 0
        self.image = self.standing_frame_right
        self.rect = self.image.get_rect(topleft=(x,y))

    def load_images(self):
        character_folder = "/Profielwerkstuk/Character Sprites/"
        self.standing_frame_right = pygame.image.load(os.path.join(character_folder, "pws_character_sprite_rest.png")).convert_alpha()
        self.standing_frame_right = pygame.transform.scale(self.standing_frame_right, tuple([int(i*0.15) for i in self.standing_frame_right.get_rect().size]))
        self.walking_frame_startup_right = pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_2.png"))
        self.walking_frame_startup_right = pygame.transform.scale(self.walking_frame_startup_right, tuple([int(i*0.15) for i in self.walking_frame_startup_right.get_rect().size]))
        self.walking_frames_right = [pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_3.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_4.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_5.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_6.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_7.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_8.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_9.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_10.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_11.png")).convert_alpha(),
                                     pygame.image.load(os.path.join(character_folder, "pws_character_sprite_run_12.png")).convert_alpha()]
        for i in range (0, len(self.walking_frames_right)):
            self.walking_frames_right[i] = pygame.transform.scale(self.walking_frames_right[i], tuple([int(i*0.15) for i in self.walking_frames_right[i].get_rect().size]))
        self.standing_frame_left = pygame.transform.flip(self.standing_frame_right, True, False)
        self.walking_frame_startup_left = pygame.transform.flip(self.walking_frame_startup_right, True, False)
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()
        if abs(self.xvel) >= 0.5:
            if self.onGround:
                self.walking = True
        else:
            self.walking = False
            self.walking_startup = 1
        if self.walking:
            if now - self.last_update > self.frame_change:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_right)
                if self.xvel > 0:
                    if self.walking_startup:
                        self.image = self.walking_frame_startup_right
                        self.walking_startup = 0
                    else:
                        self.image = self.walking_frames_right[self.current_frame]
                    self.goingRight = 1
                elif self.xvel < 0:
                    if self.walking_startup:
                        self.image = self.walking_frame_startup_left
                        self.walking_startup = 0
                    else:
                        self.image = self.walking_frames_left[self.current_frame]
                    self.goingRight = 0
                self.rect = self.image.get_rect(topleft=(self.rect.topleft))
        elif self.walking == False and self.onGround == True:
            if self.goingRight:
                self.image = self.standing_frame_right
            else:
                self.image = self.standing_frame_left
            self.rect = self.image.get_rect(topleft=(self.rect.topleft))
        elif self.onGround == False:
            pass

    def update(self, up, down, left, right, running, platforms):
        if up:
            #je kan alleen springen als je op een platform staat
            if self.onGround:
                self.yvel -= 10
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8 
        if not self.onGround:
            #zwaartekracht als je niet op een platform staat
            self.yvel += 0.35
            #maximum valsnelheid
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel *= 0.5
            if abs(self.xvel) <= 0.1:
                self.xvel = 0
        #verandering x-richting
        self.rect.left += self.xvel
        #kijken of er botsingen in de x-richting zijn
        self.collide(self.xvel, 0, platforms)
        #verandering y-richting
        self.rect.top += self.yvel
        #we nemen altijd eerst aan dat de speler in de lucht is
        self.onGround = False;
        #kijken of er botsingen in de y-richting zijn
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    show_start_screen(screen) #einde van level, nog niet toegevoegd
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

object_folder = "/Profielwerkstuk/Objects/"
class Platform(Entity):
    def __init__(self, x, y, number):
        Entity.__init__(self)
        self.load_images()
        self.image = PlatformImages['platform_'+number]
        self.rect = Rect(x, y, 32, 32)

    def load_images(self):
        global PlatformImages
        PlatformImages['platform_1'] = pygame.image.load(os.path.join(object_folder, "blok1.png")).convert_alpha()
        PlatformImages['platform_2'] = pygame.image.load(os.path.join(object_folder, "blok2.png")).convert_alpha()

class Background(Entity):
    def __init__(self, x, y, number):
        Entity.__init__(self)
        self.load_images()
        self.image = BGImages['BG_'+number]
        self.rect = Rect(x, y, 32, 32)

    def load_images(self):
        global BGImages
        BGImages['BG_1'] = pygame.image.load(os.path.join(object_folder, "achtergrond1.png")).convert_alpha() #als transparente dingen niet werken probeer .convert_alpha()
        BGImages['BG_2'] = pygame.image.load(os.path.join(object_folder, "achtergrond2.png")).convert_alpha()
        BGImages['BG_3'] = pygame.image.load(os.path.join(object_folder, "achtergrond3.png")).convert_alpha()

class ExitBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load(os.path.join(object_folder, "Exitblok.png")).convert()
        self.rect = self.image.get_rect(topleft=(x,y))


def build_level(level):
    platforms = []
    x = y = 0
    #level bouwen
    for row in level:
        for col in row:
            if col == "P":
                player = Player(x, y)
            if col == "A":
                a = Platform(x, y, "1")
                platforms.append(a)
                entities.add(a)
            if col == "B":
                a = Platform(x, y, "2")
                platforms.append(a)
                entities.add(a)
            if col == "E":
                a = ExitBlock(x, y)
                platforms.append(a)
                entities.add(a)
            if col == "Z":
                a = Background(x, y, "1")
                entities.add(a) #geen platforms.append omdat de speler er niet tegenaan moet botsen
            if col == "Y":
                a = Background(x, y, "2")
                entities.add(a)
            if col == "X":
                a = Background(x, y, "3")
                entities.add(a)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32 #lengte level berekenen in pixels
    total_level_height = len(level)*32

    levelList = [total_level_width, total_level_height, player, platforms]
    return levelList

        
          
if __name__ == "__main__":
    main()
