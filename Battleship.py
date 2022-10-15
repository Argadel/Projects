from random import randint
print()
print("Let's play Battleship!")
print()
print("Enter 2 coords (x and y) one by one")
print()
print("＼(＾▽＾)／  Good Luck!  ＼(＾▽＾)／")
print()


class Coords:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Board_Exception(Exception):
    pass


class Out_of_the_Field(Board_Exception):
    def __str__(self):
        return "Your shot is out of the field!"


class Used_Place(Board_Exception):
    def __str__(self):
        return "You've already shot there!"


class Wrong_Ship(Board_Exception):
    pass


class Ship:
    def __init__(self, direction, l, orientation) -> None:
        self.direction = direction
        self.type = l
        self.orientation = orientation
        self.lives = l

    @property
    def coords(self):
        ship_coords = []
        for i in range(self.type):
            or_x = self.direction.x
            or_y = self.direction.y

            if self.orientation == 0:
                or_x += i

            elif self.orientation == 1:
                or_y += i

            ship_coords.append(Coords(or_x, or_y))

        return ship_coords

    def damage(self, shot):
        return shot in self.coords


class Board:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide
        self.count = 0

        self.field = [["0"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        field = ""
        field += "    1   2   3   4   5   6 "
        for i, j in enumerate(self.field):
            field += f"\n{i + 1} | " + " | ".join(j) + " |"

        if self.hide:
            field = field.replace("■", "0")
        return field

    def around_the_ship(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for coord in ship.coords:
            for coord_x, coord_y in near:
                around = Coords(coord.x + coord_x, coord.y + coord_y)
                if not (self.out(around)) and around not in self.busy:
                    if verb:
                        self.field[around.x][around.y] = "."
                    self.busy.append(around)

    def add_ship(self, ship):
        for coord in ship.coords:
            if self.out(coord) or coord in self.busy:
                raise Wrong_Ship()
        for coord in ship.coords:
            self.field[coord.x][coord.y] = "■"
            self.busy.append(coord)

        self.ships.append(ship)
        self.around_the_ship(ship)

    def out(self, out):
        return not all([0 <= out.x < self.size,
                        0 <= out.y < self.size])

    def shot(self, shot):
        if self.out(shot):
            raise Out_of_the_Field()

        if shot in self.busy:
            raise Used_Place()

        self.busy.append(shot)

        for ship in self.ships:
            if ship.damage(shot):
                ship.lives -= 1
                self.field[shot.x][shot.y] = "🔥"
                if ship.lives == 0:
                    self.count += 1
                    self.around_the_ship(ship, verb=True)
                    print("The ship sank!")
                    return False
                else:
                    print("The ship is hit!")
                    return True

        self.field[shot.x][shot.y] = "."
        print("You've missed!")
        return False

    def start(self):
        self.busy = []


class Players:
    def __init__(self, field, enemy):
        self.field = field
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except Board_Exception as e:
                print(e)


class AI(Players):
    def ask(self):
        coords = Coords(randint(0, 5), randint(0, 5))
        print(f"Computer makes a move: {coords.x + 1} {coords.y + 1}")
        return coords


class User(Players):
    def ask(self):
        while True:
            coords = input("Your move: ").split()

            if len(coords) != 2:
                print("Enter 2 coords!")
                continue

            x, y = coords

            if not any([x.isdigit(), y.isdigit()]):
                print("Use digits!")
                continue

            x, y = int(x), int(y)

            return Coords(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_field()
        computer = self.random_field()
        computer.hide = True

        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def create_field(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        field = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Coords(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    field.add_ship(ship)
                    break
                except Wrong_Ship:
                    pass
        field.start()
        return field

    def random_field(self):
        field = None
        while field is None:
            field = self.create_field()
        return field

    def lets_start(self):
        num = 0
        while True:
            print("-" * 20)
            print("Player's Field:")
            print(self.user.field)
            print("-" * 20)
            print("Computer's Field:")
            print(self.ai.field)
            if num % 2 == 0:
                print("-" * 20)
                print("Player makes a move!")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Computer makes a move!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.field.count == 7:
                print("-" * 20)
                print("＼(≧▽≦)／   Player has won!   ＼(≧▽≦)／")
                break

            if self.user.field.count == 7:
                print("-" * 20)
                print("＼(≧▽≦)／   Computer has won!   ＼(≧▽≦)／")
                break
            num += 1

    def start(self):
        self.lets_start()


Lets_Play = Game()
Lets_Play.start()
