import pygame


def handle_collision(entity1, entity2):
    entity1_rect = entity1.rect
    entity2_rect = entity2.rect

    if entity1.velocity[0] > 0:
        entity1_rect.right = entity2_rect.left
        entity1.pos = list(entity1_rect.topleft)

    avg_acceleration = [
        (entity1.acceleration[0] + entity2.acceleration[0]) / 2,
        (entity1.acceleration[1] + entity2.acceleration[1]) / 2
    ]
    avg_velocity = [
        (entity1.velocity[0] + entity2.velocity[0]) / 2,
        (entity1.velocity[1] + entity2.velocity[1]) / 2
    ]

    entity1.acceleration = avg_acceleration.copy()
    entity2.acceleration = avg_acceleration.copy()

    entity1.velocity = avg_velocity.copy()
    entity2.velocity = avg_velocity.copy()


def resolve_entity_collisions(entity_list):
    for i in range(len(entity_list)):
        for j in range(i + 1, len(entity_list)):
            entity1 = entity_list[i]
            entity2 = entity_list[j]

            # Check if the entities collide
            if entity1.rect.inflate(1, 1).colliderect(entity2.rect):
                handle_collision(entity1, entity2)


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
        self.pos = list(position)
        self.gravity = list(gravity)
        self.velocity = [float(0), float(0)]
        self.acceleration = [float(0), float(0)]
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # Movement (Hard-Coded)
        self.terminal_velocity = [5, 5]
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
            if self.gravity[1] != 0:
                if (self.gravity[1] > 0 and self.collisions['bottom']) or (self.gravity[1] < 0 and self.collisions['top']):
                    self.velocity[1] = -self.jump_velocity if keys_pressed[self.keys['up']] else (self.jump_velocity if keys_pressed[self.keys['down']] else 0)
                    self.acceleration[0] = self.movement_acceleration if keys_pressed[self.keys['right']] else (-self.movement_acceleration if keys_pressed[self.keys['left']] else 0)
                else:
                    self.acceleration[0] = 0

            if self.gravity[0] != 0:
                if (self.gravity[0] > 0 and self.collisions['right']) or (self.gravity[0] < 0 and self.collisions['left']):
                    self.velocity[0] = -self.jump_velocity if keys_pressed[self.keys['left']] else (self.jump_velocity if keys_pressed[self.keys['right']] else 0)
                    self.acceleration[1] = self.movement_acceleration if keys_pressed[self.keys['down']] else (-self.movement_acceleration if keys_pressed[self.keys['up']] else 0)
                else:
                    self.acceleration[1] = 0
        else:
            self.acceleration = [0, 0]

        # calculate velocities from acceleration accounting for friction
        def apply_friction_to_acceleration(acceleration, friction_coefficient, mass=1):
            force = mass * acceleration
            frictional_force = friction_coefficient * force
            net_force = force - frictional_force
            return net_force / mass
        new_velocity = [
            self.velocity[0] + self.gravity[0] + apply_friction_to_acceleration(self.acceleration[0], self.friction),
            self.velocity[1] + self.gravity[1] + apply_friction_to_acceleration(self.acceleration[1], self.friction)
        ]
        self.velocity[0] = min(self.terminal_velocity[0], max(-self.terminal_velocity[0], new_velocity[0]))
        self.velocity[1] = min(self.terminal_velocity[1], max(-self.terminal_velocity[1], new_velocity[1]))

        # calculate velocities accounting for friction when colliding
        def apply_friction_to_velocity(velocity, friction_coefficient, mass=1):
            force = mass * velocity
            frictional_force = friction_coefficient * mass
            if velocity > 0:
                net_force = force - frictional_force
            elif velocity < 0:
                net_force = force + frictional_force
            else:
                return 0
            if abs(net_force) < frictional_force:
                return 0
            return net_force / mass
        for i in range(2):
            # require collision for friction to affect
            collision_x = (i == 0) and (self.collisions['top'] or self.collisions['bottom'])
            collision_y = (i == 1) and (self.collisions['left'] or self.collisions['right'])

            if collision_x or collision_y:
                self.velocity[i] = apply_friction_to_velocity(self.velocity[i], self.friction)

        # Reset colliding bools before calculating
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # calculate x and y collisions and reset player velocity and pos if collided
        self.pos[0] += self.velocity[0]
        self.rect.topleft = self.pos # update Rect to current pos
        for block in self.game.blocks:
            if self.rect.inflate(1, 0).colliderect(block):
                if self.velocity[0] > 0:
                    self.collisions['bottom'] = True
                if self.velocity[0] < 0:
                    self.collisions['top'] = True
            if self.rect.colliderect(block):
                if self.velocity[0] > 0:
                    self.rect.right = block.left
                if self.velocity[0] < 0:
                    self.rect.left = block.right
                self.pos[0] = self.rect.x
        if self.collisions['left'] or self.collisions['right']:
            self.velocity[0] = 0

        self.pos[1] += self.velocity[1]
        self.rect.topleft = self.pos # update Rect to current pos
        for block in self.game.blocks:
            if self.rect.inflate(0, 1).colliderect(block):
                if self.velocity[1] > 0:
                    self.collisions['bottom'] = True
                if self.velocity[1] < 0:
                    self.collisions['top'] = True
            if self.rect.colliderect(block):
                if self.velocity[1] > 0:
                    self.rect.bottom = block.top
                if self.velocity[1] < 0:
                    self.rect.top = block.bottom
                self.pos[1] = self.rect.y
        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity[1] = 0
        
        self.rect.topleft = self.pos # update Rect to current pos

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
