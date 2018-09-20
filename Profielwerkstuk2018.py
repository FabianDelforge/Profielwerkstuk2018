import pygame, glob, sys
vec = pygame.math.Vector2
clock = pygame.time.Clock()

pygame.init()

############
##SETTINGS##
############

#Visual
pygame.display.set_caption('Profielwerkstuk2018')
display_width = 800
display_height = 600
FPS = 60
col_white = (255,255,255)
col_black = (0,0,0)
col_red = (255,0,0)
col_green = (0,255,0)
col_blue = (0,0,255)
#Player
player_width = 100
player_height = 140
player_acc = 0.5
player_friction = -0.12
player_grav = 0.2
#Platform
platform_number = 0
platform_parts_total = 0
platformImages = {}

############
##SETTINGS##
############

screen = pygame.display.set_mode((display_width, display_height))

class player(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
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
        self.game = game
            
    def load_images(self):
        self.standing_frame_right = pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_rest.png")
        self.standing_frame_right = pygame.transform.scale(self.standing_frame_right,(player_width,player_height))
        self.walking_frame_startup_right = pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_2.png")
        self.walking_frame_startup_right = pygame.transform.scale(self.walking_frame_startup_right,(player_width,player_height))
        self.walking_frames_right = [pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_3.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_4.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_5.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_6.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_7.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_8.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_9.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_10.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_11.png"),
                                     pygame.image.load("C:/Users/Gebruiker/Downloads/Profielwerkstuk/Character Sprite Templates/pws_character_sprite_template_run_12.png")]
        for i in range (0, len(self.walking_frames_right)):
            self.walking_frames_right[i] = pygame.transform.scale(self.walking_frames_right[i],(player_width,player_height))
        self.standing_frame_left = pygame.transform.flip(self.standing_frame_right, True, False)
        self.walking_frame_startup_left = pygame.transform.flip(self.walking_frame_startup_right, True, False)
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame, True, False))

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
                self.rect = self.image.get_rect()
        else:
            if self.goingRight:
                self.image = self.standing_frame_right
            else:
                self.image = self.standing_frame_left

        
    def update(self):
        self.acc = vec(0,player_grav)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -player_acc
        elif keys[pygame.K_RIGHT]:
            self.acc.x = player_acc
        if keys[pygame.K_SPACE]:
            self.jump()
            
        #apply friction
        self.acc.x += self.vel.x * player_friction
        #motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5*self.acc

        #dont run off the screen
        if self.pos.x > display_width + self.rect.width/2:
            self.pos.x = -self.rect.width/2
        if self.pos.x < -self.rect.width/2:
            self.pos.x = display_width + self.rect.width/2
        
        self.rect.midbottom = self.pos

        #beweegt scherm naar rechts als speler dicht bij de rechterkant is
        global move_screen
        move_screen = False
        if self.pos.x >= display_width*0.7:
            self.pos.x -= self.vel.x
            move_screen = True


    def jump(self):
        #checks if standing on platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -8



def formPlatform(x, y, w): #w is amount of parts, .5 for small part
    w_big = int(w)  #removes the .5 (if present)
    w_small = False
    if w_big != w:
        w_small = True
    im_x = x

    platform_name = "Platform_"
    global platform_number
    global platform_parts_total
    platform_number += 1
    platform_name += str(platform_number)

    platform_parts = 1
    platform_parts_total += 1
    globals()[platform_name+"_"+str(platform_parts)] = Platform(im_x,y, "edge_left")
    im_x += 80 #lenght small
        
    for i in range(0, w_big):
        platform_parts += 1
        platform_parts_total += 1
        globals()[platform_name+"_"+str(platform_parts)] = Platform(im_x,y, "mid_big")
        im_x += 160 #lenght big
    if w_small:
        platform_parts += 1
        platform_parts_total += 1
        globals()[platform_name+"_"+str(platform_parts)] = Platform(im_x,y, "mid_small")
        im_x += 80 
    platform_parts += 1
    platform_parts_total += 1
    globals()[platform_name+"_"+str(platform_parts)] = Platform(im_x,y, "edge_right")

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, part):
        pygame.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = platformImages["self.platform_"+part]  #for example: part = "mid_big"  self.image = self.platform_mid_big
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        #put in platformImages dict so it can be used dynamically at self.image
        global platformImages
        platformImages['self.platform_mid_big'] = pygame.image.load(r"C:/Users/Gebruiker/Downloads/Profielwerkstuk/Objects/Pws Platform Middle Big.jpg")
        platformImages['self.platform_mid_small'] = pygame.image.load(r"C:/Users/Gebruiker/Downloads/Profielwerkstuk/Objects/Pws Platform Middle Small.jpg")
        platformImages['self.platform_edge_left'] = pygame.image.load(r"C:/Users/Gebruiker/Downloads/Profielwerkstuk/Objects/Pws Platform Edge Left.jpg")
        platformImages['self.platform_edge_right'] = pygame.image.load(r"C:/Users/Gebruiker/Downloads/Profielwerkstuk/Objects/Pws Platform Edge Right.jpg")





class Game:
    def __init__(self):
        self.running = True

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = player(self)
        self.all_sprites.add(self.player)
        formPlatform(50, 500, 3.5)
        for platform in range(1, platform_number+1):
            try:
                for platformPart in range(1, platform_parts_total+platform_number+1):
                    self.all_sprites.add(globals()["Platform_"+str(platform)+"_"+str(platformPart)])
                    self.platforms.add(globals()["Platform_"+str(platform)+"_"+str(platformPart)])
            except KeyError:
                break           #if Platform_1_x doesnt exist, go to Platform_2_1
            

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
           
        
            self.player.update()
            self.player.animate()
        

            pygame.display.update()
            clock.tick(FPS)

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top + 1
            self.player.vel.y = 0
        if move_screen == True:
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x
                if plat.rect.right <= 0:
                    plat.kill()
            move_screen == False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        screen.fill((100,200,255))
        self.all_sprites.draw(screen)

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
