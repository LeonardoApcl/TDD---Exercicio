import pytest
from snake_control import Snake

#Teste (Red)
def test_snake_initialization():
    # Arrange & Act
    player = Snake(start_x=5, start_y=5)
    
    # Assert
    assert len(player.body) == 2
    assert player.direction == 'd'