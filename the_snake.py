"""Игра 'Змейка' на PyGame."""

from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
BORDER_COLOR = (93, 216, 228)       # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)          # Цвет яблока
SNAKE_COLOR = (0, 255, 0)          # Цвет змейки

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализация базового игрового объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Отрисовка игрового поля и сетки."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.draw_grid()

    def draw_grid(self):
        """Отрисовка сетки игрового поля."""
        for i in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, (i, 0), (i, SCREEN_HEIGHT))
        for i in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, (0, i), (SCREEN_WIDTH, i))


class Apple(GameObject):
    """Класс для управления яблоком."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Установка случайной позиции яблока на поле."""
        self.position = (
            choice(range(0, SCREEN_WIDTH, GRID_SIZE)),
            choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        )


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки."""
        head = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()
    game = GameObject()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if (head[0] >= SCREEN_WIDTH or head[0] < 0
                or head[1] >= SCREEN_HEIGHT or head[1] < 0):
            snake.reset()

        if head in snake.positions[1:]:
            snake.reset()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position()

        game.draw()
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
