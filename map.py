import entities

block_info = []
portal_info = []


def load_map(game, level_id):
    global block_info, portal_info

    if level_id == 1:
        # Players
        entities.PhysicsEntity([game.players], game, (130, 640), (12, 12), 'pink', gravity=(0, 0.1))
        entities.PhysicsEntity([game.players], game, (600, 700), (12, 12), 'red', gravity=(0, 0.1))

        # Objects
        entities.PhysicsEntity([game.objects], game, (720, 300), (12, 12), 'orange', gravity=(0, 0.1)),

        # Portals
        portal_info = [
            (300, 670, 50, 80, 'both', 1),
            (500, 670, 50, 80, 'both', 1),
        ]

        # Map wall Entities
        block_info = [
            (0, 750, 800, 50),
            (0, 0, 17, 754),
            (779, 0, 20, 754),
            (11, 0, 773, 15),
            (149, 714, 129, 10),
            (320, 733, 277, 24),
            (391, 679, 17, 61),
            (15, 671, 67, 83),
            (403, 696, 167, 11),
            (614, 709, 90, 12),
            (729, 673, 55, 18),
            (757, 627, 26, 15),
            (301, 699, 54, 9),
            (224, 660, 60, 15),
            (247, 607, 11, 59),
            (252, 644, 21, 19),
            (257, 626, 16, 24),
            (113, 673, 65, 20),
            (58, 620, 108, 16),
            (234, 607, 19, 59),
            (305, 621, 86, 19),
            (318, 637, 32, 35),
            (346, 636, 45, 16),
            (448, 636, 73, 26),
            (570, 658, 71, 21),
            (610, 620, 31, 58),
            (637, 647, 58, 19),
            (521, 603, 65, 13),
            (414, 591, 73, 19),
        ]

    elif level_id == 2:
        # Players
        entities.PhysicsEntity([game.players], game, (320, 600), (12, 12), 'red', gravity=(0, 0.1))
        entities.PhysicsEntity([game.players], game, (600, 600), (12, 12), 'pink', gravity=(0, 0.1))

        # Objects
        entities.PhysicsEntity([game.objects], game, (720, 300), (12, 12), 'orange', gravity=(0, 0.1)),

        # Portals
        portal_info = [
            (300, 670, 50, 80, 'in', 1),
            (500, 670, 50, 80, 'out', 1),
        ]

        # Map wall Entities
        block_info = [
            (0, 750, 800, 50),
            (0, 0, 17, 754),
            (779, 0, 20, 754),
            (11, 0, 773, 15),
        ]

    for info in portal_info:
        entities.Portal(game, (info[0], info[1]), (info[2], info[3]), info[4], info[5])
    for info in block_info:
        entities.Block(game, (info[0], info[1]), (info[2], info[3]))