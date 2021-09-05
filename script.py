# my 'cross-zero' game source code
# global vars
# next lists are intended for caching checking results
# 0- no way to win, 3-winner is possible
rows=[3,3,3]
cols=[3,3,3]
diags=[3,3]
# making the game matrix. Define that -10=empty cell, 1=zero, 2=cross
matrix=[[-10 for j in range(3)]for i in range(3)]
# the dict of chars for rendering game matrix
chars={-10:'-',1:'O',2:'Х'}
# Players. The dict contains players data: the key (1=zero, 2=cross) and the list of [name,is a winner? (True or False)]
players={1:['',False],2:['',False]}

# the following function checks if there are winners already. Returns 0 if no winners,
# else return the code of winner type (1- zero, 2 - cross). Return 3 if it's the drawn
def is_there_winner():
    drawn=True
    # check rows
    for i in range(3):
        if rows[i]:
            res=chek_nums(matrix[i])
            if 0 < res <3:
                return res
            else:
                drawn = drawn and res!=3
                rows[i]=res
    # check columns
    for i in range(3):
        if cols[i]:
            res=chek_nums([matrix[0][i],matrix[1][i],matrix[2][i]])
            if 0 < res <3:
                return res
            else:
                drawn = drawn and res != 3
                cols[i]=res
    # check diagonals
    if diags[0]:
        res = chek_nums([matrix[0][0], matrix[1][1], matrix[2][2]])
        if 0 < res < 3:
            return res
        else:
            drawn = drawn and res != 3
            cols[i] = res
    if diags[1]:
        res = chek_nums([matrix[0][2], matrix[1][1], matrix[2][0]])
        if 0 < res < 3:
            return res
        else:
            drawn = drawn and res != 3
            cols[i] = res
    if drawn:
        return 3
    else:
        return 0


# check win status of 3 integers. Return 0-winner is impossible, 1 - zeros winned, 2- crosses winned, 3-winner is probable
def chek_nums(lst : list):
    total = sum(lst)
    if total > 0:
        if total == 3:
            return 1
        elif total == 6:
            return 2
        else:
            return 0
    elif total ==-7:
        return 0
    else:
        return 3


# rendering of game matrix for printing
def render_matrix():
    s ='   0 1 2\n 0 '
    s = s+' '.join(list(map(lambda x:chars[x],matrix[0]))) +'\n 1 '
    s = s + ' '.join(list(map(lambda x: chars[x], matrix[1]))) + '\n 2 '
    s = s + ' '.join(list(map(lambda x: chars[x], matrix[2])))
    return s

# the MAIN code
while True:
    players[1]=input('Кто играет ноликами? (введите имя) : ').lower().capitalize()
    players[2]=input('Кто играет крестиками? (введите имя) : ').lower().capitalize()
    if players[1] == players[2]:
        print('Имена игроков не должны совпадать')
    else:
        break
print(f'Добро пожаловать в игру {players[1]} и {players[2]}!')
# the loop of gameplay
print('Первыми ходят крестики!')
mode = 2
while True:
    msg = f'{players[mode]}, укажите через запятую строку (0-2) и столбец (0-2), где хотите поставить {"крестик" if mode == 2 else "нолик"}: '
    while True:
        s=input(msg)
        s=list(map(int, list(s.split(','))))
        if matrix[s[0]][s[1]] == mode:
            msg=f'Вы уже поставили {"крестик" if mode == 2 else "нолик"} в этой ячейке, выбирете другую строку и столбец: '
        elif matrix[s[0]][s[1]] > 0:
            msg=f'В этой ячейке уже стоит {"нолик" if mode == 2 else "крестик"}, выбирете другую строку и столбец: '
        else:
            matrix[s[0]][s[1]] = mode
            break
    print(render_matrix())
    winner=is_there_winner()
    if 0 < winner < 3:
        print(f'Игра окончена! Победу одержал(а) {players[winner]} ({"крестики" if winner == 2 else "нолики"})')
        break
    elif winner == 3:
        print('Игра закончена! Победила дружба! Это нужно отметить )')
        break
    mode = 1 if mode == 2 else 2