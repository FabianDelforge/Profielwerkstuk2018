import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Profielwerkstuk2018')

clock = pygame.time.Clock()

def gameLoop():
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        pygame.display.update()
        clock.tick(60)

gameLoop()
pygame.quit()
quit()
