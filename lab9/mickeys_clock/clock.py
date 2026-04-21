import pygame
from datetime import datetime

class MickeyClock:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mickey's Clock")

        self.clock_bg = pygame.image.load("images/clock.png").convert()
        self.clock_bg = pygame.transform.scale(self.clock_bg, (self.width, self.height))

        self.hand_img = pygame.image.load("images/mickey_hand.png").convert_alpha()
        self.hand_img = pygame.transform.scale(self.hand_img, (100, 300))

        self.center = (self.width // 2, self.height // 2)
        self.clock = pygame.time.Clock()

    def get_time_angles(self):
        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = minutes * 6   
        second_angle = seconds * 6   
        return minute_angle, second_angle

    def rotate_hand(self, surface, angle, flip=False):
        
        if flip:
            surface = pygame.transform.flip(surface, True, False)
        
        rotated = pygame.transform.rotate(surface, -angle)
        rect = rotated.get_rect(center=self.center)
        return rotated, rect

    def draw(self):
        self.screen.blit(self.clock_bg, (0, 0))

        minute_angle, second_angle = self.get_time_angles()

        min_hand, min_rect = self.rotate_hand(self.hand_img.copy(), minute_angle, flip=False)

        sec_hand, sec_rect = self.rotate_hand(self.hand_img.copy(), second_angle, flip=True)

        self.screen.blit(min_hand, min_rect)
        self.screen.blit(sec_hand, sec_rect)

        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 12)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
            self.clock.tick(1) 

        pygame.quit()