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
        
        # Desenha todas as frutas
        for f_x, f_y in fruit_list:
            coordenada = (f_x * self.block_size, f_y * self.block_size)
            screen.blit(self.img_fruit, coordenada)
            
        # Desenha a cobra a partir da lista do corpo
        for index, (p_x, p_y) in enumerate(snake_body):
            coordenada = (p_x * self.block_size, p_y * self.block_size)
            
            if index == 0:
                screen.blit(self.img_head, coordenada) # Cabeça
            else:
                screen.blit(self.img_body, coordenada) # Corpo
                
        # Atualiza a tela
        if not isinstance(screen, type(pygame.Surface((1,1)))): 
            pass
        else:
            pygame.display.flip()