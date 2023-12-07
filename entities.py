import pygame


class PhysicsEntity:
    def __init__(self, game, entity_type, position, size, gravity=(0, 0.1)):
        self.game = game
        self.type = entity_type
        self.pos = list(position)
        self.size = size
        self.gravity = list(gravity)

        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.terminal_velocity = [5, 5]
        self.collision = 0

    def update(self, movement=(0, 0)):
        self.velocity[0] = min(self.terminal_velocity[0], (self.velocity[0] + self.gravity[0])) # Adds gravity to velocity with cap
        self.velocity[1] = min(self.terminal_velocity[1], (self.velocity[1] + self.gravity[1]))

        self.velocity[0] = min(self.terminal_velocity[0], (self.velocity[0] + self.acceleration[0]))  # Adds gravity to velocity with cap
        self.velocity[1] = min(self.terminal_velocity[1], (self.velocity[1] + self.acceleration[1]))

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        print(frame_movement)

        self.pos[0] += frame_movement[0]
        entity_rect = pygame.Rect(self.pos, self.size)
        for rect in self.game.blocks:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.collision = 1
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    self.collision = -1
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
        self.collision = 0

        self.pos[1] += frame_movement[1]
        entity_rect = pygame.Rect(self.pos, self.size)
        for rect in self.game.blocks:
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.collision = 1
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.collision = -1
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
        if self.collision == 1: # if collided with floor, jump
            self.velocity[1] = -5
        self.collision = 0

    def render(self, surface):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(surface, (255, 0, 0), rect)


