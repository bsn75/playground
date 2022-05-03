import pygame
from random import randrange

RES = 600
SIZE = 30
apple_count = 7

# Получить новые координаты одного нового яблока
def get_apple():
    return [randrange(0, RES, SIZE), randrange(0, RES, SIZE)]  # Example: [15, 10]


''' Approach 1
def get_apples(count):
    result = []
    for i in range(0, count):
        result.append(get_apple())
    return result
'''

# Получить список координат для указанного количества яблок
# * Использует метод get_apple выше
# Отвечая на вопрос. Ну вот создается список яблок из количества
# так указано было только по одной координате у яблок  при  присваивании
def get_apples(count):
    return [get_apple() for i in range(0, count)]  # Example: [[15,10], [20,15]]


x, y = 150, 150  # randrange(0, RES, SIZE), randrange(0, RES, SIZE) # Случайные значения для стартовой позиции
# apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)

# Теперь вместо этого, мы можем писать так
# Потому что этот метод возвращает то же самое, что и здесь справа от знака равно
# Здесь кортеж был указан "коротким способом" это когда нет скобок вокруг, но 2 значения через запятую
# a = 1,2 это то же самое что и a = (1,2)
#apple_backup = (randrange(0, (RES - SIZE), SIZE), randrange(0, (RES - SIZE), SIZE))
apple_backup = get_apple()

# Первое: Меняем кортеж на список
# Второе: Выносим в ф-цию т.к. она нам еще пригодится
apples = get_apples(apple_count) # Ну другое же дело, и красивее выглядит и понятно

dirs = {'W': True, 'S': True, 'A': True, 'D': True}
length = 1
snake = [[x, y]]
dx, dy = 0, 0  # Здесь можно задать сразу направление движения на старте, без кнопок -да єто смещение я понял
score = 0
fps = 5


pygame.init()
sc = pygame.display.set_mode([RES, RES])

clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)
background = pygame.image.load('assets/1.jpg').convert()  # рисунок для фона

def draw_background():
    # sc.fill(pygame.Color('black'))
    sc.blit(background, (0, 0))

def draw_snake():
    # рисуем змейку
    [(pygame.draw.rect(sc, pygame.Color('Green'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]

def draw_apples():
    for apple in apples:
        # То, о чем я говорил "взять вручную" координаты из яблока
        pygame.draw.rect(sc, pygame.Color('red'), (apple[0], apple[1], SIZE, SIZE))
        pygame.draw.rect(sc, pygame.Color('blue'), (*apple_backup, SIZE, SIZE))  # backup apple
        print('apl 0:', apple[0],'apl 1:', apple[1])


def draw_score():
    render_score = font_score.render(f'SCORE: {score}', True, pygame.Color('orange'))
    sc.blit(render_score, (5, 5))

def get_head():
    global snake
    return snake[-1][0], snake[-1][1]

def check_apple_collision():
    global apple_backup
    global length
    global score
    global fps

    if snake[-1] == apple_backup:
        apple_backup = get_apple()
        length += 1
        score += 1
        fps -= 1
        snake.append(apple_backup)
    for apple in apples:
        # Потому что snake в себе содержит список списков (кортежей, не важно). ((1,1),(2,2)) ...
        # Берем последний, получается элемент (2,2) и из него по очереди берем по нулевому индексу и по первому
        # Ну или можно вариант проще, в одну строку развертыванием. Чтобы тебя не запутывать, сделаю как ниже
        # Здесь я просто сохраняю координаты в удобно читаемые названия переменных.
        snake_x, snake_y = get_head()
        apple_x = apple[0] # Здесь одна координата, правильно. Но мы то перебираем целый список apples.
        apple_y = apple[1]

        # Это вроде очевидно максимально, что тут написано ниже-- да понял - ядумал просто что они не  нужні в форе
        if snake_x == apple_x and snake_y == apple_y:
            length += 1
            score += 1
            fps += 1
            snake.append([apple_x, apple_y])  # Здесь добавляем в змейку координаты яблока

            # Здесь, если условие сработало, то мы этому яблоку берем новые координаты
            # Технически, мы его даже не удаляем , а откуда мі знамем что оно[0,1]
            new_x, new_y = get_apple()
            apple[0] = new_x
            apple[1] = new_y

def move_snake():
    global x
    global y
    global snake

    x += dx * SIZE
    y += dy * SIZE
    snake.append((x, y))
    snake = snake[-length:]

    check_game_over(x, y)


def check_game_over(x, y):
    if x < 0 or x > RES - SIZE or y > RES - SIZE or y < 0:  # вот тут повнимательней!!! len(snake) != len(set(snake))
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            sc.blit(render_end, (RES // 2 - 200, RES // 3))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()


def control_snake():
    global dirs
    global dx
    global dy

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        print('Key pressed W')
    if key[pygame.K_s]:
        print('Key pressed S')
    if key[pygame.K_a]:
        print('Key pressed A')
    if key[pygame.K_d]:
        print('Key pressed D')

    if key[pygame.K_w] and dirs['W']:  # Если нажали W то не можем нажать S
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    if key[pygame.K_s] and dirs['S']:  # Если нажали S то не можем нажать W
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    if key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    if key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True}



def quit_listener():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


while True:
    # За то, намного легче смотреть и находить что за что отвечает. А не всё в одной куче - ну давай
    draw_background()
    draw_snake()
    draw_apples()
    draw_score()

    control_snake()

    check_apple_collision()
    move_snake()

    pygame.display.flip()
    clock.tick(fps)

    quit_listener()
