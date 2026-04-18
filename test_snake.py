import pytest
from snake_control import Snake

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

#Teste (Green) - Teste para crescimento da cobra (ainda não implementado)
def test_snake_growth():
    player = Snake(start_x=5, start_y=5)

    player.grow() # Método de crescimento ainda não implementado
    player.move('d', max_x=10, max_y=10) # Move para a direita após crescer

    assert len(player.body) == 3 # Espera que o corpo cresça para 3 segmentos
    assert player.body == [(6, 5), (5, 5), (4, 5)] # Espera que o novo segmento seja adicionado na posição do antigo rabo (4,5)

#Teste (Red) - Testa colisão da cobra consigo mesma (ainda não implementado)
def test_snake_no_collision_start():
    player = Snake(start_x=5, start_y=5)
    # Uma cobra nova nunca deve estar em colisão
    assert player.check_collision() == False