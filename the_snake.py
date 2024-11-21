from random import randint, choice

import pygame

"""Константы для размеров поля и сетки"""
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

""" Константа центра поля"""
SENTRAL_POINT = (GRID_WIDTH / 2 * GRID_SIZE, GRID_HEIGHT / 2 * GRID_SIZE)

"""Направления движения:"""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Цвет фона - черный:"""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

"""Цвет границы ячейки"""
BORDER_COLOR = (93, 216, 228)

"""Цвет яблока"""
APPLE_COLOR = (255, 0, 0)

"""Цвет камня"""
STONE_COLOR = (145, 110, 48)

"""Цвет змейки"""
SNAKE_COLOR = (0, 255, 0)

"""Скорость движения змейки:"""
SPEED = 10

"""Настройка игрового окна:"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Заголовок окна игрового поля:"""
pygame.display.set_caption('Змейка')

"""Настройка времени:"""
clock = pygame.time.Clock()

"""Список команд, далее проверка на непо"""
COMANDS_DICT = {
    pygame.K_UP: (DOWN, UP),
    pygame.K_DOWN: (UP, DOWN),
    pygame.K_RIGHT: (LEFT, RIGHT),
    pygame.K_LEFT: (RIGHT, LEFT),
}


class GameObject:
    """Общий класс"""

    def __init__(self) -> None:
        self.position = SENTRAL_POINT
        self.body_color = (0, 0, 0)

    @staticmethod
    def draw(game_object) -> None:
        """Функция отрисовки единичного объекта"""
        head_rect = pygame.Rect(game_object.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, game_object.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    @staticmethod
    def game_over():
        """Функция приостановки программы"""
        pygame.quit()
        raise SystemExit


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self):
        super().__init__()
        self.reset()

    def update_direction(self, side) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = side

    def draw(self):
        """Метод draw класса Snake"""
        super().draw(self)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> None:
        """Метод передвижения змеи"""
        # Добавление элемента в начале
        x, y = self.positions[0]
        new_position_x = ((x + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH)
        new_position_y = ((y + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT)
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
        self.position = SENTRAL_POINT
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        self.position = self.randomize_position([SENTRAL_POINT])
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_position) -> tuple:
        """Задача случайной позиции яблоку"""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_position:
                return (x, y)

    def draw(self):
        """Метод draw класса Apple"""
        super().draw(self)


class Stone(Apple):
    """Класс для камня"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_object.game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_object.game_over()
            elif game_object.direction != COMANDS_DICT[event.key][0]:
                game_object.update_direction(side=COMANDS_DICT[event.key][1])
                break


def main():
    """Оснавная функция с началом игры"""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    udav = Snake()
    apple = Apple()
    baby_stone = Stone()

    """Бесконечный цикл игры"""
    while True:
        clock.tick(SPEED)

        handle_keys(udav)
        udav.move()

        """Проверка на съедание яблока"""
        if udav.get_head_position == apple.position:
            udav.lenght += 1
            apple.position = apple.randomize_position(udav.positions)
        elif (udav.get_head_position == baby_stone.position or
              udav.get_head_position in udav.positions[1:]):
            """Проверка на столкновение с камнем или с собой"""
            udav.reset()
            baby_stone.position = baby_stone.randomize_position(udav.positions)
            apple.position = apple.randomize_position(udav.positions)

        baby_stone.draw()
        apple.draw()
        udav.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
