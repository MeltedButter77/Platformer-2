import pygame



def resolve_entity_collisions(entity_list):
    for i in range(len(entity_list)):
        for j in range(i + 1, len(entity_list)):
            entity1 = entity_list[i]
            entity2 = entity_list[j]

            # Check if the entities collide
            if entity1.rect.inflate(1, 1).colliderect(entity2.rect):
                print("collide")


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, entity_type, position, size, gravity=(0, 0.1)):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Setup
        self.game = game
        self.type = entity_type

        # Image
        self.image = pygame.Surface(size)
        self.image.fill('red')

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

        # Movement (Inputted)
        self.position = pygame.Vector2(position)
        self.gravity = pygame.Vector2(gravity)
        self.velocity = pygame.Vector2(float(0), float(0))
        self.acceleration = pygame.Vector2(float(0), float(0))
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # Movement (Hard-Coded)
        self.terminal_velocity = pygame.Vector2(5, 5)
        self.friction = 0.2
        self.movement_acceleration = 0.5
        self.jump_velocity = 3.1

        # Control
        if entity_type == 'player':
            self.keys = {'up': pygame.K_w, 'left': pygame.K_a, 'down': pygame.K_s, 'right': pygame.K_d}
        else:
            self.keys = None

    def update(self, keys_pressed=None):
        self.old_rect = self.rect.copy() # previous frame

        # make acceleration equal movement_acceleration and handle jumping dependent on gravity direction
        if self.keys:
            if self.gravity.y != 0:
                if (self.gravity.y > 0 and self.collisions['bottom']) or (self.gravity.y < 0 and self.collisions['top']):
                    self.velocity.y = -self.jump_velocity if keys_pressed[self.keys['up']] else (self.jump_velocity if keys_pressed[self.keys['down']] else 0)
                    self.acceleration.x = self.movement_acceleration if keys_pressed[self.keys['right']] else (-self.movement_acceleration if keys_pressed[self.keys['left']] else 0)
                else:
                    self.acceleration.x = 0

            if self.gravity.x != 0:
                if (self.gravity.x > 0 and self.collisions['right']) or (self.gravity.x < 0 and self.collisions['left']):
                    self.velocity.x = -self.jump_velocity if keys_pressed[self.keys['left']] else (self.jump_velocity if keys_pressed[self.keys['right']] else 0)
                    self.acceleration.y = self.movement_acceleration if keys_pressed[self.keys['down']] else (-self.movement_acceleration if keys_pressed[self.keys['up']] else 0)
                else:
                    self.acceleration.y = 0
        else:
            self.acceleration = pygame.Vector2(0, 0)

        # Update velocity
        self.velocity += self.acceleration + self.gravity

        # Reset colliding bools before calculating
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # calculate x and y collisions and reset player velocity and pos if collided
        self.position.x += self.velocity.x
        self.rect.topleft = self.position  # update Rect to current position
        for block in self.game.blocks:
            if self.rect.inflate(1, 0).colliderect(block):
                if self.velocity.x > 0:
                    self.collisions['bottom'] = True
                if self.velocity.x < 0:
                    self.collisions['top'] = True
            if self.rect.colliderect(block):
                if self.velocity.x > 0:
                    self.rect.right = block.left
                if self.velocity.x < 0:
                    self.rect.left = block.right
                self.position.x = self.rect.x
        if self.collisions['left'] or self.collisions['right']:
            self.velocity.x = 0

        self.position.y += self.velocity.y
        self.rect.topleft = self.position # update Rect to current pos
        for block in self.game.blocks:
            if self.rect.inflate(0, 1).colliderect(block):
                if self.velocity.y > 0:
                    self.collisions['bottom'] = True
                if self.velocity.y < 0:
                    self.collisions['top'] = True
            if self.rect.colliderect(block):
                if self.velocity.y > 0:
                    self.rect.bottom = block.top
                if self.velocity.y < 0:
                    self.rect.top = block.bottom
                self.position.y = self.rect.y
        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity.y = 0
        
        self.rect.topleft = self.position # update Rect to current pos

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
