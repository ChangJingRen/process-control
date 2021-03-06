import pygame


class Window:
    def __init__(self, tank):
        pygame.init()
        pygame.display.set_caption("9 Tank simulation")
        self.WINDOW_HEIGHT = 1000
        self.WINDOW_WIDTH = 1115
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        self.background_image = pygame.image.load(
            "Q_learning/Tank_9/visualize/images/8_tanks.png"
        ).convert()
        self.background_image = pygame.transform.scale(
            self.background_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )

        self.clock = pygame.time.Clock()
        self.tank1 = TankImage(tank[0], 81, 34)
        self.tank2 = TankImage(tank[1], 433, 34)
        self.tank3 = TankImage(tank[2], 783, 34)
        self.tank4 = TankImage(tank[3], 81, 353)
        self.tank5 = TankImage(tank[4], 433, 353)
        self.tank6 = TankImage(tank[5], 783, 353)
        self.tank7 = TankImage(tank[6], 81, 553)
        self.tank8 = TankImage(tank[7], 433, 553)
        self.tank9 = TankImage(tank[8], 783, 553)

    def Draw(self, input_z):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.screen.blit(self.background_image, [0, 0])
        self.tank1.draw(self.screen, input_z[0])
        self.tank2.draw(self.screen, input_z[1])
        self.tank3.draw(self.screen, input_z[2])
        self.tank4.draw(self.screen, input_z[3])
        self.tank5.draw(self.screen, input_z[4])
        self.tank6.draw(self.screen, input_z[5])
        self.tank7.draw(self.screen, input_z[6])
        self.tank8.draw(self.screen, input_z[7])
        self.tank9.draw(self.screen, input_z[8])
        pygame.display.flip()
        return True


class TankImage:
    height = 186
    width = 147
    choke_width = 35
    choke_height = 5
    rga_water = (25, 130, 150)
    rga_choke = (0, 0, 0)
    choke_left_adj = 234
    choke_top_adj = -7
    choke_range = 155

    def __init__(self, tank, left_pos, top_pos):
        self.tank = tank
        self.left_pos = left_pos
        self.top_pos = top_pos

    def draw(self, screen, z):
        self.draw_level(screen)
        self.draw_choke(screen, z)

    def draw_level(self, screen):
        level_percent = (self.tank.level - self.tank.min) / (
            self.tank.max - self.tank.min
        )
        pygame.draw.rect(
            screen,
            TankImage.rga_water,
            pygame.Rect(
                self.left_pos,
                self.top_pos + (1 - level_percent) * TankImage.height,
                TankImage.width,
                level_percent * TankImage.height,
            ),
        )

    def draw_choke(self, screen, z):
        pygame.draw.rect(
            screen,
            TankImage.rga_choke,
            pygame.Rect(
                self.left_pos + TankImage.choke_left_adj,
                self.top_pos
                + TankImage.choke_top_adj
                + (1 - z) * TankImage.choke_range,
                TankImage.choke_width,
                TankImage.choke_height,
            ),
        )

