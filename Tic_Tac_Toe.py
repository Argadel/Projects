print()
print("Let's play Tic Tac Toe!")
print()
print(" /ᐠ .ᆺ. ᐟ\ﾉ ")
print()

field = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]


def game_field():
    print(f"  0 1 2")
    print(f"0 {field[0][0]} {field[0][1]} {field[0][2]}")
    print(f"1 {field[1][0]} {field[1][1]} {field[1][2]}")
    print(f"2 {field[2][0]} {field[2][1]} {field[2][2]}")


def coords():
    while True:
        print()
        i, j = map(int, input("Your turn is  ").split())
        print()
        if 0 <= i <= 2 and 0 <= j <= 2:
            if field[i][j] == "-":
                return i, j
            else:
                print("The cell is not available!")
                print()
                game_field()
        else:
            print("Your coords are out of the range! Please, check again:")
            print()
            game_field()


def check_game():
    victory_variants = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                        ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                        ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2))]
    for coord in victory_variants:
        symbols = []

        for s in coord:
            symbols.append(field[s[0]][s[1]])

            if symbols == ["x", "x", "x"]:
                print("＼(≧▽≦)／   Winner is X!   ＼(≧▽≦)／")
                print()
                game_field()
                return True
            if symbols == ["0", "0", "0"]:
                print("＼(≧▽≦)／    Winner is 0!   ＼(≧▽≦)／")
                print()
                game_field()
                return True
    return False


def steps():
    count = 0
    while True:
        count += 1
        game_field()
        if count % 2 == 1:
            print()
            print("Player 1 takes turn!")
        else:
            print()
            print("Player 2 takes turn!")

        i, j = coords()

        if count % 2 == 1:
            field[i][j] = 'x'
        else:
            field[i][j] = '0'

        if check_game():
            break

        if count == 9:
            print()
            print("¯\_(ツ)_/¯   Draw!   ¯\_(ツ)_/¯")
            break

steps()
