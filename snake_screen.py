import os
import keyboard
import time

from snake_control import Snake


class io_handler:
    
    x_size: int
    y_size: int
    game_speed = float
    last_input: str
    matrix = []

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
        
        self.game_speed = speed
        self.last_input = 'w'

        for i in range (self.y_size): 
            self.matrix.append([0]*self.x_size)

    def record_inputs(self):
        keyboard.add_hotkey('w', lambda: setattr(self, "last_input", 'w'))
        keyboard.add_hotkey('a', lambda: setattr(self, "last_input", 'a'))
        keyboard.add_hotkey('s', lambda: setattr(self, "last_input", 's'))
        keyboard.add_hotkey('d', lambda: setattr(self, "last_input", 'd'))
        keyboard.add_hotkey('esc', lambda: setattr(self, "last_input", 'end'))

    def display(self):
        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)

### exemplo do uso da classe io_handler  
#instance = io_handler((10,15), 0.5)
#instance.matrix[0][0] = 1 #corpo
#instance.matrix[0][1] = 2 #cabeça
#instance.matrix[0][2] = 3 #fruta

def process_turn(snake, display_handler, fruit_list):
    if display_handler.last_input == 'end':
        return True

    snake.move(display_handler.last_input, display_handler.x_size, display_handler.y_size)
    display_handler.matrix = [[0] * display_handler.x_size for _ in range(display_handler.y_size)]

    if snake.body[0] in fruit_list:
        snake.grow()
        fruit_list.remove(snake.body[0]) # Remove a fruta específica que foi comida

    for f_x, f_y in fruit_list:
        if f_x >= 0 and f_y >= 0: # Checagem de segurança
            display_handler.matrix[f_y][f_x] = 3 # Marca as frutas na matriz

    for index, part in enumerate(snake.body):
        p_x, p_y = part
        if index == 0:
            display_handler.matrix[p_y][p_x] = 2 # Cabeça
        else:
            display_handler.matrix[p_y][p_x] = 1 # Corpo

    if snake.check_collision():
        return True
    return False

def game_loop():
    instance = io_handler((10,10), 0.5)
    instance.record_inputs()

    player = Snake(start_x=5, start_y=5)
    while True:
        
        game_over = process_turn(player, instance)
        if game_over:
            print("Você perdeu!")
            break
        instance.display()
        time.sleep(instance.game_speed)