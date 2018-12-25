import pygame
from pygame import *

PlatformImages = {}
BGImages = {}

display_width = 800
display_height = 640

def main():
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height), 0, 32)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    
    bg = Surface((display_width, display_height)).convert()
    bg.fill(Color("#040024"))
    
    entities = pygame.sprite.Group()
    platforms = []

    x = y = 0
    level = [
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "A                           A",
        "A                           A",
        "A              P            A",
        "A                          AA",
        "A                           A",
        "A                           A",
        "A                          AA",
        "A      X       BB           A",
        "A      Y       BB           A",
        "A      Z        X          AA",
        "A      B        Y           A",
        "A      A        Y           A",
        "A    BABAB      Y           A",
        "A      A    B   Y           A",
        "A      B        Y           A",
        "A      X        Z           A",
        "A      Y        BAAB        A",
        "A      Y           X        A",
        "A      Y           Y        A",
        "A      Z           Z   AA   A",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",]
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
                b = Platform(x, y, "2")
                platforms.append(b)
                entities.add(b)
            if col == "Z":
                z = Background(x, y, "1")
                entities.add(z) #geen platforms.append omdat de speler er niet tegenaan moet botsen
            if col == "Y":
                z = Background(x, y, "2")
                entities.add(z)
            if col == "X":
                z = Background(x, y, "3")
                entities.add(z)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32 #lengte level berekenen in pixels
    total_level_height = len(level)*32  
    camera = Camera(complex_camera, total_level_width, total_level_height)
     
    entities.add(player)

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                quit()
            
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

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.walking = False
        self.walking_startup = 1
        self.goingRight = 1         #kijkend naar rechts: 1       kijkend naar links: 0
        self.load_images()          #als hij net begint met lopen: 1   als hij al loopt: _run_2 niet laten zien, dus 0
        self.last_update = 0        #telt aantal ticks sinds laatste keer dat het character frame is veranderd tijdens het lopen
        self.current_frame = 0
        self.image = self.standing_frame_right
        self.rect = self.image.get_rect()

    def load_images(self):
        self.standing_frame_right = pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_rest.png")
        self.standing_frame_right = pygame.transform.scale(self.standing_frame_right, tuple([i * 0.15 for i in self.standing_frame_right.get_rect().size]))
        self.walking_frame_startup_right = pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_2.png")
        self.walking_frame_startup_right = pygame.transform.scale(self.walking_frame_startup_right, tuple([i * 0.15 for i in self.walking_frame_startup_right.get_rect().size]))
        self.walking_frames_right = [pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_3.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_4.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_5.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_6.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_7.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_8.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_9.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_10.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_11.png"),
                                     pygame.image.load("/Profielwerkstuk/Character Sprites/pws_character_sprite_run_12.png")]
        for i in range (0, len(self.walking_frames_right)):
            self.walking_frames_right[i] = pygame.transform.scale(self.walking_frames_right[i], tuple([i * 0.15 for i in self.walking_frames_right[i].get_rect.size]))
        self.standing_frame_left = pygame.transform.flip(self.standing_frame_right, True, False)
        self.walking_frame_startup_left = pygame.transform.flip(self.walking_frame_startup_right, True, False)
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        now = pygame.time.get_ticks()
        if self.xvel != 0 and self.onGround == True:
            self.walking = True
        else:
            self.walking = False
            self.walking_startup = 1
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_right)
                if self.xvel > 0:
                    if self.walking_startup:
                        self.image = self.walking_frame_startup_right
                        self.walking_startup = 0
                    else:
                        self.image = self.walking_frames_right[self.current_frame]
                    self.goingRight = 1
                else:
                    if self.walking_startup:
                        self.image = self.walking_frame_startup_left
                        self.walking_startup = 0
                    else:
                        self.image = self.walking_frames_left[self.current_frame]
                    self.goingRight = 0
                self.rect = self.image.get_rect()
        elif self.walking == False and self.onGround == True:
            if self.goingRight:
                self.image = self.standing_frame_right
            else:
                self.image = self.standing_frame_left

    def update(self, up, down, left, right, running, platforms):
        if up:
            #je kan alleen springen als je op een platform staat
            if self.onGround: self.yvel -= 8
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            #zwaartekracht als je niet op een platform staat
            self.yvel += 0.3
            #maximum valsnelheid
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
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
                    pygame.event.post(pygame.event.Event(QUIT)) #einde van level, nog niet toegevoegd
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


class Platform(Entity):
    def __init__(self, x, y, number):
        Entity.__init__(self)
        self.load_images()
        self.image = PlatformImages['platform_'+number]
        self.rect = Rect(x, y, 32, 32)

    def load_images(self):
        global PlatformImages
        PlatformImages['platform_1'] = pygame.image.load(r"/Profielwerkstuk/Objects/blok1.png").convert() #verander r"C:/....png" naar waar blok1 staat opgeslagen op pc
        PlatformImages['platform_2'] = pygame.image.load(r"/Profielwerkstuk/Objects/blok2.png").convert()

class Background(Entity):
    def __init__(self, x, y, number):
        Entity.__init__(self)
        self.load_images()
        self.image = BGImages['BG_'+number]
        self.rect = Rect(x, y, 32, 32)

    def load_images(self):
        global BGImages
        BGImages['BG_1'] = pygame.image.load(r"/Profielwerkstuk/Objects/achtergrond1.png").convert() #als transparente dingen niet werken probeer .convert_alpha()
        BGImages['BG_2'] = pygame.image.load(r"/Profielwerkstuk/Objects/achtergrond2.png").convert()
        BGImages['BG_3'] = pygame.image.load(r"/Profielwerkstuk/Objects/achtergrond3.png").convert()

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
    main()