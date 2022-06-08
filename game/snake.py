class Snake:
    def __init__(self, x, y, direction = 0):
        self.x = x
        self.y = y
        self.direction = direction # 0: up, 1: right, 2:down, 3: left
        self.tail = []

    def forward(self):
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x -= 1
        else:
            throw Exception("Invalid direction")

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction + 3) % 4
