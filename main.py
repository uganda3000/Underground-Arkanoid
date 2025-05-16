import pygame
import random

pygame.init()

WIDTH = 1060
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
variatios = [
    'Супер подземный арканоид',
    'Легендарный подземный арканоид',
    'Мега подземный арканоид',
    'Заголовок меняется при перезапуске подземного арканоида!',
    'Подземный арканоид',
]
choise_caption = random.choice(variatios)
pygame.display.set_caption(choise_caption)

clock = pygame.time.Clock()
FPS = 60

BG_COLOR = (70, 70, 70)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255,255,255)
BLOCK_COLOR = (255, 100, 100)
TEXT_COLOR = (255, 255, 255)
TEXT_COLOR2 = (105, 106, 106)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - 40
PADDLE_SPEED = 12

BALL_SIZE = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

vol_bg = 0.1
vol_sound = 0.2

paddle_texture = pygame.image.load('data/textures/pad.png')
block_texture = pygame.image.load('data/textures/block1.png')
game_over_texture = pygame.image.load('data/textures/gameover1.png')
win_texture = pygame.image.load('data/textures/win1.png')
bg_texture = pygame.image.load('data/textures/bg2.png')

# Музика и звучки
bg_music = pygame.mixer.music.load("data/music/bg.ogg")
collision_music = pygame.mixer.Sound("data/music/knock.ogg")
pygame.mixer.music.set_volume(vol_bg)
collision_music.set_volume(vol_sound)
pygame.mixer.music.play(-1)

score = 0
record = int(open("data/record.txt").read())



font = pygame.font.SysFont(None, 36)
win_font = pygame.font.SysFont(None, 125)

BLOCK_WIDTH = 120
BLOCK_HEIGHT = 70
blocks = []
for row in range(3):
    for col in range(5):
        block_x = col * (BLOCK_WIDTH + 90) + 60
        block_y = row * (BLOCK_HEIGHT + 20) + 40
        block_rect = pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append(block_rect)

# Игровой цикл
game_run = True
while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Стены
    if ball_x <= 0 or ball_x >= WIDTH - BALL_SIZE:
        ball_speed_x *= -1
    if ball_y <= 0:
        ball_speed_y *= -1
    if ball_y > HEIGHT:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_y = 5
        score -= 10

    # Физика
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
    if ball_rect.colliderect(paddle_rect):
        ball_speed_y *= -1

    # Блоки
    new_blocks = []
    for block in blocks:
        if ball_rect.colliderect(block):
            collision_music.play()
            ball_speed_y *= -1
            score += 10
        else:
            new_blocks.append(block)
    blocks = new_blocks

    # Отображение всего
    screen.blit(bg_texture, (0, 0))
    screen.blit(paddle_texture, (paddle_x, paddle_y))
    pygame.draw.ellipse(screen, BALL_COLOR, ball_rect)

    for block in blocks:
        screen.blit(block_texture, block)
    
        # Проверка на проигрыш
    if score < 0:
        screen.blit(game_over_texture, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)
        game_run = False

    if not blocks:
        screen.blit(win_texture, (0, 0))
        win_text = win_font.render(str(score), True, TEXT_COLOR2)
        if score > record:
            open("data/record.txt", "w").write(str(score))

        if score >= 100:
            screen.blit(win_text, (WIDTH // 2 - 10, 495))
        else:
            screen.blit(win_text, (WIDTH // 2, 495))
        
        pygame.display.flip()
        pygame.time.wait(3000)
        game_run = False

    score_text = font.render(f"Очки: {score}", True, TEXT_COLOR)
    record_text = font.render(f"Рекорд: {record}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    screen.blit(record_text, (900, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()