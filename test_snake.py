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

#Teste (Red)
def test_snake_move_down():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('s', max_x=10, max_y=10) 
    
    # Assert
    assert player.body[0] == (5, 6)      # A cabeça deve ir para baixo (y+1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 5)     # O corpo antigo (4,5) sumiu, o novo é (5,5)

#Teste (Red)
def test_snake_move_left():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)]
    
    # Act
    player.move('a', max_x=10, max_y=10) 
    
    # Assert
    assert player.body[0] == (4, 5)      # A cabeça deve ir para a esquerda (x-1)
    assert len(player.body) == 2         # O tamanho deve continuar o mesmo
    assert player.body[-1] == (5, 5)     # O corpo antigo (4,5) sumiu, o novo é (5,5)