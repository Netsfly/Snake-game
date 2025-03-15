import pygame, sys, random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

        self.base_speed = 0.2
        self.speed = self.base_speed
        self.base_interval = 150
        self.move_interval = self.base_interval
        self.position = Vector2(self.body[0].x * cell_size, self.body[0].y * cell_size)
        self.target = self.body[0]
        self.has_moved = False
        self.move_timer = 0

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        self.update_position()

        for index, block in enumerate(self.body):
            if index == 0:
                x_pos, y_pos = int(self.position.x), int(self.position.y)
            else:
                x_pos, y_pos = int(block.x * cell_size), int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self, dt):
        if self.direction == Vector2(0, 0):
            return

        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            new_head = self.body[0] + self.direction
            if self.new_block:
                self.body.insert(0, new_head)
                self.new_block = False
            else:
                self.body = [new_head] + self.body[:-1]

            self.target = new_head
            self.move_timer -= self.move_interval
            self.has_moved = True

    def update_position(self):
        target_pos = Vector2(self.target.x * cell_size, self.target.y * cell_size)
        if self.position != target_pos:
            direction = (target_pos - self.position).normalize()
            self.position += direction * self.speed * cell_size
            if (target_pos - self.position).length() < self.speed * cell_size:
                self.position = target_pos

    def add_block(self):
        self.new_block = True
        self.speed = self.base_speed + (len(self.body) - 3) * 0.005
        self.move_interval = max(50, self.base_interval - (len(self.body) - 3) * 5)

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.speed = self.base_speed
        self.move_interval = self.base_interval
        self.position = Vector2(self.body[0].x * cell_size, self.body[0].y * cell_size)
        self.target = self.body[0]
        self.has_moved = False
        self.new_block = False
        self.move_timer = 0


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_active = False
        self.paused = False
        self.show_start_screen = True
        self.high_score = 0

    def update(self, dt):
        self.snake.move_snake(dt)
        self.check_collision()
        self.check_fail()
        self.snake.update_position()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

    def check_fail(self):
        if self.snake.has_moved:
            if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                self.game_over()
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

    def game_over(self):
        score = len(self.snake.body) - 3
        self.high_score = max(self.high_score, score)
        self.game_active = False
        self.show_start_screen = False

    def draw_game_over(self):
        game_over_surface = game_font.render("Game Over! Press R to Restart", True, (56, 74, 12))
        score_text = f"Score: {len(self.snake.body) - 3}"
        high_score_text = f"High: {self.high_score}"
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        high_score_surface = game_font.render(high_score_text, True, (56, 74, 12))

        game_over_rect = game_over_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 40))
        score_rect = score_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        high_score_rect = high_score_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 40))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)

    def draw_start_screen(self):
        start_surface = game_font.render("Press S to Start", True, (56, 74, 12))
        title_surface = game_font.render("Snake Game", True, (56, 74, 12))

        title_rect = title_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 40))
        start_rect = start_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 20))

        screen.blit(title_surface, title_rect)
        screen.blit(start_surface, start_rect)

    def draw_grass(self):
        grass_color = (167, 209, 61)
        dark_grass = (150, 190, 50)
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                color = grass_color if (row + col) % 2 == 0 else dark_grass
                pygame.draw.rect(screen, color, grass_rect)
        pygame.draw.rect(screen, (56, 74, 12), (0, 0, cell_size * cell_number, cell_size * cell_number), 5)

    def draw_score(self):
        score = len(self.snake.body) - 3
        score_text = f"Score: {score}"
        high_score_text = f"High: {self.high_score}"
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        high_score_surface = game_font.render(high_score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        high_score_y = int(cell_size * cell_number - 20)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        high_score_rect = high_score_surface.get_rect(center=(score_x, high_score_y))
        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        self.snake.reset()
        self.fruit.randomize()
        self.game_active = True
        self.show_start_screen = False
        self.snake.direction = Vector2(1, 0)


# Initialization
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

pygame.mixer.music.load('Sound/background.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

main_game = MAIN()

while True:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if main_game.show_start_screen and event.key == pygame.K_s:
                main_game.start_game()
            elif main_game.game_active and not main_game.paused:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_p and main_game.game_active:
                main_game.toggle_pause()
            if event.key == pygame.K_r and not main_game.game_active and not main_game.show_start_screen:
                main_game.start_game()

    if main_game.game_active and not main_game.paused:
        main_game.update(dt)

    screen.fill((175, 215, 70))
    if main_game.show_start_screen:
        main_game.draw_start_screen()
    elif main_game.game_active:
        main_game.draw_elements()
        if main_game.paused:
            pause_surface = game_font.render("Paused", True, (56, 74, 12))
            pause_rect = pause_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
            screen.blit(pause_surface, pause_rect)
    else:
        main_game.draw_game_over()

    pygame.display.update()