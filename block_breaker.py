import pygame
import random

# 初期化
pygame.init()
pygame.mixer.init()  # 音声モジュールの初期化
pygame.mixer.music.load("maou_bgm_healing15.mp3")  # BGMの読み込み
pygame.mixer.music.set_volume(0.5)  # 音量設定（0.0から1.0の範囲）
pygame.mixer.music.play(-1)  # BGMをループ再生
hit_sound = pygame.mixer.Sound("決定ボタンを押す34.mp3")  # 衝突音の読み込み
game_state = "PLAYING"  # 状態: "PLAYING", "GAMEOVER", "CLEAR"

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
PADDLE_WIDTH, PADDLE_HEIGHT = 800, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 30  # パドルの移動速度

# ボールの設定
BALL_SIZE = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [5, -5]  # [x方向, y方向]

# ブロックの設定
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20
blocks = []
special_blocks = []  # 特殊ブロックのリスト
for row in range(5):
    for col in range(WIDTH // BLOCK_WIDTH):
        block = pygame.Rect(col * BLOCK_WIDTH, row * BLOCK_HEIGHT + 50, BLOCK_WIDTH - 2, BLOCK_HEIGHT - 2)
        blocks.append(block)
        if random.random() < 0.2: # 20%の確率で特殊ブロックを追加
            special_blocks.append(block)

# ゲームループ
score = 0
font = pygame.font.Font(None, 36)  # フォント設定（サイズ36）
clock = pygame.time.Clock()
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and(game_state == "GAMEOVER" or game_state == "CLEAR"):
                # ゲームオーバーまたはクリア時にRキーでリスタート
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed = [5, -5]
                blocks = []
                for row in range(5):
                    for col in range(WIDTH // BLOCK_WIDTH):
                        block = pygame.Rect(col * BLOCK_WIDTH, row * BLOCK_HEIGHT + 50, BLOCK_WIDTH - 2, BLOCK_HEIGHT - 2)
                        blocks.append(block)
                score = 0
                game_state = "PLAYING"

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # ボールの移動
    if game_state == "PLAYING":
        ball.move_ip(ball_speed)
    
    # 壁との衝突
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= HEIGHT:
        # ゲームオーバー（ボールが下に落ちた）
        #ball.center = (WIDTH // 2, HEIGHT // 2)
        #ball_speed = [5, -5]
        game_state = "GAMEOVER"

    # パドルとの衝突
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # ブロックとの衝突
    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed[1] = -ball_speed[1]
            score += 10 #　ブロックを壊すたびにスコアを10増やす
            hit_sound.play()  # 衝突音を再生
            if block in special_blocks: # 特殊ブロックに当たった場合
                paddle.width  = max(50, paddle.width - 20)  # パドルを小さく（最小50）
            break
        if len(blocks) == 0:
            game_state = "CLEAR" # すべてのブロックを壊した

    if score > 0 and score %50 == 0: # スコアが50の倍数のとき、ボールの速度を上げる
        ball_speed[0] *= 1.005
        ball_speed[1] *= 1.005

    # Cボタンを押したらすべてのブロックを消失（テスト用）
    if keys[pygame.K_c]:
        blocks.clear()
        game_state = "CLEAR"

    # 描画
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    score_text = font.render(f"Score: {score}", True, WHITE)  # スコアを描画
    screen.blit(score_text, (10, 10)) # スコアの位置
    pygame.draw.ellipse(screen, RED, ball)
    for block in blocks:
        if block in special_blocks:
            pygame.draw.rect(screen, RED, block)
        else:
            pygame.draw.rect(screen, WHITE, block)
        if game_state == "GAMEOVER":
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        elif game_state == "CLEAR":
            clear_text = font.render("CLEAR!", True, WHITE)
            screen.blit(clear_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))


    # 画面更新
    pygame.display.flip()
    clock.tick(60)

# 終了
pygame.quit()