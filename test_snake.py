import pytest
from snake_control import Snake
from snake_screen import io_handler, process_turn, manage_fruits

#Teste (Green)
def test_snake_initialization():
    # Arrange & Act
    player = Snake(start_x=5, start_y=5)
    
    # Assert
    assert len(player.body) == 2
    assert player.direction == 'd'

#Teste (Green)
def test_snake_move_right():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('d', max_x=10, max_y=10) 
    
    # Assert
    assert player.body[0] == (6, 5)      # A cabeça deve ir para a direita (x+1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 5)     # O corpo antigo (4,5) sumiu, o novo é (5,5)

#Teste (Green)
def test_snake_move_up():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('w', max_x=10, max_y=10) 
    
    # Assert
    assert player.body[0] == (5, 4)      # A cabeça deve ir para cima (y-1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 5)     # O corpo antigo (4,5) sumiu, o novo é (5,5)

#Teste (Green)
def test_snake_move_down():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('s', max_x=10, max_y=10) 
    
    # Assert
    assert player.body[0] == (5, 6)      # A cabeça deve ir para baixo (y+1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 5)     # O corpo antigo (4,5) sumiu, o novo é (5,5)

#Teste (Green) refatorado para impedir ré (inversão de direção)
def test_snake_move_left():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('w', max_x=10, max_y=10) # Primeiro move para cima (válido)
    player.move('a', max_x=10, max_y=10) # Depois tenta mandar para a esquerda (sem ré)
    
    # Assert
    assert player.body[0] == (4, 4)      # A cabeça deve ir para cima (y-1) e para a esquerda (x-1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 4)     # O corpo antigo (4,5) sumiu, o novo é (5,4)

#Teste (Green)
def test_snake_ignore_opposite_direction():
    player = Snake(start_x=5, start_y=5) # Começa virada para direita ('d')
    
    player.move('a', max_y=10, max_x=10) # Tenta mandar para a esquerda (ré)
    
    assert player.direction == 'd'       # Deve ignorar e continuar para direita
    assert player.body[0] == (6, 5)      # Deve ter andado para a direita normalmente

#Teste (Green) - Testa comportamento de movimento para fora dos limites do mapa
def test_snake_move_out_of_bounds():
    player = Snake(start_x=9, start_y=5) # Começa perto da borda direita do mapa
    
    player.move('d', max_x=10, max_y=10) # Tenta mandar para direita (na parede)
    
    assert player.body[0] == (0, 5)      # A cabeça deve reaparecer na borda esquerda (x=0)
    assert len(player.body) == 2         # O tamanho continua sendo 2
    assert player.body[-1] == (9, 5)     # A antiga cabeça (9,5) agora é o corpo

#Teste (Green) - Testa comportamento de movimento para fora dos limites do mapa na vertical
def test_snake_move_out_of_bounds_vertical():
    player = Snake(start_x=5, start_y=0) # Começa perto da borda superior do mapa

    player.move('w', max_x=10, max_y=10) # Tenta mandar para cima (na parede)

    assert player.body[0] == (5, 9)      # A cabeça deve reaparecer na borda inferior (y=9)
    assert len(player.body) == 2         # O tamanho continua sendo 2
    assert player.body[-1] == (5, 0)     # A antiga cabeça (5,0) agora é o corpo

#Teste (Green) - Testa comportamento de movimento com input inválido
def test_snake_input_validation():
    player = Snake(start_x=5, start_y=5)

    player.move('f', max_x=10, max_y=10) # Tenta mandar um input inválido

    assert player.direction == 'd' # Deve ignorar o input inválido e continuar na direção atual
    assert player.body[0] == (6, 5) # Deve ter andado para a direita normalmente

#Teste (Green) - Teste para crescimento da cobra
def test_snake_growth():
    player = Snake(start_x=5, start_y=5)

    player.grow() # Método de crescimento ainda não implementado
    player.move('d', max_x=10, max_y=10) # Move para a direita após crescer

    assert len(player.body) == 3 # Espera que o corpo cresça para 3 segmentos
    assert player.body == [(6, 5), (5, 5), (4, 5)] # Espera que o novo segmento seja adicionado na posição do antigo rabo (4,5)

#Teste (Green) - Testa colisão da cobra consigo mesma
def test_snake_no_collision_start():
    player = Snake(start_x=5, start_y=5)
    # Uma cobra nova nunca deve estar em colisão
    assert player.check_collision() == False

#Teste (Green) - Testa colisão da cobra consigo mesma
def test_snake_self_collision():
    player = Snake(start_x=5, start_y=5)
    # Simulamos uma cobra grande enrolada em si mesma 
    # (a cabeça (5,5) está ocupando o mesmo espaço que a ponta do rabo)
    player.body = [(5, 5), (5, 6), (6, 6), (6, 5), (5, 5)] 
    
    assert player.check_collision() == True

#Teste (Green) - Testa a regra de frutas permitidas com base no tamanho da cobra
def test_allowed_fruits_rule():
    player = Snake(start_x=5, start_y=5)
    
    # Cobra iniciante (tamanho 2) -> 1 fruta
    assert player.get_allowed_fruits() == 1
    
    # Simulamos uma cobra com tamanho exato de 10 -> 2 frutas
    player.body = [(0,0)] * 10
    assert player.get_allowed_fruits() == 2
    
    # Simulamos uma cobra com tamanho de 25 -> 3 frutas
    player.body = [(0,0)] * 25
    assert player.get_allowed_fruits() == 3

###########  Testes para o loop geral de gameplay e integração da tela com a lógica da cobra ###########

#Teste (Green) - não há implementação do process_turn, apenas um placeholder que retorna True
def test_process_turn_updates_matrix():
    #arrange

    player = Snake(start_x=5, start_y=5)
    instance = io_handler((10, 10), 0.5)
    instance.last_input = 'd' # Simula o usuário apertando 'd'

    game_over = process_turn(player, instance, fruit_list=[(0, 0)])

    assert game_over == False
    assert player.body[0] == (6, 5) # A cabeça andou pra direita
    assert instance.matrix[5][6] == 2   # A matriz da tela recebeu a cabeça (2) na nova posição
    assert instance.matrix[5][5] == 1   # A matriz da tela recebeu o corpo (1)
    assert instance.matrix[0][0] == 3   # A matriz da tela recebeu a fruta (3) na posição correta

#Teste (Green))
def test_process_turn_erases_old_tail():
    # Arrange
    player = Snake(start_x=5, start_y=5) 
    instance = io_handler((10, 10), 0.5)
    
    
    # Isso simula o rastro do frame anterior, onde a cabeça estava em (5,5) e o corpo em (5,4)
    instance.matrix[5][4] = 1 
    
    process_turn(player, instance, fruit_list=[(0, 0)])
    
    # Assert
    assert instance.matrix[4][5] == 2 # A Cabeça deve estar na nova posição (4,5), o input padrão do io_handler é 'w' ao invés do 'd' usado no snake_control
    assert instance.matrix[5][5] == 1 # A Cabeça antiga (5,5) agora é o corpo
    assert instance.matrix[5][4] == 0 # O rastro antigo (5,4) deve ser limpo (0)

#Teste(Green)
def test_process_turn_game_over_on_self_collision():
    player = Snake(start_x=5, start_y=5)
    instance = io_handler((10, 10), 0.5)
    
    # Simulamos uma cobra grande enrolada em si mesma 
    player.body = [(5, 5), (5, 6), (6, 6), (6, 5), (6,4)] 
    instance.last_input = 's' # Tenta mover para baixo, o que causaria colisão com o corpo

    game_over = process_turn(player, instance,  fruit_list=[(0, 0)])

    assert game_over == True

#Teste (Green)
def test_process_turn_game_over_on_input():
    player = Snake(start_x=5, start_y=5)
    instance = io_handler((10, 10), 0.5)
    
    instance.last_input = 'end' # input de saída do jogo, que deve causar game over imediato

    game_over = process_turn(player, instance, fruit_list=[(0, 0)])

    assert game_over == True

#Teste (Green)
def test_process_turn_growth():
    player = Snake(start_x=5, start_y=5)
    instance = io_handler((10, 10), 0.5)
    
    instance.last_input = 'd' # Move para a direita

    game_over = process_turn(player, instance, fruit_list=[(6, 5)]) # A fruta está na posição para onde a cabeça vai se mover

    assert player.grow_pending == True # A cobra deve ter a flag de crescimento ativada

#Teste (Green)
def test_manage_fruits_respects_allowed_rule():
    # Arrange
    player = Snake(start_x=5, start_y=5) 
    
    # Simulamos que a cobra cresceu até o tamanho 10 (A regra diz que agora ela tem direito a 2 frutas)
    player.body = [(x, 0) for x in range(10)] 
    assert player.get_allowed_fruits() == 2 # Só pra garantir que a regra matemática funciona
    
    # A lista de frutas atual só tem 1 fruta, mas a regra permite 2.
    fruit_list = [(1, 1)]
    
    # Act
    manage_fruits(player, fruit_list, max_x=10, max_y=10)
    
    # Assert
    # A função deve ter gerado e adicionado +1 fruta nova na lista
    assert len(fruit_list) == 2

#Teste (Green)
def test_manage_fruits_does_not_make_fruits_when_position_is_invalid():
    player = Snake(start_x=0, start_y=0) 
    player.body = [(0,0),(0,1),(1,1)] 
    
    fruit_list = []
    
    # Act
    manage_fruits(player, fruit_list, max_x=2, max_y=2)
    
    # Assert
    # Só pode adicionar a fruta em uma única posição válida
    assert len(fruit_list) == 1
    assert fruit_list[0] == (1, 0) # A única posição válida para a fruta é (1,0) porque as outras estão ocupadas pelo corpo da cobra

# Teste (Green)
def test_manage_fruits_does_not_add_duplicate_fruits():
    player = Snake(start_x=0, start_y=0) 
    player.body = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), 
    (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)
    ] 
    
    fruit_list = []
    
    # Act
    manage_fruits(player, fruit_list, max_x=11, max_y=1)
    
    # Assert
    # A função deve tentar adicionar uma fruta nova, mas como a única posição válida já tem uma fruta, ela não deve adicionar nada
    assert len(fruit_list) == 1
    assert fruit_list[0] == (10, 0) # A fruta existente deve permanecer inalterada

# ------ Testes Com o Pygame ------
import pygame
from unittest.mock import Mock

@pytest.mark.parametrize("pygame_key, expected_direction", [
    (pygame.K_UP, 'w'),
    (pygame.K_w, 'w'),
    (pygame.K_DOWN, 's'),
    (pygame.K_s, 's'),
    (pygame.K_LEFT, 'a'),
    (pygame.K_a, 'a'),
    (pygame.K_RIGHT, 'd'),
    (pygame.K_d, 'd'),
    (pygame.K_ESCAPE, 'end')
])
def test_pygame_input_translation(pygame_key, expected_direction):
    # Arrange
    mock_event = Mock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame_key # Usa a chave injetada pelo Pytest
    
    from snake_pygame import PygameHandler
    tela_pygame = PygameHandler(x_size=10, y_size=10, block_size=20)
    
    # Act
    tela_pygame.parse_event(mock_event)
    
    # Assert
    assert tela_pygame.last_input == expected_direction # Verifica se a saída bate