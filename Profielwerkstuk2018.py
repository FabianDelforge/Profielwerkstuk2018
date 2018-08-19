import pygame, glob

pygame.init()

display_width = 800
display_height = 600
FPS = 60

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Profielwerkstuk2018')

clock = pygame.time.Clock()

class player:
    class pos:
        def __init__(self):
            self.x = display_width * 0.3
            self.y = display_height/2
    class vel:
        def __init__(self):
            self.x = 0
            self.y = 0
    class acc:
        def __init__(self):
            self.x = 0
            self.y = 0
    
    def __init__(self):
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame_right
        self.pos = self.pos()
        self.vel = self.vel()
        self.acc = self.acc()
        self.goingRight = 1      #if facing right: 1       if facing left: 0
        self.walking_startup = 1 #if starting to walk: 1   if already walking: no need to show _run_2, so 0

            
    def load_images(self):
        self.standing_frame_right = pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_rest.png")
        self.standing_frame_right = pygame.transform.scale(self.standing_frame_right,(100,140))
        self.walking_frame_startup_right = pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_2.png")
        self.walking_frame_startup_right = pygame.transform.scale(self.walking_frame_startup_right,(100,140))
        self.walking_frames_right = [pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_3.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_4.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_5.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_6.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_7.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_8.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_9.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_10.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_11.png"),
                                     pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_12.png")]
        for i in range (0, len(self.walking_frames_right)):
            self.walking_frames_right[i] = pygame.transform.scale(self.walking_frames_right[i],(100,140))
        self.standing_frame_left = pygame.transform.flip(self.standing_frame_right, True, False)
        self.walking_frame_startup_left = pygame.transform.flip(self.walking_frame_startup_right, True, False)
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -5
            self.pos.x += self.vel.x
        elif keys[pygame.K_RIGHT]:
            self.vel.x = 5
            self.pos.x += self.vel.x
        else:
            self.vel.x = 0

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
            self.walking_startup = 1
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_right)
                if self.vel.x > 0:
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
        else:
            if self.goingRight:
                self.image = self.standing_frame_right
            else:
                self.image = self.standing_frame_left


class Game:
    def __init__(self):
        self.running = True

    def new(self):
        pass

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
           
        
            player.update()
            player.animate()
        
            screen.blit(player.image, (player.pos.x, player.pos.y))
            pygame.display.update()
            clock.tick(FPS)

    def update(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        screen.fill((100,200,255))

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
        

    
Game = Game()
        
player = player()
player.load_images()


while Game.running:
    Game.new()
    Game.run()
    Game.show_go_screen()
    
pygame.quit()
quit()
