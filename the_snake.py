"""Модуль игры «Змейка».

Содержит классы GameObject, Apple, Snake и основную логику игры.
"""

import pygame

from random import randint


# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует игровой объект.

        Если позиция не передана, устанавливается в центр игрового поля.
        """
        if position is None:
            center_x = (GRID_WIDTH // 2) * GRID_SIZE
            center_y = (GRID_HEIGHT // 2) * GRID_SIZE
            position = (center_x, center_y)
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на поверхности.

        По умолчанию ничего не делает — переопределяется в наследниках.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко в игре."""

    def __init__(self):
        """Создаёт яблоко и размещает его в случайной точке поля."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Размещает яблоко в случайной клетке сетки."""
        rand_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        rand_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (rand_x, rand_y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(
            surface,
            BORDER_COLOR,
            rect,
            1
        )


class Snake(GameObject):
    """Класс, описывающий змейку в игре."""

    def __init__(self):
        """Создаёт змейку, устанавливает начальную позицию и направление."""
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        start_position = (center_x, center_y)

        super().__init__(body_color=SNAKE_COLOR, position=start_position)

        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки в соответствии с текущим направлением."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Применяет новое направление, и не является разворотом на 180°."""
        if self.next_direction is not None:
            opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
            if self.next_direction != opposite.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def check_self_collision(self):
        """Проверяет, не столкнулась ли голова змейки с её телом."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        start_position = (center_x, center_y)

        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на поверхности, стирая предыдущий след."""
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                surface,
                BOARD_BACKGROUND_COLOR,
                last_rect
            )

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(
                surface,
                BORDER_COLOR,
                rect,
                1
            )


def handle_keys(snake):
    """нажатие клавиш и направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры: инициализация и игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw(screen)
            apple.draw(screen)
            pygame.display.update()
            continue

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
    