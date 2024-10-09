"""
一个游戏地图的工具类
"""
import random


class GameMap:
    """
    一个地图类
    """
    def __init__(self, map_width, map_height, bomb_num, timer_thread):
        """
        
        :param map_width: 地图长
        :param map_height: 地图宽
        :param bomb_num: 地雷数
        :param timer_thread: 计时器对象
        """
        self.width = map_width
        self.height = map_height
        # 计时器对象
        self.timer = timer_thread
        # 地图数据
        self.ground:list = [[0 for i in range(map_width)] for j in range(map_height)]
        # 用于布置地雷的地雷数
        self.__bomb_num = bomb_num
        # 用于记录原始地雷数
        self.bomb_num = bomb_num
        # 地雷位置
        self.bomb_area:list = []
        # 判断区域，用于记录检测过程
        self.judge_ground:list = [[0 for i in range(map_width)] for j in range(map_height)]
        # 用于显示的地图
        self.show_ground:list = [["block" for i in range(map_width)] for j in range(map_height)]
        # 用于显示需要更新的地图块
        self.update_block:list = []
        # 用于显示已经点击过的地图坐标
        self.has_clicked_pos:list = []
        # 用于记录坐标的标识状态
        self.has_clicked_state:list = [["empty" for i in range(map_width)] for j in range(map_height)]
        # 用于记录已经正确标记的地雷数量
        self.bomb_found_num = 0
        # 用于记录所有标记为sure的坐标
        self.sure_num = []
        # 随机布置地雷
        while self.__bomb_num > 0:
            b = random.randint(0, map_width - 1)
            a = random.randint(0, map_height - 1)
            if self.ground[a][b] != 9:
                self.ground[a][b] = 9
                self.__bomb_num -= 1
                self.bomb_area.append([a, b])

        # 打印地雷位置，并在地雷周围做标记
        for i in self.bomb_area:
            self.pre_boom(i[0], i[1])

    # 在地雷周围做标记，增加计数
    def pre_boom(self, x, y):
        """
        在地雷周围做标记，增加计数
        :param x: 地雷的x坐标
        :param y: 地雷的y坐标
        """
        # 遍历地雷周围的每个格子，如果不是地雷，则计数加一
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if 0 <= i < self.height and 0 <= j < self.width and self.ground[i][j] != 9:
                    self.ground[i][j] += 1

    # 检测安全区域，标记已检测区域
    def detection(self, x, y):
        """
        检测安全区域，标记已检测区域
        :param x: 检测区域的x坐标
        :param y: 检测区域的y坐标
        """
        # 判断当前区域是否安全
        judge = True
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.ground[i][j] == 9:
                        judge = False
                        self.update_block.append([y, x, "bomb"])
                        break

        # 标记已检测区域
        self.judge_ground[x][y] = 11
        if judge:
            for i in [x - 1, x, x + 1]:
                if 0 <= i < self.height and self.judge_ground[i][y] != 11:
                    self.judge_ground[i][y] = 11
                    self.detection(i, y)

            for j in [y - 1, y, y + 1]:
                if 0 <= j < self.width and self.judge_ground[x][j] != 11:
                    self.judge_ground[x][j] = 11
                    self.detection(x, j)

        # 更新显示的地图
        if self.ground[x][y] != 9:
            self.show_ground[x][y] = self.ground[x][y] if self.ground[x][y] != 0 else "empty"
            self.update_block.append([y, x,self.show_ground[x][y]])
            if (x, y) in self.sure_num:
                self.sure_num.remove((x, y))




