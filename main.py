import sys

import pygame
from entities import PhysicsEntity


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Platformer!")
        self.screen = pygame.display.set_mode((800, 800))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, 'player', (50, 50), (12, 12), gravity=(0, 0.1))
        self.blocks = [pygame.Rect((0, 750), (800, 50)),  # bottom
                       pygame.Rect((750, 0), (50, 800)),  # right
                       pygame.Rect((0, 0), (50, 800)),  # left
                        pygame.Rect((750, 0), (50, 800)),  # right
                        pygame.Rect((400, 700), (50, 50))]

    def run(self):
        while True:
            self.screen.fill((0, 0, 100))

            self.player.update((1, 0))
            self.player.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:

                        print("down")

            pygame.display.update()
            self.clock.tick(60)


Game().run()
