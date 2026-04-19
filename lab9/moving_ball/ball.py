class Ball:
    def __init__(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height // 2
        
        self.radius = 25
        self.speed = 20 
        
        self.max_w = screen_width
        self.max_h = screen_height

    def move_up(self):
        if self.y - self.speed >= self.radius:
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed <= self.max_h - self.radius:
            self.y += self.speed

    def move_left(self):
        if self.x - self.speed >= self.radius:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed <= self.max_w - self.radius:
            self.x += self.speed