import pygame
from player import MusicPlayer

# initialize
pygame.init()
screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("Music Player")

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)

# font
font = pygame.font.Font(None, 32)

# Music player object
player = MusicPlayer()

running = True
while running:
    screen.fill(BLACK)

    # Show current song
    song_name = player.get_song()
    screen.blit(font.render(f"Now Playing: {song_name}", True, WHITE), (30, 40))

    # Controls text
    tips = "P=Play | S=Stop | N=Next | B=Back | Q=Quit"
    screen.blit(font.render(tips, True, GRAY), (30, 120))

    # Keyboard control system
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

    # Auto-next song system
    if player.playing and not pygame.mixer.music.get_busy() and player.playlist:
        player.next()

    pygame.display.update()

pygame.quit()