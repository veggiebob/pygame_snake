class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    @staticmethod
    def toVector (d):
        if d == 0: # up
            return [-1, 0]
        elif d == 1: # left
            return [0, -1]
        elif d==2: # down
            return [1, 0]
        elif d==3: # right
            return [0, 1]
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
        v = Direction.toVector(di)
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