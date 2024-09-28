"""
以后请把信息移交至Git版本控制，不会可以学，方便维护
还有建议代码写标准一些，变成强类型，这样代码提示更加准确！
"""

import random

# 定义全局变量
# 地图，记录地雷和数字
ground = []
# 显示的地图，记录玩家可见的信息
show_ground = []
# 地图的长度
length = 0
# 判断区域，用于记录检测过程
judge_ground = []

# 在地雷周围做标记，增加计数
def pre_boom(x, y):
    """
    在地雷周围做标记，增加计数
    :param x: 地雷的x坐标
    :param y: 地雷的y坐标
    """
    global ground, show_ground, length

    # 遍历地雷周围的每个格子，如果不是地雷，则计数加一
    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if 0 <= i < length and 0 <= j < length and ground[i][j] != 9:
                ground[i][j] += 1

# 检测安全区域，标记已检测区域
def detection(x, y):
    """
    检测安全区域，标记已检测区域
    :param x: 检测区域的x坐标
    :param y: 检测区域的y坐标
    """
    global ground, show_ground, length, judge_ground

    # 判断当前区域是否安全
    judge = True
    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if 0 <= i < length and 0 <= j < length:
                if ground[i][j] == 9:
                    judge = False
                    break

    # 标记已检测区域
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

    # 更新显示的地图
    if ground[x][y] != 9:
        show_ground[x][y] = ground[x][y]


# 初始化地图参数
length = 10
number = 10
ground = [[0 for i in range(length)] for j in range(length)]
bomb_area = []

# 随机布置地雷
while number > 0:
    a = random.randint(0, length - 1)
    b = random.randint(0, length - 1)
    if ground[a][b] != 9:
        ground[a][b] = 9
        number -= 1
        bomb_area.append([a, b])

# 打印地雷位置，并在地雷周围做标记
for i in bomb_area:
    print(i)
    pre_boom(i[0], i[1])

# 打印生成的地图
for i in ground:
    print(i)

# 初始化显示的地图
show_ground = [[8 for i in range(length)] for j in range(length)]

# 游戏主循环
while True:
    judge_ground = [[0 for i in range(length)] for j in range(length)]
    region = list(map(int,input("2").split()))
    # 判断是否踩中地雷
    if [region[1] - 1, region[0] - 1] in bomb_area:
        print("lose")
        break
    else:
        # 检测安全区域
        detection(region[1] - 1, region[0] - 1)

    # 更新并打印显示的地图
    for i in show_ground:
        print("".join(map(str, i)))
