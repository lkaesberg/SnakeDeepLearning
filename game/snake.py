class Snake:
    def __init__(self, x, y, direction = 0, length = 1):
        self.x = x
        self.y = y
        self.direction = direction # 0: up, 1: right, 2:down, 3: left
        self.length = length
        self.tail = []

    def forward(self):
        self.tail.append((x,y))
        while(len(self.tail) > self.length):
            self.tail.pop(0)
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x -= 1
        else:
            raise Exception("Invalid direction")

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction + 3) % 4

    def eat(self):
        self.length += 1
