"""24.9.25"""
"""
不是胆大妄为
"""

import random


def pre_boom(x, y):
    global ground, show_ground, length
    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if 0 <= i < length and 0 <= j < length and ground[i][j] != 9:
                ground[i][j] += 1

def detection(x, y):
    global ground, show_ground, length, judge_ground
    judge = True
    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if 0 <= i < length and 0 <= j < length:
                if ground[i][j] == 9:
                    judge = False
                    break
    judge_ground[x][y] = 11
    if judge:
        for i in [x - 1, x, x + 1]:
            if 0 <= i < length and judge_ground[i][y] != 11:
                judge_ground[i][y] = 11

                detection(i, y)
        for j in [y - 1, y, y + 1]:
            if 0 <= j < length and judge_ground[x][j] != 11:
                judge_ground[x][j] = 11
                detection(x, j)
    if ground[x][y] != 9:
        show_ground[x][y] = ground[x][y]


length = 10
number = 10
ground = [[0 for i in range(length)] for j in range(length)]
bomb_area = []
while number > 0:
    a = random.randint(0, length - 1)
    b = random.randint(0, length - 1)
    if ground[a][b] != 9:
        ground[a][b] = 9
        number -= 1
        bomb_area.append([a, b])
for i in bomb_area:
    print(i)
    pre_boom(i[0], i[1])
for i in ground:
    print(i)
show_ground = [[8 for i in range(length)] for j in range(length)]
while True:
    judge_ground = [[0 for i in range(length)] for j in range(length)]
    region = list(map(int,input("2").split()))
    if [region[1] - 1, region[0] - 1] in bomb_area:
        print("lose")
        break
    else:
        detection(region[1] - 1, region[0] - 1)
    for i in show_ground:
        print("".join(show_ground))
