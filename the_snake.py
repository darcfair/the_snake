from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константа центра поля
SENTRAL_POINT = (GRID_WIDTH / 2 * GRID_SIZE, GRID_HEIGHT / 2 * GRID_SIZE)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (145, 110, 48)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры
class GameObject:
    """Общий класс"""

    def __init__(self) -> None:
        self.position = SENTRAL_POINT
        self.body_color = None

    def draw(self) -> None:
        """Функция отрисовки объекта"""
        pass


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self):
        super().__init__()
        self.lenght = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод draw класса Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> None:
        """Метод передвижения змеи"""
        # Добавление элемента в начале
        new_position_x = ((self.positions[0][0]
                           + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH)
        new_position_y = ((self.positions[0][1]
                           + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT)
        self.position = (new_position_x, new_position_y)
        self.positions.insert(0, self.position)

        # Проверка на съедение яблока
        if self.lenght + 1 == len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    @property
    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змеи (сделан как атрибут)"""
        return self.positions[0]

    def reset(self):
        """Сбрасывание состояние змейки до дефолтного"""
        screen.fill(BOARD_BACKGROUND_COLOR)

        self.lenght = 1
        self.positions = [SENTRAL_POINT]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple:
        """Задача случайной позиции яблоку"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(Apple):
    """Класс для камня"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
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
    """Оснавная функция с началом игры"""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    udav = Snake()
    apple = Apple()
    big_baby_stone = Stone()

    """Бесконечный цикл игры"""
    while True:
        clock.tick(SPEED)

        handle_keys(udav)
        udav.update_direction()
        udav.move()

        """Проверка на съедание яблока"""
        if udav.get_head_position == apple.position:
            udav.lenght += 1
            while True:
                apple.position = apple.randomize_position()
                if apple.position not in udav.positions:
                    break

        """Проверка на столкновение с камнем"""
        if udav.get_head_position == big_baby_stone.position:
            # Небольшая задержка
            clock.tick(1)
            udav.reset()
            big_baby_stone.position = big_baby_stone.randomize_position()

        """Проверка на сталкновение с сомой собой"""
        if udav.get_head_position in udav.positions[1:]:
            # Небольшая задержка
            clock.tick(1)
            udav.reset()
            big_baby_stone.position = big_baby_stone.randomize_position()

        big_baby_stone.draw()
        apple.draw()
        udav.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
