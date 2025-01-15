import pygame

pygame.init()
screen = pygame.display.set_mode(size=(600, 600))
clock = pygame.time.Clock()

last_pos = None

inventory = {
    "0": {
        "name": "red",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "red",
        "placed": False,
        "pos": None
    },
    "1": {
        "name": "green",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "green",
        "placed": False,
        "pos": None
    },
    "2": {
        "name": "blue",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "blue",
        "placed": False,
        "pos": None
    },
    "3": {
        "name": "yellow",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "yellow",
        "placed": False,
        "pos": None
    },
    "4": {
        "name": "purple",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "purple",
        "placed": False,
        "pos": None
    },
    "5": {
        "name": "orange",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "orange",
        "placed": False,
        "pos": None
    },
    "6": {
        "name": "pink",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "pink",
        "placed": False,
        "pos": None
    },
    "7": {
        "name": "cyan",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "cyan",
        "placed": False,
        "pos": None
    },
    "8": {
        "name": "brown",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "brown",
        "placed": False,
        "pos": None
    },
    "9": {
        "name": "black",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "black",
        "placed": False,
        "pos": None
    },
    "a": {
        "name": "white",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "white",
        "placed": False,
        "pos": None
    },
    "b": {
        "name": "gray",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "gray",
        "placed": False,
        "pos": None
    },
    "c": {
        "name": "lime",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "lime",
        "placed": False,
        "pos": None
    },
    "d": {
        "name": "magenta",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "magenta",
        "placed": False,
        "pos": None
    },
    "e": {
        "name": "teal",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "teal",
        "placed": False,
        "pos": None
    },
    "f": {
        "name": "navy",
        "rect": pygame.rect.Rect((pygame.mouse.get_pos()), (50, 50)),
        "color": "navy",
        "placed": False,
        "pos": None
    }
}


grid = {}

inventory_pages = {}

current_rects = {}

current_page = 1
current_item = None

for i, item in enumerate(inventory):
    if int((i + 1) / 11 + 1) not in inventory_pages:
        inventory_pages[int((i + 1) / 11 + 1)] = []
    inventory_pages[int((i + 1) / 11 + 1)].append(item)

def snatch_to_middle_of_rect(bg_rect: pygame.rect.Rect, fg_rect: pygame.rect.Rect):
    for key, item in inventory.items():
        if item["placed"] and item["pos"] == (bg_rect.centerx - fg_rect.width // 2, bg_rect.centery - fg_rect.height // 2):
            print(f"Colliding with {key}")
            return False

    return (bg_rect.centerx - fg_rect.width // 2, bg_rect.centery - fg_rect.height // 2)

while True:
    screen.fill("gray")


    # Draw the crafting grid

    rects = []
    for row in range(3):
        for col in range(3):
            rect = pygame.draw.rect(
                surface=screen, 
                color=pygame.Color(90, 90, 90), 
                rect=pygame.Rect((140 + col * 110, 150 + row * 110), (100, 100)),
                border_radius=5
            )
            rects.append((rect))
    
    # Draw the inventory
    
    pygame.draw.rect(
        surface=screen,
        color=pygame.Color(90, 90, 90),
        rect=pygame.Rect(0, 0, 600, 75)
    )

    for i, item in enumerate(inventory_pages[current_page]):
        item_rect = pygame.draw.rect(
            surface=screen,
            color=pygame.Color(inventory[item]["color"]),
            rect=pygame.Rect((55 + i * 50, 10), (40, 40))
        )

        if i not in current_rects:
            current_rects[i] = inventory[item]["color"]

        text = pygame.font.Font(None, 36).render(f"{i}", True, "white")
        screen.blit(text, (55 + i * 50, 50))

    if current_page > 1:
        left_triangle = pygame.draw.polygon(
            screen, "black", [[10, 30], [35, 10], [35, 50]]
        )

    if current_page < len(inventory_pages):
        right_triangle = pygame.draw.polygon(
            screen, "black", [[590, 30], [565, 10], [565, 50]]
        )

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            current_item = pygame.key.name(event.key) if pygame.key.name(event.key).isnumeric() else None

        if event.type == pygame.QUIT:
            print(grid)
            pygame.quit()
        
        if pygame.mouse.get_pressed()[0]:
            for i, rect in enumerate(rects):
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if current_rect != None:
                        last_pos = snatch_to_middle_of_rect(rect, current_rect)
                        if last_pos:
                            if rects.index(rect) not in grid:
                                grid[rects.index(rect)] = current_rects[int(current_item)]
                            grid[rects.index(rect)] = current_rects[int(current_item)]
                    elif current_rect == None:
                        for key, item in inventory.items():
                            if item["pos"] == (rect.centerx - 25, rect.centery - 25):
                                current_item = key

            if current_page > 1:
                if left_triangle:
                    if left_triangle.collidepoint(pygame.mouse.get_pos()):
                        current_page -= 1
                        current_item = None
                        current_rects = {}
            
            if current_page < len(inventory_pages):
                if right_triangle:
                    if right_triangle.collidepoint(pygame.mouse.get_pos()):
                        current_page += 1
                        current_item = None
                        current_rects = {}
                        print(f"Current page: {current_page}, Current item: {current_item}")

    for i, rect in enumerate(rects):
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(
                surface=screen,
                color=pygame.Color(110, 110, 110),
                rect=pygame.Rect(rect.topleft, (100, 100)),
                border_radius=5
            )

    for i, item in grid.items():
        pygame.draw.rect(
            surface=screen,
            color=pygame.Color(item),
            rect=pygame.Rect((rects[i].centerx - 25, rects[i].centery - 25), (50, 50)),
            border_radius=5
        )

    try:
        current_rect = (
                pygame.draw.rect(
                    surface=screen,
                    color=pygame.Color(current_rects[int(current_item)]),
                    rect=pygame.Rect((pygame.mouse.get_pos()), (50, 50)),
                    border_radius=5
                ) if (current_item != None) else None
            )
    except KeyError:
        current_rect = None

    pygame.display.flip()
    clock.tick(60)