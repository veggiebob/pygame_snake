class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    @staticmethod
    def to_vector (d):
        if d == 0: # up
            return [-1, 0]
        elif d == 1: # left
            return [0, -1]
        elif d==2: # down
            return [1, 0]
        elif d==3: # right
            return [0, 1]
    @staticmethod
    def from_vector (i, j):
        if j == 1:
            return Direction.RIGHT
        elif j == -1:
            return Direction.LEFT
        elif i == 1:
            return Direction.DOWN
        elif i == -1:
            return Direction.UP
    @staticmethod
    def reverse_direction (d):
        v = Direction.to_vector(d)
        v[0] *= -1
        v[1] *= -1
        return Direction.from_vector(v[0], v[1])

class Turn:
    STRAIGHT = 0
    RIGHT = 1
    LEFT = -1
    @staticmethod
    def from_vectors (a, b):
        # do a cross product
        c = a[0]*b[1]-a[1]*b[0]
        return Turn.RIGHT if c > 0 else Turn.LEFT if c < 0 else Turn.STRAIGHT

class SnakePart:
    START = 0
    BODY = 1
    END = 2


class Snake:
    MIN_LENGTH = 3
    def __init__ (self, pos):
        self.path = [pos]
        self.length = 1
        self.dead = False
        self.latest = pos
        self.movement = []
        self.last_dir = 2
        self.fruits_eaten = 0
        self.grown = 0

    def move (self, fruit=False):
        di = self.last_dir
        v = Direction.to_vector(di)
        self.movement.append(di)
        self.latest = [
            self.latest[0]+v[0],
            self.latest[1]+v[1]
        ]
        self.path.append(self.latest)
        if not fruit and self.length >= Snake.MIN_LENGTH + self.grown:
            self.path = self.path[1:]
            self.length -= 1
        self.length += 1
        # if self.check_bump_into(self):
        #     print('bumped into self')
        #     self.die()

    def check_bump_into (self, snek):
        self_head = self.get_head()
        other_snake_head = snek.get_head()
        other_snake_length = snek.length
        # checking if self_head is in the same square as any segment of the other snake
        l = other_snake_length
        for segment in snek.path:
            l -= 1
            if l == 0:
                continue
            if segment[0] == self_head[0] and segment[1] == self_head[1]:
                # crash!
                return True
        return False
    def flush (self):
        m = self.movement[0:]
        self.movement = []
        return m
    def is_head (self, index):
        return index == len(self.path)-1
    def is_tail (self, index):
        return index == 0
    def get_head (self):
        return self.latest

    def set_direction (self, di):
        self.last_dir = di

    def eat_fruit (self, grow=True):
        self.fruits_eaten += 1
        if grow:
            self.grown += 1

    def die (self):
        self.dead = True

    def cut (self):
        if self.length > 1:
            self.path = self.path[1:]
            self.length -= 1
            self.grown -= 1

    def get_relative_next (self, index):
        if index == len(self.path)-1:
            return self.last_dir
        elif index == -1:
            return self.get_relative_next(0)
        else:
            return Direction.from_vector(self.path[index+1][0]-self.path[index][0], self.path[index+1][1]-self.path[index][1])

    def get_turn (self, index):
        prev = self.get_relative_next(index-1)
        iturn = self.get_relative_next(index)
        iturn = Direction.to_vector(Direction.reverse_direction(iturn))
        prev = Direction.to_vector(prev)
        return Turn.from_vectors(prev, iturn)

    def get_body_part (self, index):
        if self.is_head(index):
            return SnakePart.START
        elif self.is_tail(index):
            return SnakePart.END
        else:
            return SnakePart.BODY
    def get_snake_image (self, snake_animator, index, dim_size):
        return snake_animator.get_snake_image(self.get_body_part(index), self.get_turn(index), self.get_relative_next(index), dim_size)