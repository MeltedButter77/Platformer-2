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
        entities.PhysicsEntity([self.objects], self, (720, 300), (12, 12), gravity=(0, 0.1)),
        entities.PhysicsEntity([self.players], self, (100, 600), (12, 12), gravity=(0, 0.1))

        # Map wall Entities
        block_info = [
            (0, 750, 800, 50),
            (0, 0, 17, 754),
            (779, 0, 20, 754),
            (11, 0, 773, 15),
            (149, 714, 129, 10),
            (320, 733, 277, 24),
            (391, 679, 17, 61),
            (15, 671, 67, 83),
            (403, 696, 167, 11),
            (614, 709, 90, 12),
            (729, 673, 55, 18),
            (757, 627, 26, 15),
            (301, 699, 54, 9),
            (224, 660, 60, 15),
            (247, 607, 11, 59),
            (252, 644, 21, 19),
            (257, 626, 16, 24),
            (113, 673, 65, 20),
            (58, 620, 108, 16),
            (234, 607, 19, 59),
            (305, 621, 86, 19),
            (318, 637, 32, 35),
            (346, 636, 45, 16),
            (448, 636, 73, 26),
            (570, 658, 71, 21),
            (610, 620, 31, 58),
            (637, 647, 58, 19),
            (521, 603, 65, 13),
            (414, 591, 73, 19),
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
