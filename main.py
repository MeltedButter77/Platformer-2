import sys
import pygame
from entities import PhysicsEntity
import blocks


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Platformer!")
        self.screen = pygame.display.set_mode((800, 800))

        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.crates = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.entities = [
            PhysicsEntity([self.crates, self.walls], self, 'crate', (500, 50), (12, 12), gravity=(0, 0.1)),
            PhysicsEntity([self.players], self, 'player', (100, 600), (12, 12), gravity=(0, 0.1))
        ]

        self.blocks = [
            blocks.Block(self, (0, 750), (800, 50)),  # bottom
            blocks.Block(self, (0, 0), (800, 50)),  # top
            blocks.Block(self, (400, 720), (400, 10)),  # middle
            blocks.Block(self, (0, 0), (50, 800)),  # left
            blocks.Block(self, (750, 0), (50, 800)),  # right
        ]

    def run(self):
        while True:
            self.screen.fill((0, 0, 100))

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


Game().run()
