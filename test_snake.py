import pytest
from snake_model import Snake
from snake_control import process_turn, manage_fruits
import pygame
from snake_screen import PygameHandler
from unittest.mock import Mock, MagicMock, patch

def test_snake_initialization():
    # Arrange & Act
    player = Snake(start_x=5, start_y=5)
    
    # Assert
    assert len(player.body) == 2
    assert player.direction == 'd'

@pytest.mark.parametrize("lista_movimentos, cabeca_esperada", [
    (['d'], (6, 5)),         # Movimento simples para a direita
    (['w'], (5, 4)),         # Movimento simples para cima
    (['s'], (5, 6)),         # Movimento simples para baixo
    (['w', 'a'], (4, 4)),    # Sequência: vai para cima, depois esquerda (evita a ré)
    (['s', 'a'], (4, 6)),    # Sequência: vai para baixo, depois esquerda
])
def test_snake_valid_movements(lista_movimentos, cabeca_esperada):
    # Arrange
    player = Snake(start_x=5, start_y=5) # Corpo inicial: [(5,5), (5,4)], direção 'd'
    
    # Act
    for movimento in lista_movimentos:
        player.move(movimento, max_x=10, max_y=10)
        
    # Assert
    assert player.body[0] == cabeca_esperada
    assert len(player.body) == 2 # Garante que a cobra andou, mas não cresceu

@pytest.mark.parametrize("input_invalido", [
    'a',   # Direção oposta direta (ré)
    'f',   # Tecla aleatória não mapeada
    'x',   # Outra letra qualquer
    '1',   # Número
    ' ',   # Espaço em branco
    'end'  # Palavra inteira
])
def test_snake_ignore_invalid_inputs(input_invalido):
    # Arrange
    player = Snake(start_x=5, start_y=5) # Inicia virada para 'd'
    
    # Act
    player.move(input_invalido, max_x=10, max_y=10)
    
    # Assert
    assert player.direction == 'd'   # A direção interna não pode ter sido alterada
    assert player.body[0] == (6, 5)  # A cobra deve ter dado um passo para a direita mesmo assim

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

    player.grow() # Método de crescimento
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

#---------------------------- Testes para o loop geral de gameplay ----------------------------

def test_process_turn_moves_snake():
    # Arrange
    player = Snake(start_x=5, start_y=5) # Inicia em (5,5) olhando para 'd'
    fruit_list = [(0, 0)]
    
    # Act: Passamos o input 'd' (direita)
    game_over = process_turn(player, fruit_list, max_x=10, max_y=10, last_input='d')

    # Assert
    assert game_over is False
    assert player.body[0] == (6, 5) # A cabeça andou pra direita
    assert len(player.body) == 2    # O tamanho não 
    
def test_process_turn_game_over_on_input():
    # Arrange
    player = Snake(start_x=5, start_y=5)
    fruit_list = [(0, 0)]
    
    # Act: Simulamos o botão de sair ('end')
    game_over = process_turn(player, fruit_list, max_x=10, max_y=10, last_input='end')

    # Assert
    assert game_over is True

def test_process_turn_game_over_on_self_collision():
    # Arrange
    player = Snake(start_x=5, start_y=5)
    # Cobra longa enrolada. Ao mover para baixo ('s'), a cabeça (5,5) baterá no corpo (5,6)
    player.body = [(5, 5), (5, 6), (6, 6), (6, 5), (6,4)] 
    fruit_list = [(0, 0)]

    # Act
    game_over = process_turn(player, fruit_list, max_x=10, max_y=10, last_input='s')

    # Assert
    assert game_over is True

def test_process_turn_eats_fruit_and_grows():
    # Arrange
    player = Snake(start_x=5, start_y=5)
    # A fruta está na posição para onde a cabeça vai se mover
    fruit_list = [(6, 5)] 
    
    # Act: Move a cobra para cima da fruta
    game_over = process_turn(player, fruit_list, max_x=10, max_y=10, last_input='d')

    # Assert
    assert game_over is False
    assert player.grow_pending is True # A cobra deve estar pronta para crescer
    assert len(fruit_list) == 0        # A fruta deve sumir da lista do jogo

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

#------------------------------ Testes Com o Pygame ------------------------------

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
    
    from snake_screen import PygameHandler
    tela_pygame = PygameHandler(x_size=10, y_size=10, block_size=20)
    
    # Act
    tela_pygame.parse_event(mock_event)
    
    # Assert
    assert tela_pygame.last_input == expected_direction # Verifica se a saída bate

def test_pygame_display_draws_sprites_with_blit():
    # Arrange
    tamanho_bloco = 20
    handler = PygameHandler(x_size=2, y_size=2, block_size=tamanho_bloco)
    
    # Cria uma tela falsa (Mock)
    tela_falsa = MagicMock() 
    
    # Nova estrutura de dados no lugar da matriz:
    # A cabeça (0,0) é sempre o índice 0. O corpo (0,1) vem a seguir.
    corpo_cobra = [(0, 0), (0, 1)] 
    
    # Fruta na coordenada (1,1)
    lista_frutas = [(1, 1)]
    
    # Act
    handler.display(tela_falsa, corpo_cobra, lista_frutas)
    
    # Assert
    # Verifica se a tela é limpa no começo
    tela_falsa.fill.assert_called_once()
    
    # Verifica se o método 'blit' (desenhar imagem) foi chamado 3 vezes!
    assert tela_falsa.blit.call_count == 3
    
    # Pega todos os argumentos que foram passados nas chamadas do blit
    chamadas_blit = tela_falsa.blit.call_args_list
    
    # Extrai apenas as coordenadas (x,y) de cada chamada para verificar
    coordenadas_usadas = [chamada[0][1] for chamada in chamadas_blit]
    
    # Verifica se os elementos foram desenhados nos locais corretos (multiplicados por block_size)
    assert (0, 0) in coordenadas_usadas   # Posição da Cabeça: x=0*20, y=0*20
    assert (0, 20) in coordenadas_usadas  # Posição do Corpo: x=0*20, y=1*20
    assert (20, 20) in coordenadas_usadas # Posição da Fruta: x=1*20, y=1*

# Testes para usar as sprites corretas de acordo com a direção
from snake_screen import get_sprite_name 

@pytest.mark.parametrize("corpo, sprite_esperado", [
    ([(5, 4), (5, 5)], "head_up"),    # Cabeça em y=4, pescoço em y=5 (Subindo)
    ([(5, 6), (5, 5)], "head_down"),  # Cabeça em y=6, pescoço em y=5 (Descendo)
    ([(6, 5), (5, 5)], "head_right"), # Cabeça em x=6, pescoço em x=5 (Indo para a direita)
    ([(4, 5), (5, 5)], "head_left"),  # Cabeça em x=4, pescoço em x=5 (Indo para a esquerda)
])
def test_sprite_cabeca(corpo, sprite_esperado):
    # Act
    # Pede o sprite para o index 0 (Cabeça)
    resultado = get_sprite_name(corpo, index=0)
    
    # Assert
    assert resultado == sprite_esperado

@pytest.mark.parametrize("corpo, index_alvo, sprite_esperado", [
    # --- Linhas Retas ---
    ([(5, 3), (5, 4), (5, 5)], 1, "body_vertical"),   # X é todo igual, variação no Y
    ([(4, 5), (5, 5), (6, 5)], 1, "body_horizontal"), # Y é todo igual, variação no X
    
    # --- Curvas (O vértice está sempre no index 1) ---
    # Esquerda <-> Cima
    ([(4, 5), (5, 5), (5, 4)], 1, "body_topleft"), 
    
    # Direita <-> Cima
    ([(6, 5), (5, 5), (5, 4)], 1, "body_topright"),
    
    # Esquerda <-> Baixo
    ([(4, 5), (5, 5), (5, 6)], 1, "body_bottomleft"),
    
    # Direita <-> Baixo
    ([(6, 5), (5, 5), (5, 6)], 1, "body_bottomright"),
])
def test_sprite_corpo_curvas(corpo, index_alvo, sprite_esperado):
    # Act
    resultado = get_sprite_name(corpo, index=index_alvo)
    
    # Assert
    assert resultado == sprite_esperado

@pytest.mark.parametrize("corpo, sprite_esperado", [
    ([(5, 2), (5, 3), (5, 4)], "tail_down"),  # Cauda em y=4, corpo da frente em y=3 (Ponta virada para baixo)
    ([(5, 6), (5, 5), (5, 4)], "tail_up"),    # Cauda em y=4, corpo da frente em y=5 (Ponta virada para cima)
    ([(3, 5), (4, 5), (5, 5)], "tail_right"), # Cauda em x=5, corpo da frente em x=4 (Ponta virada para a direita)
    ([(7, 5), (6, 5), (5, 5)], "tail_left"),  # Cauda em x=5, corpo da frente em x=6 (Ponta virada para a esquerda)
])
def test_sprite_cauda(corpo, sprite_esperado):
    # Act
    ultimo_index = len(corpo) - 1
    resultado = get_sprite_name(corpo, index=ultimo_index)
    
    # Assert
    assert resultado == sprite_esperado

def test_pygame_handler_loads_all_sprites():
    handler = PygameHandler(x_size=10, y_size=10, block_size=20)
    
    # Assert
    esperados = [
        'head_up', 'head_down', 'head_left', 'head_right',
        'tail_up', 'tail_down', 'tail_left', 'tail_right',
        'body_vertical', 'body_horizontal',
        'body_topleft', 'body_topright', 'body_bottomleft', 'body_bottomright',
        'apple'
    ]
    
    for nome in esperados:
        assert nome in handler.sprites # O dicionário deve conter todas estas chaves!

@pytest.mark.parametrize("corpo_cobra, sprites_esperados", [
    # Cenário 1: Cobra Reta Horizontal (indo para a direita)
    (
        [(5, 5), (4, 5), (3, 5)], 
        [('head_right', 100, 100), ('body_horizontal', 80, 100), ('tail_left', 60, 100)]
    ),
    # Cenário 2: Cobra Reta Vertical (indo para baixo)
    (
        [(5, 5), (5, 4), (5, 3)], 
        [('head_down', 100, 100), ('body_vertical', 100, 80), ('tail_up', 100, 60)] 
    ),
    # Cenário 3: Cobra fazendo uma Curva (Tamanho 3)
    (
        [(5, 4), (5, 5), (6, 5)], 
        [('head_up', 100, 80), ('body_topright', 100, 100), ('tail_right', 120, 100)] 
    )
])
def test_pygame_display_uses_dynamic_sprites(corpo_cobra, sprites_esperados):
    # Arrange
    handler = PygameHandler(x_size=10, y_size=10, block_size=20)
    
    # Usa o mock do dicionário de sprites para saber se o display chamou a chave certa
    for key in handler.sprites.keys():
        handler.sprites[key] = MagicMock(name=key)
        
    tela_falsa = MagicMock()
    lista_frutas = [(1, 1)] # Fruta fixa em x=20, y=20
    
    # Act
    handler.display(tela_falsa, corpo_cobra, lista_frutas)
    
    # Assert
    # Verifica se a maçã foi desenhada
    tela_falsa.blit.assert_any_call(handler.sprites['apple'], (20, 20))
    
    # Verifica dinamicamente se a cobra foi desenhada com os sprites e posições exatas
    for nome_sprite, pos_x, pos_y in sprites_esperados:
        tela_falsa.blit.assert_any_call(handler.sprites[nome_sprite], (pos_x, pos_y))

# Espiona as funções do Pygame para não ter que carregar imagens reais do disco no teste
@patch('pygame.transform.scale')
@patch('pygame.image.load')
def test_pygame_handler_loads_images_into_dictionary(mock_load, mock_scale):
    # Arrange
    from snake_screen import PygameHandler # Ajuste o import
    
    # Configur os espiões para devolverem algo sempre que forem chamados
    mock_load.return_value = pygame.Surface((10, 10)) 
    mock_scale.return_value = "Imagem_Escalonada_Mock" 
    
    # Act
    handler = PygameHandler(x_size=10, y_size=10, block_size=20)
    
    # Assert
    # Verifica se a função de carregar imagem foi chamada exatamente 15 vezes!
    assert mock_load.call_count == 15
    
    # Garante que TODOS os valores no dicionário foram preenchidos (Nenhum é None)
    assert None not in handler.sprites.values()
    
    # Garante que os valores receberam a imagem processada
    assert handler.sprites['head_up'] == "Imagem_Escalonada_Mock"
    assert handler.sprites['apple'] == "Imagem_Escalonada_Mock"

@pytest.mark.parametrize("corpo, index, sprite_esperado", [
    # --- Atravessando as bordas (Mapa 10x10) ---
    
    # 1. Cabeça cruzando da direita (x=9) para a esquerda (x=0)
    ([(0, 5), (9, 5)], 0, "head_right"), 
    
    # 2. Cauda sendo puxada da esquerda (x=0) para a direita (x=9)
    ([(0, 5), (9, 5)], 1, "tail_left"),  
    
    # 3. Corpo fazendo uma curva EXATAMENTE na borda (Cabeça em 0,5 | Curva em 9,5 | Cauda em 9,4)
    # A cobra vinha descendo pela direita e virou para atravessar a parede!
    ([(0, 5), (9, 5), (9, 4)], 1, "body_topleft"), 
])
def test_sprite_wall_wrapping(corpo, index, sprite_esperado):
    # Act: dimensões de um mapa 10x10
    resultado = get_sprite_name(corpo, index, max_x=10, max_y=10)
    
    # Assert
    assert resultado == sprite_esperado