class Ball:
    def __init__(self, screen_width, screen_height):
        # 小球初始位置（屏幕中心）
        self.x = screen_width // 2
        self.y = screen_height // 2
        
        # 大小：半径25 → 50x50
        self.radius = 25
        self.speed = 20  # 每次移动20像素
        
        # 屏幕边界
        self.max_w = screen_width
        self.max_h = screen_height

    def move_up(self):
        # 不让小球出界
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