import pygame


class PhysicsEntity:
    def __init__(self, game, entity_type, position, size, gravity=(0, 0.1)):
        self.game = game
        self.type = entity_type
        self.pos = list(position)
        self.size = size
        self.gravity = list(gravity)

        self.velocity = [float(0), float(0)]
        self.acceleration = [float(0), float(0)]
        self.terminal_velocity = [5, 5]
        self.friction = 0.2

        self.movement_acceleration = 0.5
        self.jump_velocity = 3.1

        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}
        self.keys = {'up': pygame.K_w, 'left': pygame.K_a, 'down': pygame.K_s, 'right': pygame.K_d}

    def get_rect(self):
        return pygame.Rect(self.pos, self.size)

    def update(self, keys_pressed=None):
        # make acceleration equal movement_acceleration and handle jumping dependent on gravity direction
        if keys_pressed:
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
        entity_rect = self.get_rect()
        for block in self.game.blocks:
            if entity_rect.inflate(1, 0).colliderect(block):
                if self.velocity[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = block.left
                if self.velocity[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = block.right
                self.pos[0] = entity_rect.x
        if self.collisions['left'] or self.collisions['right']:
            self.velocity[0] = 0

        self.pos[1] += self.velocity[1]
        entity_rect = self.get_rect()
        for block in self.game.blocks:
            if entity_rect.inflate(0, 1).colliderect(block):
                if self.velocity[1] > 0:
                    self.collisions['bottom'] = True
                    entity_rect.bottom = block.top
                if self.velocity[1] < 0:
                    self.collisions['top'] = True
                    entity_rect.top = block.bottom
                self.pos[1] = entity_rect.y
        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity[1] = 0

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.get_rect())
