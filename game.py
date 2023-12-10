import sys
import pygame
import entities


class Game:
    def __init__(self):
        # Pygame Setup
        pygame.init()
        pygame.display.set_caption("Platformer!")
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Physics Entities
        entities.PhysicsEntity([self.objects], self, 'player', (500, 50), (12, 12), gravity=(0, 0.1)),
        entities.PhysicsEntity([self.players], self, 'player', (100, 600), (12, 12), gravity=(0, 0.1))

        # Map wall Entities
        block_info = [
            (0, 750, 800, 50),  # bottom
            (0, 0, 800, 50),  # top
            (400, 720, 400, 10),  # middle
            (0, 0, 50, 800),  # left
            (750, 0, 50, 800),  # right
        ]
        for info in block_info:
            entities.Block(self, (info[0], info[1]), (info[2], info[3]))

    def run(self):
        while True:
            self.screen.fill((0, 0, 100))

            self.all_sprites.update()
            self.blocks.draw(self.screen)
            self.objects.draw(self.screen)
            self.players.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


Game().run()
