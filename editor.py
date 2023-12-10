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
        entities.PhysicsEntity([self.objects], self, 'object', (500, 50), (12, 12), gravity=(0, 0.1)),
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
        global new_block_origin
        while True:
            self.screen.fill((0, 0, 100))

            self.blocks.update() # update blocks so their size can change as we create blocks
            self.blocks.draw(self.screen)
            self.objects.draw(self.screen)
            self.players.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    entities.Block(self, event.pos, (1, 1))
                    new_block_origin = pygame.Vector2(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0] and new_block_origin:
                        block = self.blocks.sprites()[-1]
                        mouse_pos = pygame.Vector2(event.pos)
                        new_size = pygame.Vector2(mouse_pos - new_block_origin)

                        # Bottom Right
                        if new_size.x > 0 and new_size.y > 0:
                            block.size = new_size

                        # Top Right
                        elif new_size.x > 0 > new_size.y:
                            block.position.y = mouse_pos.y
                            block.size.x = new_size.x
                            block.size.y = -new_size.y

                        # Bottom Left
                        elif new_size.x < 0 < new_size.y:
                            block.position.x = mouse_pos.x
                            block.size.x = -new_size.x
                            block.size.y = new_size.y

                        # Top Left
                        elif new_size.x < 0 and new_size.y < 0:
                            block.position = mouse_pos
                            block.size = -new_size
                if event.type == pygame.MOUSEBUTTONUP:
                    block = self.blocks.sprites()[-1]
                    if block.size.x < 5 or block.size.y < 5:
                        self.blocks.remove(block)

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
