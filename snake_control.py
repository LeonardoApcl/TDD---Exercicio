class Snake:
    def __init__(self, start_x, start_y):
        self.body = [(start_x, start_y), (start_x - 1, start_y)]
        self.direction = 'd'
        self.grow_pending = False

        self.directions = {
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0)
        }

        self.opposites = {
            'w': 's',
            's': 'w',
            'a': 'd',
            'd': 'a'
        }

    def move(self, user_input, max_x, max_y):

        if user_input in self.directions and user_input != self.opposites.get(self.direction):
            self.direction = user_input

        head_x, head_y = self.body[0]
        d_x, d_y = self.directions[self.direction]
        new_head = ((head_x + d_x) % max_x, (head_y + d_y) % max_y)
        self.body.insert(0, new_head)

        #corta o rabo da cobra, a menos que ela tenha acabado de comer (crescer)
        if self.grow_pending:
            self.grow_pending = False # Reseta a flag, a cobra acabou de crescer
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]
    
    def get_allowed_fruits(self):
        size = len(self.body)

        if size < 10:
            return 1
        elif size < 20:
            return 2
        else:
            return 3