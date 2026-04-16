class Snake:
    def __init__(self, start_x, start_y):
        self.body = [(start_x, start_y), (start_x, start_y - 1)]
        self.direction = 'd'