import random
import pygame
from snake_screen import PygameHandler

from snake_model import Snake

def process_turn(snake, fruit_list, max_x, max_y, last_input):
    # Checa se o jogador pediu para sair
    if last_input == 'end':
        return True

    # Move a cobra
    snake.move(last_input, max_x, max_y)

    # Lógica de comer a fruta
    if snake.body[0] in fruit_list:
        snake.grow()
        fruit_list.remove(snake.body[0])

    # Checa colisão (Game Over)
    if snake.check_collision():
        return True
        
    return False # O jogo continua

def manage_fruits(snake, fruit_list, max_x, max_y):
    limit_T = snake.get_allowed_fruits() - len(fruit_list)

    total_spaces = max_x * max_y
    occupied_spaces = len(snake.body) + len(fruit_list)
    free_spaces = total_spaces - occupied_spaces

    limit = min(limit_T, free_spaces)
    
    # Enquanto faltar fruta na tela, gera novas!
    while limit > 0:
        new_fruit = (random.randint(0, max_x - 1), random.randint(0, max_y - 1))
        if new_fruit not in snake.body and new_fruit not in fruit_list:
            fruit_list.append(new_fruit)
            limit -= 1

def game_loop():
    pygame.init()
    
    tamanho_bloco = 20
    largura, altura = 10, 15
    screen = pygame.display.set_mode((largura * tamanho_bloco, altura * tamanho_bloco))
    
    player = Snake(start_x=5, start_y=5)
    tela_handler = PygameHandler(largura, altura, tamanho_bloco)
    frutas_na_tela = []
    
    clock = pygame.time.Clock()

    while True:
        # Pega inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            tela_handler.parse_event(event)
            
        # Roda as regras do jogo (sem passar a tela!)
        manage_fruits(player, frutas_na_tela, largura, altura)
        game_over = process_turn(player, frutas_na_tela, largura, altura, tela_handler.last_input)
        
        if game_over:
            print("GAME OVER")
            break
            
        # Manda a tela desenhar o estado atual
        tela_handler.display(screen, player.body, frutas_na_tela)
        
        clock.tick(5)