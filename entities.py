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
    def __init__(self, game, position, size, portal_type, portal_id):
        super().__init__()

        if portal_type == 'in':
            game.in_portals.add(self)
        if portal_type == 'out':
            game.out_portals.add(self)
        game.all_portals.add(self)
        game.all_sprites.add(self)

        # Portal Info
        self.id = portal_id
        self.type = portal_type
        self.position = pygame.Vector2(position)

        # Image
        self.image = pygame.Surface(size)
        self.fill_colour = 'green'
        self.image.fill(self.fill_colour)

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, game, position, size, colour, gravity=(0, 0.1)):
        super().__init__()

        game.all_sprites.add(self)
        for group in sprite_groups:
            group.add(self)

        # Setup
        self.game = game
        self.portal_entities = []
        self.collision_groups = [
            self.game.blocks,
            self.game.players,
            self.game.objects,
        ]

        # Image
        self.image = pygame.Surface(size)
        self.colour = colour
        self.image.fill(colour)

        # Controls
        self.keys = None

        # Carrying
        self.pickup_range = 20
        self.carried_sprite = None
        self.carried_sprite_relative_distance = pygame.Vector2(0, 0)

        # Type-dependant variables
        if game.players in sprite_groups:
            self.keys = {'up': pygame.K_w, 'left': pygame.K_a, 'down': pygame.K_s, 'right': pygame.K_d, 'pickup': pygame.K_SPACE}
        if game.objects in sprite_groups:
            pass

        # Rect
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

        # Movement (Inputted)
        self.position = pygame.Vector2(position)
        self.gravity = pygame.Vector2(gravity)

        # Movement (Empty)
        self.velocity = pygame.Vector2(float(0), float(0))
        self.acceleration = pygame.Vector2(float(0), float(0))
        self.touching = {'top': False, 'left': False, 'bottom': False, 'right': False}

        # Movement (Hard-Coded)
        self.terminal_velocity = pygame.Vector2(3, 5)
        self.drag_factor = 0.85  # A value less than 1 to reduce velocity
        self.movement_acceleration = 0.4
        self.jump_velocity = 3.1
        self.velocity_transfer_percentage = 0.75  # amount of velocity transferred when colliding with an object
        self.max_jumps = 1
        self.jumps = 0
        self.jump_vel_carry_percentage = 0.8  # percentage of jump velocity retained when carrying another object

    def event_input(self, event):

        if not self.keys:
            return

        if event.type == pygame.KEYDOWN:

            if event.key == self.keys['pickup']:
                if self.carried_sprite:

                    # Check if the object is colliding with anything
                    for group in self.collision_groups:
                        for sprite in pygame.sprite.spritecollide(self.carried_sprite, group, False):
                            if sprite != self:
                                print("Cant drop, colliding")
                                return

                    # drop entity
                    self.game.objects.add(self.carried_sprite)
                    self.carried_sprite = None
                    self.carried_sprite_relative_distance = 0
                else:
                    # Calculate nearest_sprite
                    nearest_sprite = None
                    nearest_distance = float('inf')
                    for sprite in self.game.objects:
                        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(sprite.rect.center))
                        if distance < nearest_distance:
                            nearest_sprite = sprite
                            nearest_distance = distance

                    if nearest_distance <= self.pickup_range:
                        self.game.objects.remove(nearest_sprite)
                        self.carried_sprite = nearest_sprite
                        self.carried_sprite_relative_distance = nearest_sprite.position - self.position

            # Jump logic
            if self.jumps < self.max_jumps:
                jump_velocity = self.jump_velocity
                if self.carried_sprite:
                    jump_velocity *= self.jump_vel_carry_percentage
                if self.gravity.y != 0:
                    if event.key == self.keys['up']:
                        self.jumps += 1
                        self.velocity.y = -jump_velocity
                    elif event.key == self.keys['down']:
                        self.jumps += 1
                        self.velocity.y = jump_velocity

                if self.gravity.x != 0:
                    if event.key == self.keys['left']:
                        self.jumps += 1
                        self.velocity.x = -jump_velocity
                    elif event.key == self.keys['right']:
                        self.jumps += 1
                        self.velocity.x = jump_velocity

    def continuous_input(self):
        keys_pressed = pygame.key.get_pressed()

        # make acceleration equal movement_acceleration and handle jumping dependent on gravity direction
        if self.keys:
            if self.gravity.y != 0:
                grounded = (self.gravity.y > 0 and self.touching['bottom']) or (self.gravity.y < 0 and self.touching['top'])

                if grounded:
                    self.jumps = 0

                    if keys_pressed[self.keys['right']]:
                        self.acceleration.x = self.movement_acceleration
                    elif keys_pressed[self.keys['left']]:
                        self.acceleration.x = -self.movement_acceleration
                    else:
                        self.acceleration.x = 0
                else:
                    self.acceleration.x = 0

            if self.gravity.x != 0:
                grounded = (self.gravity.x > 0 and self.touching['right']) or (
                            self.gravity.x < 0 and self.touching['left'])

                if grounded:
                    self.jumps = 0

                    if keys_pressed[self.keys['down']]:
                        self.acceleration.y = self.movement_acceleration
                    elif keys_pressed[self.keys['up']]:
                        self.acceleration.y = -self.movement_acceleration
                    else:
                        self.acceleration.y = 0
                else:
                    self.acceleration.y = 0

        else:
            self.acceleration = pygame.Vector2(0, 0)

    def calc_touching(self):

        # Reset touching bools before calculating touching (and after calculating input())
        self.touching = {'top': False, 'left': False, 'bottom': False, 'right': False}

        def touching_collision(sprite1, sprite2):
            # Expand both rects by 1 pixel in all directions to include touching
            rect1 = sprite1.rect.inflate(1, 1)
            rect2 = sprite2.rect.inflate(1, 1)
            return rect1.colliderect(rect2)

        touching_sprites = set()
        for group in self.collision_groups:
            for sprite in pygame.sprite.spritecollide(self, group, False, touching_collision):
                if sprite != self:  # Exclude self from the results
                    touching_sprites.add(sprite)
        touching_sprites = list(touching_sprites)

        for sprite in touching_sprites:
            # Check collision on the right
            if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                self.touching['right'] = True

            # Check collision on the left
            if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                self.touching['left'] = True

            # Check collision on the bottom
            if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                self.touching['bottom'] = True

            # Check collision on the top
            if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                self.touching['top'] = True

    def collision(self, direction):

        # Using a set to avoid duplicates
        collision_sprites = set()

        # Check collision with all groups and add to the set
        for group in self.collision_groups:
            for sprite in pygame.sprite.spritecollide(self, group, False):
                if sprite != self:  # Exclude self from the results
                    collision_sprites.add(sprite)

        # If you need a list instead of a set, convert it back to a list
        collision_sprites = list(collision_sprites)

        if direction == 'horizontal':
            for sprite in collision_sprites:
                # If colliding with an object, transfer velocity. This is not done for vertical as this does both axis
                if self.game.objects.has(sprite):
                    sprite.velocity = (self.velocity.copy() * self.velocity_transfer_percentage)

                # Check collision on the right
                if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                    self.velocity.x = 0
                    self.rect.right = sprite.rect.left
                    self.position.x = self.rect.x

                # Check collision on the left
                if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                    self.velocity.x = 0
                    self.rect.left = sprite.rect.right
                    self.position.x = self.rect.x

        if direction == 'vertical':
            for sprite in collision_sprites:
                # Check collision on the bottom
                if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                    self.velocity.y = 0
                    self.rect.bottom = sprite.rect.top
                    self.position.y = self.rect.y

                # Check collision on the top
                if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                    self.velocity.y = 0
                    self.rect.top = sprite.rect.bottom
                    self.position.y = self.rect.y

    def check_portals(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.game.all_portals, False)

        # Once physicObject leaves portal, re-enable its calculation
        if not collision_sprites:
            for entity in self.portal_entities:
                entity.kill()
            self.portal_entities = []
            if self.game.no_portal_interact.has(self):
                self.game.no_portal_interact.remove(self)
            return

        if not self.game.no_portal_interact.has(self):
            for portal in collision_sprites:
                relative_position = self.position - portal.position
                out_portals = []

                for out_portal in self.game.all_portals:
                    if out_portal.id == portal.id and portal != out_portal:
                        out_portals.append(out_portal)

                for i, out_portal in enumerate(out_portals):
                    if portal.rect.contains(self):
                        # if player is fully within the portal
                        for entity in self.portal_entities:
                            entity.keys = self.keys
                        self.kill()
                    else:
                        # if player is overlapping with portal but not fully inside
                        if len(self.portal_entities) > i:
                            self.portal_entities[i].velocity = self.velocity.copy()
                            self.portal_entities[i].acceleration = self.acceleration.copy()
                            self.portal_entities[i].position = out_portal.position.copy() + relative_position
                        else:
                            self.portal_entities.insert(i, PhysicsEntity(self.groups(), self.game, out_portal.position.copy() + relative_position, self.rect.size, self.colour, self.gravity.copy()))
                            self.portal_entities[i].keys = None
                            self.game.no_portal_interact.add(self.portal_entities[i])

    def ground_drag(self):
        near_zero_threshold = 0.2  # Velocity threshold below which it is set to zero

        if self.gravity.y != 0:
            if self.touching['bottom'] or self.touching['top']:
                self.velocity.x *= self.drag_factor
                if abs(self.velocity.x) < near_zero_threshold and self.velocity.x != 0 and self.acceleration.x == 0:
                    self.velocity.x = 0

        if self.gravity.x != 0:
            if self.touching['left'] or self.touching['right']:
                self.velocity.y *= self.drag_factor
                if abs(self.velocity.y) < near_zero_threshold and self.velocity.y != 0 and self.acceleration.y == 0:
                    self.velocity.y = 0

    def update(self):
        if self.game.players.has(self) or self.game.objects.has(self):
            # Save Previous Frame
            self.old_rect = self.rect.copy()

            # Calculate new velocities and accelerations from user input
            self.continuous_input()

            # Update velocity
            self.velocity += self.acceleration + self.gravity
            self.velocity.x = max(min(self.velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x)
            self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)

            # Decrease velocities depending on collisions
            self.ground_drag()

            # Update Position and check collisions
            self.position.x += self.velocity.x + self.gravity.x
            self.rect.x = round(self.position.x)
            self.collision('horizontal')
            self.position.y += self.velocity.y + self.gravity.y
            self.rect.y = round(self.position.y)
            self.collision('vertical')

            # Calc whether Object is touching any collision objects
            self.calc_touching()

            # Check portals
            self.check_portals()

            # Check carry
            if self.carried_sprite:
                self.carried_sprite.position = self.position + self.carried_sprite_relative_distance
                self.carried_sprite.rect.topleft = pygame.Vector2(round(self.carried_sprite.position.x), round(self.carried_sprite.position.y))
                self.game.screen.blit(self.carried_sprite.image, self.carried_sprite.position)
