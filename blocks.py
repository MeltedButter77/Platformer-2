import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, game, position, size):
        super().__init__()

        game.walls.add(self)
        game.all_sprites.add(self)

        # Image
        self.image = pygame.Surface(size)
        self.image.fill('blue')

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

