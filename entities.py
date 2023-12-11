import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, game, position, size):
        super().__init__()

        game.blocks.add(self)
        game.all_sprites.add(self)

        # Image
        self.image = pygame.Surface(size)
        self.fill_colour = 'blue'
        self.image.fill(self.fill_colour)

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()


class Portal(pygame.sprite.Sprite):
    def __init__(self, game, position, size, portal_type):
        super().__init__()

        if portal_type == 'in':
            game.in_portals.add(self)
        if portal_type == 'out':
            game.out_portals.add(self)
        game.all_portals.add(self)
        game.all_sprites.add(self)

        # Image
        self.image = pygame.Surface(size)
        self.fill_colour = 'green'
        self.image.fill(self.fill_colour)

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, game, position, size, gravity=(0, 0.1)):
        super().__init__()
        
        game.all_sprites.add(self)
        for group in sprite_groups:
            group.add(self)

        # Setup
        self.game = game

        # Image
        self.image = pygame.Surface(size)
        self.image.fill('red')

        # Controls
        self.keys = None

        # Type-dependant variables
        if game.players in sprite_groups:
            self.keys = {'up': pygame.K_w, 'left': pygame.K_a, 'down': pygame.K_s, 'right': pygame.K_d}
            self.image.fill('red')
        if game.objects in sprite_groups:
            self.image.fill('orange')

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

        # Movement (Inputted)
        self.position = pygame.Vector2(position)
        self.gravity = pygame.Vector2(gravity)

        # Movement (Empty)
        self.velocity = pygame.Vector2(float(0), float(0))
        self.acceleration = pygame.Vector2(float(0), float(0))
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # Movement (Hard-Coded)
        self.terminal_velocity = pygame.Vector2(3, 5)
        self.drag_factor = 0.85  # A value less than 1 to reduce velocity
        self.movement_acceleration = 0.4
        self.jump_velocity = 3.1
        self.velocity_transfer_percentage = 0.75 # amount of velocity transferred when colliding with an object

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        # make acceleration equal movement_acceleration and handle jumping dependent on gravity direction
        if self.keys:
            if self.gravity.y != 0:
                if (self.gravity.y > 0 and self.collisions['bottom']) or (self.gravity.y < 0 and self.collisions['top']):
                    self.velocity.y = -self.jump_velocity if keys_pressed[self.keys['up']] else (self.jump_velocity if keys_pressed[self.keys['down']] else self.velocity.y)
                    self.acceleration.x = self.movement_acceleration if keys_pressed[self.keys['right']] else (-self.movement_acceleration if keys_pressed[self.keys['left']] else 0)
                else:
                    self.acceleration.x = 0

            if self.gravity.x != 0:
                if (self.gravity.x > 0 and self.collisions['right']) or (self.gravity.x < 0 and self.collisions['left']):
                    self.velocity.x = -self.jump_velocity if keys_pressed[self.keys['left']] else (self.jump_velocity if keys_pressed[self.keys['right']] else self.velocity.x)
                    self.acceleration.y = self.movement_acceleration if keys_pressed[self.keys['down']] else (-self.movement_acceleration if keys_pressed[self.keys['up']] else 0)
                else:
                    self.acceleration.y = 0
        else:
            self.acceleration = pygame.Vector2(0, 0)

    def collision(self, direction):
        collision_groups = [
            self.game.blocks,
            self.game.players,
            self.game.objects,
        ]

        # Using a set to avoid duplicates
        collision_sprites = set()

        # Check collision with all groups and add to the set
        for group in collision_groups:
            for sprite in pygame.sprite.spritecollide(self, group, False):
                if sprite != self:  # Exclude self from the results
                    collision_sprites.add(sprite)

        # If you need a list instead of a set, convert it back to a list
        collision_sprites = list(collision_sprites)

        if not collision_sprites:
            return

        if direction == 'horizontal':
            for sprite in collision_sprites:
                # If colliding with an object, transfer velocity
                if self.game.objects.has(sprite):
                    sprite.velocity = (self.velocity.copy() * self.velocity_transfer_percentage)

                # Check collision on the right
                if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                    self.collisions['right'] = True
                    self.velocity.x = 0
                    self.rect.right = sprite.rect.left
                    self.position.x = self.rect.x

                # Check collision on the left
                if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                    self.collisions['left'] = True
                    self.velocity.x = 0
                    self.rect.left = sprite.rect.right
                    self.position.x = self.rect.x

        if direction == 'vertical':
            for sprite in collision_sprites:
                # If colliding with an object, transfer velocity
                if self.game.objects.has(sprite):
                    sprite.velocity = (self.velocity.copy() * self.velocity_transfer_percentage)

                # Check collision on the bottom
                if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                    self.collisions['bottom'] = True
                    self.velocity.y = 0
                    self.rect.bottom = sprite.rect.top
                    self.position.y = self.rect.y

                # Check collision on the top
                if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                    self.collisions['top'] = True
                    self.velocity.y = 0
                    self.rect.top = sprite.rect.bottom
                    self.position.y = self.rect.y

    def block_drag(self):
        near_zero_threshold = 0.2  # Velocity threshold below which it is set to zero

        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity.x *= self.drag_factor
            if abs(self.velocity.x) < near_zero_threshold and self.velocity.x != 0 and self.acceleration.x == 0:
                self.velocity.x = 0

        if self.collisions['left'] or self.collisions['right']:
            self.velocity.y *= self.drag_factor
            if abs(self.velocity.y) < near_zero_threshold and self.velocity.y != 0 and self.acceleration.y == 0:
                self.velocity.y = 0

    def update(self):
        # Save Previous Frame
        self.old_rect = self.rect.copy()

        # Calculate new velocities and accelerations from user input
        self.input()

        # Update velocity
        self.velocity += self.acceleration + self.gravity
        self.velocity.x = max(min(self.velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x)
        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)

        # Decrease velocities depending on collisions
        self.block_drag()

        # Reset colliding bools before calculating collisions (and after calculating input())
        self.collisions = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # Update Position and check collisions
        self.position.x += self.velocity.x + self.gravity.x
        self.rect.x = self.position.x
        self.collision('horizontal')
        self.position.y += self.velocity.y + self.gravity.y
        self.rect.y = self.position.y
        self.collision('vertical')
