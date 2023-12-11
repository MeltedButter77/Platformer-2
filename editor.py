import sys
import pygame
import entities


render_scale = 2
new_block_origin = None


class Editor:
    def __init__(self):
        # Pygame Setup
        pygame.init()
        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Physics Entities
        entities.PhysicsEntity([self.objects], self, (500, 50), (12, 12), gravity=(0, 0.1)),
        entities.PhysicsEntity([self.players], self, (100, 600), (12, 12), gravity=(0, 0.1))

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
        global new_block_origin
        while True:
            self.screen.fill((0, 0, 100))

            self.blocks.draw(self.screen)
            self.objects.draw(self.screen)
            self.players.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    entities.Block(self, event.pos, (0, 0))
                    new_block_origin = pygame.Vector2(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] and new_block_origin:
                        block = self.blocks.sprites()[-1]

                        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

                        # Determine the top-left and bottom-right points
                        top_left = (min(new_block_origin[0], mouse_pos[0]), min(new_block_origin[1], mouse_pos[1]))
                        bottom_right = (max(new_block_origin[0], mouse_pos[0]), max(new_block_origin[1], mouse_pos[1]))

                        # Calculate width and height
                        width = bottom_right[0] - top_left[0]
                        height = bottom_right[1] - top_left[1]

                        # Create new rects and images and update image colour
                        block.rect = pygame.Rect(top_left, (width, height))
                        block.image = pygame.Surface(block.rect.size)
                        block.image.fill(block.fill_colour)
                if event.type == pygame.MOUSEBUTTONUP:
                    block = self.blocks.sprites()[-1]
                    if block.rect.size[0] < 5 or block.rect.size[1] < 5:
                        block.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.blocks.sprites()[-1].kill()
                    if event.key == pygame.K_SPACE:
                        print(self.blocks)

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
