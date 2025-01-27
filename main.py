import pygame
import json

from inventory import ItemList

pygame.init()
screen = pygame.display.set_mode(size=(600, 600))
clock = pygame.time.Clock()

grid = {}
displayed_rects = {}
current_page = 1
current_item = None

ItemList = ItemList()
item_list = ItemList.get_item_pages()

textures = {}

# Load crafting recipes
with open('crafting_recipes.json') as f:
    recipes = json.load(f)

def snatch_to_middle_of_rect(bg_rect: pygame.rect.Rect, fg_rect: pygame.rect.Rect):
    return (bg_rect.centerx - fg_rect.width // 2, bg_rect.centery - fg_rect.height // 2)

def check_crafting(grid):
    for recipe_name, recipe in recipes.items():
        pattern = recipe["pattern"]
        key = recipe["key"]
        match = True
        for i, row in enumerate(pattern):
            for j, char in enumerate(row):
                if char == " ":
                    continue
                grid_index = i * 3 + j
                if grid_index not in grid or grid[grid_index]["name"] != key[char]["item"]:
                    match = False
                    break
            if not match:
                break
        if match:
            return recipe["result"]["item"]
    return None

while True:
    screen.fill("gray")

    # Draw the grid
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

    for i, item in enumerate(item_list[current_page]):
        if item_list[current_page][i]["texture"] != None:
            if item_list[current_page][i]["texture"] not in textures:
                textures[item_list[current_page][i]["texture"]] = pygame.image.load(item_list[current_page][i]["texture"])

            screen.blit(pygame.transform.scale(textures[item_list[current_page][i]["texture"]], (40, 40)), (55 + i * 50, 10))
        else:
            item_rect = pygame.draw.rect(
                surface=screen,
                color=pygame.Color(item_list[current_page][i]["color"]),
                rect=pygame.Rect((55 + i * 50, 10), (40, 40)),
                border_radius=5
            )

        if i not in displayed_rects:
            if item_list[current_page][i]["texture"] != None:
                displayed_rects[i] = {}
                displayed_rects[i]["texture"] = item_list[current_page][i]["texture"]
                displayed_rects[i]["name"] = item_list[current_page][i]["name"]
            else:
                displayed_rects[i] = {}
                displayed_rects[i]["color"] = item_list[current_page][i]["color"]
                displayed_rects[i]["name"] = item_list[current_page][i]["name"]

        text = pygame.font.Font(None, 36).render(f"{i}", True, "white")
        screen.blit(text, (55 + i * 50, 50))

    if current_page > 1:
        left_triangle = pygame.draw.polygon(
            screen, "black", [[10, 30], [35, 10], [35, 50]]
        )

    if current_page < len(item_list):
        right_triangle = pygame.draw.polygon(
            screen, "black", [[590, 30], [565, 10], [565, 50]]
        )

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            current_item = pygame.key.name(event.key) if pygame.key.name(event.key).isnumeric() else None

        if event.type == pygame.QUIT:
            pygame.quit()
        
        if pygame.mouse.get_pressed()[0]:
            for i, rect in enumerate(rects):
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if current_rect != None:
                        if snatch_to_middle_of_rect(rect, current_rect):
                            if rects.index(rect) not in grid:
                                grid[rects.index(rect)] = {}
                                if "texture" in displayed_rects[int(current_item)]:
                                    grid[rects.index(rect)]["texture"] = displayed_rects[int(current_item)]["texture"]
                                else:
                                    grid[rects.index(rect)]["color"] = displayed_rects[int(current_item)]["color"]
                                grid[rects.index(rect)]["name"] = displayed_rects[int(current_item)]["name"]
                            grid[rects.index(rect)] = displayed_rects[int(current_item)]
                            print(grid)
                    elif current_rect == None:
                        if rects.index(rect) in grid:
                           del grid[rects.index(rect)]
                        print(grid)

            if current_page > 1:
                if left_triangle:
                    if left_triangle.collidepoint(pygame.mouse.get_pos()):
                        current_page -= 1
                        current_item = None
                        displayed_rects = {}
            
            if current_page < len(item_list):
                if right_triangle:
                    if right_triangle.collidepoint(pygame.mouse.get_pos()):
                        current_page += 1
                        current_item = None
                        displayed_rects = {}

    for i, rect in enumerate(rects):
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(
                surface=screen,
                color=pygame.Color(110, 110, 110),
                rect=pygame.Rect(rect.topleft, (100, 100)),
                border_radius=5
            )

    for i, item in grid.items():
        if item != None:
            try:
                if "texture" in item:
                   if item["texture"] not in textures:
                        textures[item["texture"]] = pygame.image.load(item["texture"])

                if "texture" in item:
                    screen.blit(pygame.transform.scale(textures[item["texture"]], (50, 50)), (rects[i].centerx - 25, rects[i].centery - 25))
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                pygame.draw.rect(
                    surface=screen,
                    color=pygame.Color(item["color"]),
                    rect=pygame.Rect((rects[i].centerx - 25, rects[i].centery - 25), (50, 50)),
                    border_radius=5
                )

    try:
        if current_item != None and item_list[current_page][int(current_item)]["texture"] != None:
            if item_list[current_page][int(current_item)]["texture"] not in textures:
                textures[item_list[current_page][int(current_item)]["texture"]] = pygame.image.load(item_list[current_page][int(current_item)]["texture"])

            texture = pygame.transform.scale(textures[item_list[current_page][int(current_item)]["texture"]], (50, 50))
            current_rect = screen.blit(texture, pygame.mouse.get_pos())
        else:
            current_rect = (
                    pygame.draw.rect(
                        surface=screen,
                        color=pygame.Color(displayed_rects[int(current_item)]["color"]),
                        rect=pygame.Rect((pygame.mouse.get_pos()), (50, 50)),
                        border_radius=5
                    ) if (current_item != None) else None
                )
    except KeyError:
        current_rect = None

    # Check crafting
    crafted_item = check_crafting(grid)
    if crafted_item:
        print(f"Crafted item: {crafted_item}")

    pygame.display.flip()
    clock.tick(60)
