board = list(range(10))


def draw_field(board):
    print('-' * 13)
    for i in range(3):
        print("|", board[i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
        print('-' * 13)


def game_step(index, char):
    '''функция хода игрока'''
    if (index > 8 or index < 0 or board[index] in ('X', 'O')):
        return False
    board[index] = char
    return True


def check_win():
    win = False

    win_combination = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6),
    )
    for p in win_combination:
        if (board[0] == board[1] == board[2]):
            win = board[0]

    return win


def turns():
    current_player = 'X'
    step = 1

    draw_field(board)

    while (step <= 9) and (check_win() == False):
        try:
            index = int(
                input('Ходит игрок ' + current_player + '. куда хотите поставить точку?(Если хотите выйти введите 9)'))
        except ValueError:
            print('Нужно написать цифру!')

        if (index == 9):
            break

        if (game_step(index, current_player)):
            print('все хорошо!')

            if (current_player == 'X'):
                current_player = 'O'
            else:
                current_player = 'X'

            draw_field(board)

            step += 1
        else:
            print('Неверный ход!')

    if step == 10:
        print('Ничья!')
    else:
        print('Выиграл игрок ' + check_win())


turns()
