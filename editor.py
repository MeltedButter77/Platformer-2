import sys
import pygame
import entities
import map

render_scale = 2
new_block_origin = None


class Editor:
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
        global new_block_origin
        while True:
            self.screen.fill((0, 0, 100))

            self.all_portals.draw(self.screen)
            self.blocks.draw(self.screen)
            self.objects.draw(self.screen)
            self.players.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        entities.Block(self, event.pos, (0, 0))
                        new_block_origin = pygame.Vector2(event.pos)
                    if event.button == 3:
                        print('kill')
                        for sprite in self.blocks.sprites():
                            if sprite.rect.collidepoint(event.pos):
                                sprite.kill()
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] and new_block_origin:
                        sprite = self.blocks.sprites()[-1]

                        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

                        # Determine the top-left and bottom-right points
                        top_left = (min(new_block_origin[0], mouse_pos[0]), min(new_block_origin[1], mouse_pos[1]))
                        bottom_right = (max(new_block_origin[0], mouse_pos[0]), max(new_block_origin[1], mouse_pos[1]))

                        # Calculate width and height
                        width = bottom_right[0] - top_left[0]
                        height = bottom_right[1] - top_left[1]

                        # Create new rects and images and update image colour
                        sprite.rect = pygame.Rect(top_left, (width, height))
                        sprite.image = pygame.Surface(sprite.rect.size)
                        sprite.image.fill(sprite.fill_colour)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        sprite = self.blocks.sprites()[-1]
                        if sprite.rect.size[0] < 5 or sprite.rect.size[1] < 5:
                            sprite.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.blocks.sprites()[-1].kill()
                    if event.key == pygame.K_SPACE:
                        for sprite in self.blocks.sprites():
                            print(str(sprite.rect.topleft) + ", " + str(sprite.rect.size) + ",")

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
