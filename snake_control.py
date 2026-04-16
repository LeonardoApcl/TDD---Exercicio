class Snake:
    def __init__(self, start_x, start_y):
        self.body = [(start_x, start_y), (start_x, start_y - 1)]
        self.direction = 'd'

    def move(self, user_input, max_x, max_y):
        if user_input == 'd':
            new_head = (self.body[0][0] + 1, self.body[0][1])
            self.body.insert(0, new_head)
            self.body.pop()
        if user_input == 'w':
            new_head = (self.body[0][0], self.body[0][1] - 1)
            self.body.insert(0, new_head)
            self.body.pop()
        if user_input == 's':
            new_head = (self.body[0][0], self.body[0][1] + 1)
            self.body.insert(0, new_head)
            self.body.pop()
        if user_input == 'a':
            new_head = (self.body[0][0] - 1, self.body[0][1])
            self.body.insert(0, new_head)
            self.body.pop()