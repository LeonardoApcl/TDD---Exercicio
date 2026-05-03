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

        self.sprites = {
            'head_up': None, 'head_down': None, 'head_left': None, 'head_right': None,
            'tail_up': None, 'tail_down': None, 'tail_left': None, 'tail_right': None,
            'body_vertical': None, 'body_horizontal': None,
            'body_topleft': None, 'body_topright': None, 'body_bottomleft': None, 'body_bottomright': None,
            'apple': None
        }

        # Coloquei um try/except para evitar que o Pytest quebre se não achar a imagem na pasta dele.
        try:
            self.img_head = pygame.image.load('Graphics/head_right.png')
            self.img_body = pygame.image.load('Graphics/tail_left.png')
            self.img_fruit = pygame.image.load('Graphics/apple.png')
            
            # Redimensiona as imagens para caberem perfeitamente nos "quadradinhos" do jogo
            self.img_head = pygame.transform.scale(self.img_head, (block_size, block_size))
            self.img_body = pygame.transform.scale(self.img_body, (block_size, block_size))
            self.img_fruit = pygame.transform.scale(self.img_fruit, (block_size, block_size))
        except FileNotFoundError:
            # Fallback de segurança exclusivo para os testes
            self.img_head = pygame.Surface((block_size, block_size))
            self.img_body = pygame.Surface((block_size, block_size))
            self.img_fruit = pygame.Surface((block_size, block_size))

    def parse_event(self, event):
        # Se for um evento de apertar tecla e estiver no nosso mapa, atualiza
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                self.last_input = self.key_map[event.key]

    def display(self, screen, snake_body, fruit_list):
        # Limpa a tela
        screen.fill((0, 0, 0)) 
        
        for f_x, f_y in fruit_list:
            coordenada = (f_x * self.block_size, f_y * self.block_size)
            screen.blit(self.sprites['apple'], coordenada)
            
        # Desenha a Cobra Dinamicamente
        for index, (p_x, p_y) in enumerate(snake_body):
            coordenada = (p_x * self.block_size, p_y * self.block_size)
            
            # Pergunta ao Cérebro Visual qual é o nome correto da imagem
            nome_correto = get_sprite_name(snake_body, index)
            
            # Vai no dicionário buscar o sprite exato e desenha na tela
            screen.blit(self.sprites[nome_correto], coordenada)
                
        # Atualiza a tela
        if not isinstance(screen, type(pygame.Surface((1,1)))): 
            pass
        else:
            pygame.display.flip()

def get_sprite_name(corpo, index):
    if index == 0:
        head_x, head_y = corpo[0]
        neck_x, neck_y = corpo[1]

        # Compara a cabeça com o pescoço
        if head_y < neck_y: return "head_up"
        if head_y > neck_y: return "head_down"
        if head_x > neck_x: return "head_right"
        if head_x < neck_x: return "head_left"

    elif index == len(corpo) - 1:
        tail_x, tail_y = corpo[index]
        front_x, front_y = corpo[index - 1] # A parte do corpo que está ligada à cauda

        # Compara a ponta da cauda com o bloco da frente
        if tail_y < front_y: return "tail_up"
        if tail_y > front_y: return "tail_down"
        if tail_x > front_x: return "tail_right"
        if tail_x < front_x: return "tail_left"

    else:
        # Pega a coordenada atual e as coordenadas dos dois vizinhos (anterior e próximo)
        x, y = corpo[index]
        prev_x, prev_y = corpo[index - 1]
        next_x, next_y = corpo[index + 1]

        # Se o X de ambos os vizinhos for igual, é uma linha reta vertical
        if prev_x == next_x: return "body_vertical"
        
        # Se o Y de ambos os vizinhos for igual, é uma linha reta horizontal
        if prev_y == next_y: return "body_horizontal"

        # Se não é reta, é curva! Vamos verificar em quais posições os vizinhos estão:
        vizinhos_x = (prev_x, next_x)
        vizinhos_y = (prev_y, next_y)

        is_left = (x - 1) in vizinhos_x
        is_right = (x + 1) in vizinhos_x
        is_up = (y - 1) in vizinhos_y
        is_down = (y + 1) in vizinhos_y

        if is_up and is_left: return "body_topleft"
        if is_up and is_right: return "body_topright"
        if is_down and is_left: return "body_bottomleft"
        if is_down and is_right: return "body_bottomright"