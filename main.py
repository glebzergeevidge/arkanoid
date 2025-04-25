import pygame as pg
import sys
from random import randrange
from time import sleep

class Game:
    def __init__(self):
        pg.init()
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('Breakout')

        self.click_sound = pg.mixer.Sound('sounds/minecraft_click.mp3')
        self.hit_sound = pg.mixer.Sound('sounds/Jump.wav')
        self.lose_sound = pg.mixer.Sound('sounds/lose.mp3')
        self.win_sound = pg.mixer.Sound('sounds/win.mp3')

        self.show_start_screen()


    def show_start_screen(self):
        self.screen.fill(pg.Color('black'))
        self.paddle = Paddle(self)
        self.ball = Ball(self)

        self.font = pg.font.SysFont('arial', 36)

        self.FPS = 120  # FPS
        self.clock = pg.time.Clock()

        self.image = pg.transform.scale(pg.image.load('images/bg.jpg'), (self.WIDTH, self.HEIGHT)).convert()

        self.block_list = [pg.Rect(10 + self.WIDTH // 10 * i,
                                   10 + self.HEIGHT // 10 * j,
                                   110,
                                   60) for i in range(10) for j in range(1)]

        self.color_list = [(randrange(30, 256),
                            randrange(30, 256),
                            randrange(30, 256)) for _ in range(10) for _ in range(1)]

        self.screen.blit(self.image, (0, 0))

        self.font = pg.font.SysFont("arial", 36)

        start_button = self.font.render('Начать игру', True, (255, 255, 255))
        start_button_rect = start_button.get_rect(center=(self.WIDTH // 2, 150))

        settings_button = self.font.render('Управление', True, (255, 255, 255))
        settings_button_rect = settings_button.get_rect(center=(self.WIDTH // 2, 300))

        texts = ['Левая стрелочка (<-) - движение влево', 'Правая стрелочка (->) - движение вправо']

        u_button = self.font.render(f'Левая стрелочка (<-) - движение влево \n Правая стрелочка (->) - движение вправо', True, (255, 255, 255))
        u_button_rect = u_button.get_rect(center=(self.WIDTH // 2, 300))

        exit_button = self.font.render('Выход', True, (255, 255, 255))
        exit_button_rect = exit_button.get_rect(center=(self.WIDTH // 2, 450))

        self.screen.blit(start_button, start_button_rect)
        self.screen.blit(settings_button, settings_button_rect)
        self.screen.blit(exit_button, exit_button_rect)

        pg.display.flip()

        flag = False
        while not flag:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        self.screen.fill((0, 0, 0))
                        flag = True
                    if settings_button_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        self.screen.fill(pg.Color('black'))  # Красим фон в чёрный
                        self.screen.blit(self.image, (0, 0))

                        surfaces = list()  # список поверхностей строк
                        for text in texts:
                            surface = self.font.render(text, True, (255, 255, 255))
                            surfaces.append(surface)
                        # добавляем отрендоринную поверхность текста в список поверхностей

                        new_line = 0  # отступ новой линии в пикселях
                        for surface in surfaces:
                            self.screen.blit(surface, (self.WIDTH // 3.3, self.HEIGHT // 3 + new_line))
                            # рисуем на экране поверхность и к координате Y прибавляем new_line
                            new_line += 50

                        pg.display.flip()
                        sleep(5)
                        self.show_start_screen()

                    if exit_button_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        sleep(self.click_sound.get_length())
                        pg.quit()
                        sys.exit()

    def update(self):
        self.paddle.update()
        self.ball.update()
        pg.display.flip()
        self.clock.tick(self.FPS)

    def draw(self):
        self.screen.blit(self.image, (0, 0))

        for color, block in enumerate(self.block_list):
            pg.draw.rect(self.screen, self.color_list[color], block)

        self.paddle.draw()
        self.ball.draw()

    def check_game_over(self):
        if self.ball.ball.bottom > self.HEIGHT:
            self.lose_sound.play()
            lose_button = self.font.render('GAME OVER!', True, (255, 0, 0))
            lose_button_rect = lose_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(lose_button, lose_button_rect)
            pg.display.flip()
            sleep(5)

            print('GAME OVER!')
            self.show_start_screen()
            pg.display.flip()

        elif not len(self.block_list):
            self.win_sound.play()
            lose_button = self.font.render('УРА, ПОБЕДА!', True, (255, 0, 0))
            lose_button_rect = lose_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(lose_button, lose_button_rect)
            pg.display.flip()
            sleep(5)
            print('WIN!!!')
            sys.exit()

    @staticmethod
    def check_events():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_game_over()
            self.check_events()
            self.update()
            self.draw()


class Paddle:
    def __init__(self, root: Game):
        self.game = root
        self.paddle_w = 250
        self.paddle_h = 30
        self.paddle_speed = 15
        self.rect = pg.Rect(root.WIDTH // 2 - self.paddle_w // 2,
                            root.HEIGHT - self.paddle_h - 10,
                            self.paddle_w, self.paddle_h)

        self.color = pg.Color(200, 130, 50)

    def draw(self):
        pg.draw.rect(self.game.screen, self.color, self.rect)

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.paddle_speed

        elif key[pg.K_RIGHT] and self.rect.right < self.game.WIDTH:
            self.rect.right += self.paddle_speed

class Ball:
    def __init__(self, root: Game):
        self.game = root
        self.radius = 20
        self.speed = 5

        self.rect = int(self.radius * 2 ** 0.5)

        self.ball = pg.Rect(randrange(self.rect, self.game.WIDTH- self.rect),
                            self.game.HEIGHT // 2, self.rect, self.rect)
        self.dx, self.dy = 1, -1

    def draw(self):
        pg.draw.circle(self.game.screen,
                       pg.Color(255, 255, 255),
                       self.ball.center,
                       self.radius)

    def move(self):
        self.ball.x += self.speed * self.dx
        self.ball.y += self.speed * self.dy

    def check_collisions(self):
        if self.ball.centerx < self.radius or self.ball.centerx > self.game.WIDTH - self.radius:
            self.dx = -self.dx
        if self.ball.centery < self.radius:
            self.dy = -self.dy

    def calculate_movement(self, rect):
        if self.dx > 0:
            delta_x = self.ball.right - rect.left
        else:
            delta_x = rect.right - self.ball.left

        if self.dy > 0:
            delta_y = self.ball.bottom - rect.top
        else:
            delta_y = rect.bottom - self.ball.top

        if abs(delta_x - delta_y) < 10:
            self.dx, self.dy = -self.dx, -self.dy

        elif delta_x > delta_y:
            self.dy = -self.dy

        elif delta_x < delta_y:
            self.dx = -self.dx

    def check_paddle(self):
        if self.ball.colliderect(self.game.paddle) and self.dy > 0:
            self.calculate_movement(self.game.paddle.rect)

    def check_block_collision(self):
        hit_index = self.ball.collidelist(self.game.block_list)

        if hit_index != -1:
            hit_rect = self.game.block_list.pop(hit_index)
            self.game.hit_sound.play()
            self.game.color_list.pop(hit_index)

            self.calculate_movement(hit_rect)
            self.game.FPS += 0

    def update(self):
        self.move()
        self.check_collisions()
        self.check_paddle()
        self.check_block_collision()

if __name__ == '__main__':
    game = Game()
    game.run()
