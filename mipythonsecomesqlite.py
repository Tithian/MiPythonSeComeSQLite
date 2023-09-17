import pygame
import random
from debug import debug

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1200
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('My Python se come SQLite')

clock = pygame.time.Clock()

snake_block = 40
snake_speed = 5

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("arial", 35)

sprite_snake = pygame.image.load("snake-graphics.png").convert_alpha()


def get_img(img, columna, fila, size, scale, colorin):
    image = pygame.Surface((size, size)).convert_alpha()
    image.blit(img, (0, 0), ((columna*size), (fila*size), size, size))
    image = pygame.transform.scale(image, (scale, scale))
    image.set_colorkey(colorin)
    return image


def Your_score(score):
    value = score_font.render("Puntos: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    image = None
    fila = 0
    columna = 0
    for num, x in enumerate(snake_list):
        if num == len(snake_list)-1:
            if x[1] > snake_list[num-1][1]:
                image = get_img(sprite_snake, 4, 1, 64, snake_block, black)
            elif x[0] > snake_list[num-1][0]:
                image = get_img(sprite_snake, 4, 0, 64, snake_block, black)
            elif x[0] < snake_list[num-1][0]:
                image = get_img(sprite_snake, 3, 1, 64, snake_block, black)
            else:
                image = get_img(sprite_snake, 3, 0, 64, snake_block, black)
        elif num == 0:
            if x[1] > snake_list[num+1][1]:
                image = get_img(sprite_snake, 3, 2, 64, snake_block, black)
            elif x[1] < snake_list[num+1][1]:
                image = get_img(sprite_snake, 4, 3, 64, snake_block, black)
            elif x[0] < snake_list[num+1][0]:
                image = get_img(sprite_snake, 4, 2, 64, snake_block, black)
            else:
                image = get_img(sprite_snake, 3, 3, 64, snake_block, black)
        else:
            sig = snake_list[num-1]
            ant = snake_list[num+1]
            if ant[0] < x[0] < sig[0] or sig[0] < x[0] < ant[0]:
                image = get_img(sprite_snake, 1, 0, 64, snake_block, black)
            elif ant[0] < x[0] and sig[1] > x[1] or sig[0] < x[0] and ant[1] > x[1]:
                image = get_img(sprite_snake, 2, 0, 64, snake_block, black)
            elif ant[1] < x[1] < sig[1] or sig[1] < x[1] < ant[1]:
                # Vertical Up-Down
                image = get_img(sprite_snake, 2, 1, 64, snake_block, black)
            elif ant[1] < x[1] and sig[0] < x[0] or sig[1] < x[1] and ant[0] < x[0]:
                # Angle Top-Left
                image = get_img(sprite_snake, 2, 2, 64, snake_block, black)
            elif ant[0] > x[0] and sig[1] < x[1] or sig[0] > x[0] and ant[1] < x[1]:
                # Angle Right-Up
                image = get_img(sprite_snake, 0, 1, 64, snake_block, black)
            elif ant[1] > x[1] and sig[0] > x[0] or sig[1] > x[1] and ant[0] > x[0]:
                image = get_img(sprite_snake, 0, 0, 64, snake_block, black)
        dis.blit(image, (x[0], x[1]))


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop(starting):
    global snake_speed
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 2

    food_x = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            dis.fill((30, 30, 30))
            message("¡Has Perdido! Pulsa C-Coninuar o S-Salir", red)
            Your_score(length_of_snake - 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                starting = False

        if x1 >= dis_width or x1 < 0 or y1 < 0 or y1 >= dis_height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill((30, 30, 30))
        manzana = get_img(sprite_snake, 0, 3, 64, snake_block, black)
        dis.blit(manzana, (food_x, food_y))
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head and not starting:
                game_close = True

        our_snake(snake_block, snake_list)
        Your_score(length_of_snake - 1)
        debug(str(snake_speed), 50)
        pygame.display.update()

        if int(x1) == food_x and int(y1) == food_y:
            food_x = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            food_y = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1

            snake_speed = snake_speed + 0.2

        clock.tick(snake_speed)


    pygame.quit()
    quit()


gameLoop(True)
pygame.quit()
quit()
