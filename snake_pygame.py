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

    def parse_event(self, event):
        # Se for um evento de apertar tecla e estiver no nosso mapa, atualiza
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                self.last_input = self.key_map[event.key]