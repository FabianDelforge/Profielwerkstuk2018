import pygame, glob
vec = pygame.math.Vector2

pygame.init()

display_width = 800
display_height = 600
player_width = 100
player_height = 140
FPS = 60
player_acc = 0.5
player_friction = -0.12

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Profielwerkstuk2018')

clock = pygame.time.Clock()

class player:
    def __init__(self):
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame_right
        self.rect = self.image.get_rect()
        self.rect.center = (display_width * 0.3, display_height/2)
        self.pos = vec(display_width * 0.3, display_height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.goingRight = 1      #if facing right: 1       if facing left: 0
        self.walking_startup = 1 #if starting to walk: 1   if already walking: no need to show _run_2, so 0

            
    def load_images(self):
        self.standing_frame_right = pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_rest.png")
        self.standing_frame_right = pygame.transform.scale(self.standing_frame_right,(player_width,player_height))
        self.walking_frame_startup_right = pygame.image.load("\Profielwerkstuk\Character Sprite Templates\Sprite Templates PNG\pws_character_sprite_template_run_2.png")
        self.walking_frame_startup_right = pygame.transform.scale(self.walking_frame_startup_right,(player_width,player_height))
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
            self.walking_frames_right[i] = pygame.transform.scale(self.walking_frames_right[i],(player_width,player_height))
        self.standing_frame_left = pygame.transform.flip(self.standing_frame_right, True, False)
        self.walking_frame_startup_left = pygame.transform.flip(self.walking_frame_startup_right, True, False)
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))
        
    def update(self):
        self.acc = vec(0,0.5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -player_acc
        elif keys[pygame.K_RIGHT]:
            self.acc.x = player_acc

        #apply friction
        self.acc.x += self.vel.x * player_friction
        #motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc

        #dont run off the screen
        if self.pos.x >  display_width:
            self.pos.x = -player_width
        if self.pos.x < -player_width:
            self.pos.x = display_width
        
        self.rect.center = self.pos

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

class Platform:
    def __init__(self, x, y, w, h):
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        self.running = True

    def new(self):
        self.player = player()
        self.player.load_images()
        self.platform = Platform(100, 500, display_width, 30)

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
           
        
            self.player.update()
            self.player.animate()
        
            screen.blit(self.player.image, (self.player.pos.x, self.player.pos.y))
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


while Game.running:
    Game.new()
    Game.run()
    Game.show_go_screen()
    
pygame.quit()
quit()
