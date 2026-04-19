import pygame
from player import MusicPlayer

# 初始化
pygame.init()
screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("Music Player")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)

# 字体
font = pygame.font.Font(None, 32)

# 创建播放器
player = MusicPlayer()

running = True
while running:
    screen.fill(BLACK)

    # 显示当前歌曲
    song_name = player.get_song()
    screen.blit(font.render(f"Now Playing: {song_name}", True, WHITE), (30, 40))

    # 按键提示
    tips = "P=Play | S=Stop | N=Next | B=Back | Q=Quit"
    screen.blit(font.render(tips, True, GRAY), (30, 120))

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.back()
            elif event.key == pygame.K_q:
                running = False

    # 自动播放下一首
    if player.playing and not pygame.mixer.music.get_busy() and player.playlist:
        player.next()

    pygame.display.update()

pygame.quit()