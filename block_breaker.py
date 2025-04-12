import pygame
import random

# 初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# パドルの設定
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 5

# ボールの設定
BALL_SIZE = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [5, -5]  # [x方向, y方向]

# ブロックの設定
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20
blocks = []
for row in range(5):
    for col in range(WIDTH // BLOCK_WIDTH):
        block = pygame.Rect(col * BLOCK_WIDTH, row * BLOCK_HEIGHT + 50, BLOCK_WIDTH - 2, BLOCK_HEIGHT - 2)
        blocks.append(block)

# ゲームループ
clock = pygame.time.Clock()
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # ボールの移動
    ball.move_ip(ball_speed)

    # 壁との衝突
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= HEIGHT:
        # ゲームオーバー（ボールが下に落ちた）
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed = [5, -5]

    # パドルとの衝突
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # ブロックとの衝突
    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed[1] = -ball_speed[1]
            break

    # 描画
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for block in blocks:
        pygame.draw.rect(screen, WHITE, block)

    # 画面更新
    pygame.display.flip()
    clock.tick(60)

# 終了
pygame.quit()