import pygame

class PygameHandler:
    def __init__(self, x_size, y_size, block_size):
        self.x_size = x_size
        self.y_size = y_size
        self.block_size = block_size
        self.last_input = 'd'
        
        # Mapeamento de teclas do Pygame para o formato de entrada do jogo
        self.key_map = {
            pygame.K_w: 'w', pygame.K_UP: 'w',
            pygame.K_s: 's', pygame.K_DOWN: 's',
            pygame.K_a: 'a', pygame.K_LEFT: 'a',
            pygame.K_d: 'd', pygame.K_RIGHT: 'd',
            pygame.K_ESCAPE: 'end'
        }

        # O NOVO SISTEMA DE SPRITES
        self.sprites = {}
        nomes_sprites = [
            'head_up', 'head_down', 'head_left', 'head_right',
            'tail_up', 'tail_down', 'tail_left', 'tail_right',
            'body_vertical', 'body_horizontal',
            'body_topleft', 'body_topright', 'body_bottomleft', 'body_bottomright',
            'apple'
        ]
        
        # Carrega todos os sprites automaticamente usando um loop
        for nome in nomes_sprites:
            try:
                # O caminho deve bater com a pasta onde guardou as imagens do asset pack
                img = pygame.image.load(f'Graphics/{nome}.png') 
                self.sprites[nome] = pygame.transform.scale(img, (block_size, block_size))
            except FileNotFoundError:
                # Fallback de segurança para o Pytest
                self.sprites[nome] = pygame.Surface((block_size, block_size))

    def parse_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                self.last_input = self.key_map[event.key]

    def display(self, screen, snake_body, fruit_list):
        screen.fill((0, 0, 0)) 
        
        # Desenha as Frutas
        for f_x, f_y in fruit_list:
            coordenada = (f_x * self.block_size, f_y * self.block_size)
            screen.blit(self.sprites['apple'], coordenada)
            
        # Desenha a Cobra Dinamicamente!
        for index, (p_x, p_y) in enumerate(snake_body):
            coordenada = (p_x * self.block_size, p_y * self.block_size)
            nome_correto = get_sprite_name(snake_body, index, self.x_size, self.y_size)
            
            # Um pequeno fallback de segurança (se a função não souber o que é, desenha horizontal)
            if not nome_correto or nome_correto not in self.sprites:
                nome_correto = 'body_horizontal' 
                
            # Desenha a imagem selecionada
            screen.blit(self.sprites[nome_correto], coordenada)
                
        if not isinstance(screen, type(pygame.Surface((1,1)))): 
            pass
        else:
            pygame.display.flip()

def get_sprite_name(corpo, index, max_x, max_y):
    # Lógica da Cabeça
    if index == 0:
        head_x, head_y = corpo[0]
        neck_x, neck_y = corpo[1]

        # Compara usando a volta do mapa (módulo)
        if head_x == (neck_x + 1) % max_x: return "head_right"
        if head_x == (neck_x - 1) % max_x: return "head_left"
        if head_y == (neck_y + 1) % max_y: return "head_down"
        if head_y == (neck_y - 1) % max_y: return "head_up"

    # Lógica da Cauda
    elif index == len(corpo) - 1:
        tail_x, tail_y = corpo[index]
        front_x, front_y = corpo[index - 1]

        # A ponta da cauda aponta para o lado oposto ao bloco da frente
        if tail_x == (front_x - 1) % max_x: return "tail_left"
        if tail_x == (front_x + 1) % max_x: return "tail_right"
        if tail_y == (front_y - 1) % max_y: return "tail_up"
        if tail_y == (front_y + 1) % max_y: return "tail_down"

    # Lógica do Corpo e Curvas
    else:
        x, y = corpo[index]
        prev_x, prev_y = corpo[index - 1]
        next_x, next_y = corpo[index + 1]

        # Se o X de ambos os vizinhos for igual, é uma linha reta vertical
        if prev_x == next_x: return "body_vertical"
        
        # Se o Y de ambos os vizinhos for igual, é uma linha reta horizontal
        if prev_y == next_y: return "body_horizontal"

        # Vizinhança com cálculos de borda (wrap-around)
        vizinhos_x = (prev_x, next_x)
        vizinhos_y = (prev_y, next_y)

        is_left = ((x - 1) % max_x) in vizinhos_x
        is_right = ((x + 1) % max_x) in vizinhos_x
        is_up = ((y - 1) % max_y) in vizinhos_y
        is_down = ((y + 1) % max_y) in vizinhos_y

        if is_up and is_left: return "body_topleft"
        if is_up and is_right: return "body_topright"
        if is_down and is_left: return "body_bottomleft"
        if is_down and is_right: return "body_bottomright"