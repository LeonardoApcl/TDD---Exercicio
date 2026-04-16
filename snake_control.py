class Snake:
    def __init__(self, start_x, start_y):
        self.body = [(start_x, start_y), (start_x, start_y - 1)]
        self.direction = 'd'

        self.directions = {
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0)
        }

    def move(self, user_input, max_x, max_y):
        self.direction = user_input

        head_x, head_y = self.body[0]
        d_x, d_y = self.directions[self.direction]
        new_head = (head_x + d_x, head_y + d_y)
        self.body.insert(0, new_head)
        self.body.pop()