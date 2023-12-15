import sys
import pygame
import map


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
        self.all_portals = pygame.sprite.Group()
        self.no_portal_interact = pygame.sprite.Group()

        map.load_map(self, 1)

    def run(self):
        while True:
            self.screen.fill((0, 0, 100))

            self.all_sprites.update()
            self.all_portals.draw(self.screen)
            self.blocks.draw(self.screen)
            self.objects.draw(self.screen)
            self.players.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for physics_object in self.players.sprites():
                    physics_object.event_input(event)

            pygame.display.update()
            self.clock.tick(60)


Game().run()
